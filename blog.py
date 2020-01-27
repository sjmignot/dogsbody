from flask import Flask, render_template, redirect, url_for, render_template_string, Markup
from flask_flatpages import FlatPages, pygments_style_defs, pygmented_markdown
import markdown
from flask_frozen import Freezer
from slugify import slugify
import sys
import re
import datetime
import json

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
MARKDOWN_EXTENSIONS = ['codehilite', 'footnotes', 'fenced_code']
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
OTHER_DIR = 'other'

def prerender_jinja(text):
    prerendered_body = render_template_string(Markup(text))
    pygmented = markdown.markdown(prerendered_body, extensions = app.config['MARKDOWN_EXTENSIONS'])
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        return header_markdown_preprocess(img_markdown_preprocess(pygmented))
    else:
        return header_markdown_preprocess(pygmented)

FLATPAGES_HTML_RENDERER = prerender_jinja

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

app.config.from_object(__name__)

def img_markdown_preprocess(page):
    '''adds a srcset attribute to all images to allow responsive image serving. Requires name of all images file to be the same. '''
    image_sizes = {'sm':'320w', 'md':'640w', 'lg': '1024w'}
    img_pattern = r"<img alt=\".*\" src=\"(/static/img/.*)\" />"
    src_replace_pattern = r"src=\"/static/img/.*\""
    srcset_size_pattern = "src=\"{img_src}\" srcset=\"{srcset_val}\"" #sizes=\"(max-width: 640px) 480px, (min-width:768px) 800px, 1200w\""
    img_matches = re.findall(img_pattern, page)
    for img_match in img_matches:
        srcset_val = ', '.join([img_match.replace(".jpg", f"-{k}.jpg")+f" {v}" for k, v in image_sizes.items()])
        src_replace_value = srcset_size_pattern.format(img_src=img_match, srcset_val=srcset_val)
        page = re.sub(src_replace_pattern, src_replace_value, page)
    return page

def header_markdown_preprocess(page):
    '''adds a srcset attribute to all images to allow responsive image serving. Requires name of all images file to be the same. '''
    header_pattern = r"<h2>(.*)</h2>"
    header_matches = re.findall(header_pattern, page)
    for match in header_matches:
        header_replace = f"<h2 class=\"group relative z-0\" id=\"{slugify(match)}\"><a class=\"header-link absolute inline-block opacity-0 group-hover:opacity-100 pin-l pin-t transition-ease\" href=\"#{slugify(match)}\">#</a>{match}</h2>"
        header_pattern = re.compile(f"<h2>{match}</h2>")
        page = re.sub(header_pattern, header_replace, page)
    return page


@app.route('/')
def home():
    return redirect(url_for('blog'))

@app.route("/posts/")
def blog():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=True)
    dates = [post['date'].strftime("%b. %d, %Y").lower() for post in posts]
    post_names = [p.path.replace('posts/','') for p in posts]
    return render_template('posts.html', posts=zip(posts,dates), post_names=post_names)

@app.route('/post/<name>/')
def blog_post(name):
    path = '{}/{}'.format(POST_DIR, name)
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    post = flatpages.get_or_404(path)
    date = post['date'].strftime("%b. %d, %Y").lower()
    post_names = [p.path.replace('posts/', '') for p in posts]
    return render_template('post.html', post=post, date=date, post_names=post_names)

@app.route("/about/")
def about():
    path = '{}/{}'.format(OTHER_DIR, 'about')
    about = flatpages.get_or_404(path)
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    post_names = json.dumps([p.path.replace('posts/','') for p in posts])
    return render_template('about.html', about=about, post_names=post_names)

@app.route("/backblog/")
def backblog():
    path = '{}/{}'.format(OTHER_DIR, 'backblog')
    backblog= flatpages.get_or_404(path)
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    post_names = json.dumps([p.path.replace('posts/','') for p in posts])
    return render_template('backblog.html', backblog=backblog, post_names=post_names)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)

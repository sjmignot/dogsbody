from flask import Flask, render_template, redirect, url_for, render_template_string, Markup
from flask_flatpages import FlatPages, pygments_style_defs, pygmented_markdown
import markdown
from flask_frozen import Freezer

from slugify import slugify
import os
import sys
import re
import datetime
import json

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
MARKDOWN_EXTENSIONS = ['codehilite', 'footnotes', 'fenced_code']

# FLATPAGES DIRS
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
OTHER_DIR = 'other'
FICTION_DIR = 'fiction'
CODING_DIR = 'coding'
PHOTOS_DIR = 'photos'
POETRY_DIR = 'poetry'

CATEGORY_DICT = {
    'fiction': FICTION_DIR,
    'coding': CODING_DIR,
    'photos': PHOTOS_DIR,
    'poetry': POETRY_DIR
}


# MARKDOWN POSTPROCESS FUNCTIONS FOR RESPONSIVE IMAGES AND HEADERS WITH ANCHOR TAGS
def img_markdown_postprocess(page):
    '''
    adds a srcset attribute to all images to allow responsive image serving.
    Requires name of all images file to be the same.
    '''
    image_sizes = {'sm': '480w', 'md': '640w', 'lg': '1024w'}
    img_pattern = r"<img alt=\".*\" src=\"(/static/img/.*)\" />"
    src_replace_pattern = 'src="{img_src}"'
    srcset_size_pattern = 'src="{img_src}" srcset="{srcset_val}"'
    img_matches = re.findall(img_pattern, page)
    for img_match in img_matches:
        print(img_match)
        srcset_val = ', '.join([
            img_match.replace(".jpg", f"-{k}.jpg") + f" {v}"
            for k, v in image_sizes.items()
        ])
        src_replace_value = srcset_size_pattern.format(img_src=img_match,
                                                       srcset_val=srcset_val)
        page = re.sub(
            re.compile(src_replace_pattern.format(img_src=img_match)),
            src_replace_value, page)
    return page


def header_markdown_postprocess(page):
    '''
    Adds link to all post headers.
    Requires name of all images file to be the same.
    '''
    header_pattern = r"<h2>(.*)</h2>"
    header_matches = re.findall(header_pattern, page)
    for match in header_matches:
        header_replace = (
            f'<div class=\"post-header__padding\" id=\"{slugify(match)}\"></div>'
            f'<h2 class=\"post__header\">'
            f'<a class=\"header-link\" href=\"#{slugify(match)}\">#</a>'
            f'{match}'
            f'</h2>')
        header_pattern = re.compile(f"<h2>{re.escape(match)}</h2>")
        page = re.sub(header_pattern, header_replace, page)
    return page


MARKDOWN_POSTPROCESS = [
    (header_markdown_postprocess, False),
    (img_markdown_postprocess, True),
]


def markdown_postprocess(pygmented, build):
    '''
    Runs every markdown postprocess function on pygmented html generated from markdown files.
    '''
    for process_function, build_only in MARKDOWN_POSTPROCESS:
        if not build_only or build:
            pygmented = process_function(pygmented)
    return pygmented


# MARKDOWN PREPROCESS FUNCTIONS FOR FORMATTING FICTION AND POETRY PAGES


def format_prose(page):
    '''
    Formats prose posts so that line breaks are respected, paragraphs are indented.
    '''
    return page


def format_poetry(page):
    '''
    formats poetry posts so text is indented; and linebreaks, leading spaces, and tabs aren't ignored
    '''
    leading_whitespace = r'^ *'
    page = re.sub(leading_whitespace,
                  lambda x: 2 * len(x[0]) * '&nbsp;',
                  page,
                  flags=re.MULTILINE)
    page = re.sub('\n\n', "\n<br>\n\n  ", page, flags=re.MULTILINE)
    page = re.sub('  \n', "  \n\n", page, flags=re.MULTILINE)
    return page


def writing_markdown_preprocess(page):
    split_page = page.splitlines()
    if (split_page[0] == 'fiction_post'):
        return format_prose('\n'.join(split_page[1:]))
    elif (split_page[0] == 'poetry_post'):
        return format_poetry('\n'.join(split_page[1:]))
    return page


MARKDOWN_PREPROCESS = [(writing_markdown_preprocess, False)]


def markdown_preprocess(pygmented):
    '''runs markdown preprocess function on markdown text extracted from markdown files'''
    for process_function, build_only in MARKDOWN_PREPROCESS:
        if not build_only or build:
            pygmented = process_function(pygmented)
    return pygmented


def prerender_jinja(text):
    text = markdown_preprocess(text)
    prerendered_body = render_template_string(Markup(text))
    pygmented = markdown.markdown(prerendered_body,
                                  extensions=app.config['MARKDOWN_EXTENSIONS'])
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        return markdown_postprocess(pygmented, True)
    else:
        return markdown_postprocess(pygmented, False)


FLATPAGES_HTML_RENDERER = prerender_jinja

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

app.config.from_object(__name__)


def get_posts():
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        return [
            p for p in flatpages
            if p.path.startswith(POST_DIR) and 'draft' not in p.meta
        ]
    else:
        return [p for p in flatpages if p.path.startswith(POST_DIR)]


def get_coding_projects():
    coding = [
        p for p in flatpages if p.path.startswith(f'{CODING_DIR}/projects')
    ]
    coding.sort(key=lambda x: x['date'])
    return coding


def get_coding_notebooks():
    coding = [
        p for p in flatpages if p.path.startswith(f'{CODING_DIR}/notebooks')
    ]
    print([c['date'] for c in coding])
    coding.sort(key=lambda x: x['date'])
    return coding


def get_photos_pages():
    photos = [p for p in flatpages if p.path.startswith(PHOTOS_DIR)]
    photos.sort(key=lambda x: x['date'])
    return photos


def get_fiction_pages():
    fiction = [p for p in flatpages if p.path.startswith(FICTION_DIR)]
    fiction.sort(key=lambda x: x['date'])
    return fiction


def get_poetry_pages():
    poetry = [p for p in flatpages if p.path.startswith(POETRY_DIR)]
    poetry.sort(key=lambda x: x['date'])
    return poetry


def add_preview(latest_post):
    latest_post.preview = latest_post.body[:latest_post.body.
                                           find('!')].replace(
                                               '\n', ' ')[:300] + "..."
    return latest_post


@app.route('/')
def home():
    posts = get_posts()
    posts.sort(key=lambda item: item['date'], reverse=True)
    latest_post = posts[0]
    return render_template('index.html', latest_post=add_preview(latest_post))


@app.route("/posts/")
def blog():
    posts = get_posts()
    posts.sort(key=lambda item: item['date'], reverse=True)
    dates = [post['date'].strftime("%b. %d, %Y").lower() for post in posts]
    return render_template('posts.html', posts=zip(posts, dates))


@app.route('/posts/<name>/')
def blog_post(name):
    path = f'{POST_DIR}/{name}'
    post = flatpages.get_or_404(path)
    date = post['date'].strftime("%b. %d, %Y").lower()
    img_path = f'static/img/post-images/{name}/colors.svg'
    if os.path.isfile(img_path):
        with open(img_path, 'r') as f:
            svg = Markup(f.read())
    else:
        svg = False
    return render_template('post.html', post=post, date=date, svg=svg)


@app.route("/about/")
def about():
    path = '{}/{}'.format(OTHER_DIR, 'about')
    about = flatpages.get_or_404(path)
    return render_template('about.html', about=about)


@app.route("/about/resume/")
def resume():
    return render_template('resume.html')


@app.route('/projects/<category>/<name>/')
def project_page(category, name):
    path = f'{CATEGORY_DICT[category]}/{name}'
    project_page = flatpages.get_or_404(path)
    date = project_page['date'].strftime("%b. %d, %Y").lower()
    return render_template(
        'project_page.html',
        project_page=project_page,
        date=date,
    )


@app.route("/projects/")
def projects():
    return render_template('projects.html',
                           fiction=get_fiction_pages(),
                           poetry=get_poetry_pages(),
                           photos=get_photos_pages(),
                           coding_projects=get_coding_projects(),
                           notebooks=get_coding_notebooks())


@app.route('/projects/notebooks/<name>/')
def notebook_page(name):
    path = f'coding/notebooks/{name}'
    notebook_page = flatpages.get_or_404(path)
    date = notebook_page['date'].strftime("%b. %d, %Y").lower()
    return render_template('jupyter_notebook.html',
                           notebook_page=notebook_page,
                           date=date)


@app.route("/contact/")
def contact():
    return render_template('contact.html')


@app.route('/sitemap.xml')
def site_map():
    posts = get_posts()
    posts.sort(key=lambda item: item['date'], reverse=True)
    return render_template('sitemap_template.xml',
                           posts=posts,
                           base_url="https://sjmignot.github.io",
                           date=datetime.datetime.today().date())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)

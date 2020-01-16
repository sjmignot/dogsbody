from flask import Flask, render_template, redirect, url_for
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
import sys
import datetime
import random
import json

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
OTHER_DIR = 'other'

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)

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

from flask import Flask, session, url_for, redirect, jsonify, render_template, request, flash
from gennames import gennames
import os
from functools import wraps

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='\x04\xdf\x9aW\r\xa3\x9f\xaf\x9b\x89A\xb7\xa1\xb0h+\xc8\x0c\xfe\xe1\xbdI\r\x8f',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.realpath('./sqlite.db'),
    SEARCH_RADIUS = 1
))
import models
from geoloc import geoloc

#Decorator function that checks for authentication
def requires_checkin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or 'loc' not in session:
            flash('Location required')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#filter for jinga to turn spaces to underscores
@app.template_filter('space_to_underscore')
def space_to_underscore(string):
    return '_'.join(string.split(' '))


@app.route('/', methods=['GET'])
@requires_checkin
def get_all_posts():
    return render_template('posts.html', posts=models.Post.get_all(session['loc']))

@app.route('/post/<slug>/<title>')
@requires_checkin
def get_post(slug, title):
    post = models.Post.get_post_from_slug(slug)
    return render_template('post.html', post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session:
        session['username'] = gennames.gen_name()
    form = models.LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        lat = form.lat.data
        lon = form.lon.data
        session['loc'] = {'lat':lat, 'lon':lon}
        return redirect(url_for('get_all_posts'))
    return render_template('login.html', form=form)


@app.route('/newpost', methods=['GET', 'POST'])
@requires_checkin
def new_post():
    form = models.PostForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        username = session['username']
        locx = session['loc']['lon']
        locy = session['loc']['lat']
        post = models.Post(title=title, body=body, username=username, locx=locx, locy=locy)
        models.db.session.add(post)
        models.db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('newpost.html', form=form)

#Generate posts as Json
@app.route('/api/posts/')
def get_posts_json():
    posts = [post.to_dict() for post in models.Post.query.all()]
    return jsonify({'posts':posts})

#API point that shows all replies to a post and accepts new replies
@app.route('/api/post/<id>/')
def get_post_json(id):
    post = models.Post.query.get_or_404(id)
    if post:
        replies = [reply.to_dict() for reply in models.Post.query.get(id).replies]
    return jsonify({'post':post.to_dict(), 'replies':replies})

def init_db():
    models.db.create_all()


if __name__ == '__main__':
    app.run()



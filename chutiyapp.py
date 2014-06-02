from flask import Flask, session, url_for, redirect, jsonify, render_template, request
from gennames import gennames
import os

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='\x04\xdf\x9aW\r\xa3\x9f\xaf\x9b\x89A\xb7\xa1\xb0h+\xc8\x0c\xfe\xe1\xbdI\r\x8f',
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
))
import models

#The api point that shows all posts and accepts new posts
@app.route('/', methods=['GET'])
def posts():
    return get_posts_json()

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    username = get_name()
    form = models.PostForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        locx = form.locx.data
        locy = form.locy.data
        post = models.Post(title=title, body=body, username=username, locx=locx, locy=locy)
        models.db.session.add(post)
        models.db.session.commit()
        return redirect(url_for('posts'))
    return render_template('newpost.html', form=form)

#Generate posts as Json
def get_posts_json():
    posts = [post.to_dict() for post in models.Post.query.all()]
    return jsonify({'posts':posts})

#API point that shows all replies to a post and accepts new replies
@app.route('/api/post/<id>/')
def get_post(id):
    return get_post_json(id)

#generate posts as json
def get_post_json(id):
    replies = [reply.to_dict() for reply in models.Post.query.get(id).replies]
    return jsonify({'replies':replies})

#Returns username from session or generates a new one and saves to session
def get_name():
    try:
        username = session['username']
    except KeyError, e:
        username = ''.join(gennames.gen_name())
        session['username'] = username
    except:
        username = "AnonymousCoward"
    return username




if __name__ == '__main__':
    app.run()



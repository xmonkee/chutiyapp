from chutiyapp import app
from random import randrange
from string import capitalize
from models import Post, Reply, db
from gennames import gennames

lorem = ''.join(open('lorem.txt'))

def get_random_lorem():
    first = randrange(len(lorem)/2)
    second = first + randrange(len(lorem)/2)
    return lorem[first:second]

def get_random_title():
    first = randrange(len(lorem)/2)
    second = first + randrange(140)
    return lorem[first:second]

def populate_databse(n,m):
    for i in range(n):
        post = Post(title = capitalize(get_random_title()), body=get_random_lorem(), locx=20, locy=20, username=gennames.gen_name())
        db.session.add(post)
        for j in range(n):
            reply = Reply(post=post, body=get_random_lorem(), username=gennames.gen_name())
            db.session.add(reply)
    db.session.commit()

if __name__=='__main__':
    populate_databse(200, 200)
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    if blog_id is not None:
        blogs = Blog.query.filter_by(id=blog_id)
        return render_template('blogpost.html', blogs=blogs)
    else:
        blogs = Blog.query.all()    
        return render_template('blog.html',blogs=blogs)







def empty_entry(entry):
    if entry == '':
        return False
    else:
        return True


@app.route('/newpost', methods=['POST'])
def newpost_error():
    body_error = ''
    title_error = ''
    blog_body = request.form['blog']
    blog_title = request.form['title']
    spider_man = True

    if empty_entry(blog_body) == False:
        body_error = 'Please fill in body'
        spider_man = False
    if empty_entry(blog_title) == False:
        title_error ='Please fill in title'
        spider_man = False


    if spider_man == False:
        return render_template('newpost.html', title_error=title_error, body_error=body_error)    
    else:
        blog_body = request.form['blog']
        blog_title = request.form['title']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('blog?id={0}'.format(new_blog.id))




@app.route('/newpost', methods=['GET'])
def newpost():
        return render_template('newpost.html')


if __name__ == '__main__':
    app.run()
from flask import  Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String

app =Flask(__name__)

# DB config
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
db= SQLAlchemy(app)
# end DB config

# Database Model
class AllBlogPost(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    Content=db.Column(db.Text,nullable=False)
    Author=db.Column(db.String,nullable=False,default='N/A')
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return'Blog Post ' +str(self.id)

# Database end   
# datetime.datetime.today().strftime("%d %b")


allPosts=[
    {
      "title":"Post 1",
      "Content":"this is the content Numero 1"  ,
      "Author":"Peter Dongle"
    },
     {
      "title":"Post 2",
      "Content":"this is the content Numero duo" ,
      "Author" :"Pimp the dog"
    },
     {
      "title":"Post 2",
      "Content":"this is the content Numero duo" ,
      "Author" :""
    },
    
    ]

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/posts',methods=['POST','GET'])
def posts():
    if request.method=='POST':
        post_title=request.form['title']
        post_content=request.form['Content']
        post_author=request.form['Author']
        newBlog=AllBlogPost(title=post_title,Content=post_content,Author=post_author)
        db.session.add(newBlog)
        db.session.commit()
        return redirect('/posts')
    else:
        allPosts=AllBlogPost.query.order_by(AllBlogPost.date_posted).all()
        return render_template('/posts.html',posts=allPosts)


# delete route
@app.route('/posts/delete/<int:id>')
def delete(id):
    post=AllBlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

# edit route
@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post=AllBlogPost.query.get_or_404(id)
    if request.method=='POST':
       
        post.title=request.form['title']
        post.Author=request.form['Author']
        post.Content=request.form['Content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post)


@app.route('/home/<string:name>')
def hello(name):
    return "Hello world " +name


@app.route('/onlyget',methods=['GET','POST'])
def get_req():
   
    return 'You can only get this request'






if __name__=="__main__":
    app.run(debug=True)
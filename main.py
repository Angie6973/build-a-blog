from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def is_valid(self):
        if self.title and self.body:
            return True
        else:
            return False




@app.route("/blog")
def display_blog_entries():
    
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Blog.query.get(entry_id)
        return render_template('blog.html', entry=entry)

    #
    all_entries = Blog.query.all()
    
       
    return render_template('blog.html', all_entries=all_entries)   
    
     


@app.route("/newpost", methods=['POST', 'GET'])
def new_entry():
    if request.method =='POST':

        blog_title=request.form['title'] 
        blog_body=request.form['body'] 
        new_entry=Blog(blog_title,blog_body) 

        if new_entry.is_valid:

            db.session.add(new_entry)
            db.session.commit()
            return redirect("/blog?id="+str(new_entry.id))        
        

        else:
            flash("Please check your entry for errors. Both a title and body are required.")
            return render_template("newpost.html")

    else:
        return render_template("newpost.html")

    

    
if __name__ == '__main__':
    app.run()
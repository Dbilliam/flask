from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError , TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# flask_migrate : its database migrate old date covert new data
from flask_migrate import Migrate
# werkzeug : its a flask libery its convert hash the password
from werkzeug.security import generate_password_hash, check_password_hash
# for big text Area Need for our blog
from wtforms.widgets import TextArea
# for login Model 
from flask_login import UserMixin, login_user, login_manager, login_required, logout_user, current_user, LoginManager
# Use other form 
from webforms import LoginForm
from flask_ckeditor import CKEditor
from flask_ckeditor import CKEditorField 
# ad file field for upload file in website
from flask_wtf.file import FileField 
# add file Security with werkzeug
from werkzeug.utils import secure_filename
# file convert with uuid unique number with uuid
import uuid as uuid
# then save on os
import os
# func
from sqlalchemy.sql import func
# date new function
from datetime import timedelta





# Create a Flask Instance

app = Flask(__name__)
# Add Ckeditor for Editor.
ckeditor = CKEditor(app)

'''
FILTER
safe, 
capitalize, 
lower, 
uppeer, 
title , 
trim, 
striptags
'''

# For
# if


# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
# add new mysql database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/our_users'
# Secret Key!

app.config['SECRET_KEY'] = "raKE738@$"



# create the extension
db=SQLAlchemy()

# Initialize Migrate extentions its help update our internal database
migrate=Migrate(app, db)
# make vi
# python -m venv virt
# source virt/Scripts/activate
# pip freeze

# winpty python => create sqlalchmey database
# from app import db
#  db.create_all()
# then git terminal cmd: flask db init
# then git terminal cmd: flask db
# then git terminal cmd: flask db migrate -m 'Initial Migration'
# then think are push in database
# cmd: flask db upgrade

# then any time need update data with Migrate
# cmd: flask db migrate -m "commit something added new data"
# cmd: flask db upgrade


# Initialize The Database
db.init_app(app)


# file Upload Configations Like tell over app where is the file will save
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




# Create a Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    # author = db.Column(db.String(255))
    banner = db.Column(db.LargeBinary)
    content = db.Column(db.Text)
    # date_posted = db.Column(db.DateTime(timezone=True), default=func.now())
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    # Foreign Key to Link Users (refer to primary key to users)
    # poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    comments = db.relationship(
        'Comment', backref='posts', cascade='all, delete, delete-orphan', lazy=True, passive_deletes=True)
    likes = db.relationship('Like', cascade='all, delete, delete-orphan',
                            backref='posts', lazy=True, passive_deletes=True)


# Create Model

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    profile_pic = db.Column(db.String(), nullable=True)
    about_author = db.Column(db.Text(120), nullable=True)
    address = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    # posts = db.relationship('Posts', backref='poster')
    posts = db.relationship('Posts', cascade='all, delete, delete-orphan',
                            backref='users', lazy=True, passive_deletes=True)
    comments = db.relationship(
        'Comment', cascade='all, delete, delete-orphan', backref='user', lazy=True, passive_deletes=True)
    likes = db.relationship('Like', cascade='all, delete, delete-orphan',
                            backref='users', lazy=True, passive_deletes=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Create aString
    def __repr__(self):
        return '<Name %r>' % self.name

    #hash property
    @property
    def password(self):
        raise AttributeError('password is not a readable attibute!')
    # set-up the password 
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)   
    # verify the password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# Comments 
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(380), nullable=False)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)


# Like
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)




with app.app_context():
    db.create_all()
if __name__=="__main__":
    app.run(debug=True)

# Some Flask_login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# CREATE A Form Class
class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    about_author= TextAreaField("About Author")
    address = StringField("Address", validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")
    password_hash = PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2', message='Password Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


# CREATE A Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create A Password Form Class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create A Blog Post Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author")
    banner = FileField('Banner')
    # content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('Content',validators=[DataRequired()])
    slug = StringField("Slug", [DataRequired()])
    submit = SubmitField("Submit")
    
# Create A Search Form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

# # Create A Login Form
# class LoginForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired()])
#     password = PasswordField("Password", validators=[DataRequired()])
#     submit = SubmitField("Submit")





# # wtf form
# BooleanField
# DataField
# DateTimeField
# DecimalField
# FileField
# HinddenField
# MultipleField
# FloatField
# FieldList
# FloatField
# FormField
# IntegerField
# PasswordField
# RadioField
# SelectField
# SelectMultipleField
# SubmitField
# StringField
# TextAreaField
# # Validations
# DataRequied
# Email
# EqualTo
# InputRequired
# IPAddress
# Length
# MacAddress
# NumberRange
# Optional
# Regexp
# URL
# UUID
# AnyOf
# NoneOf
# Create a route decorator

@app.route('/')
def index():
    flash("Welcome to my Travel Hub")
    title = "Be Lived Life"
    stuff =" This is <strong>Bold</strong> Text"
    category =["Bungee jump","Zip lines","Hill walk","Camping","Rock Climbing","Cycling","Trekking","kayaking"]
    return render_template("index.html", title_name = title, stuff=stuff, category_name= category)


#local user/rakesh dinammic name
@app.route("/user/<name>")    
def user(name):
    return render_template("user.html", user_name=name)

# Create custom Error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Create login Page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     name = None
#     form = NamerForm()
#     # validation
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#         flash("Registion Form Submitted Successfully!")

#     return render_template("login.html" , name = name, form = form)


@app.route('/signup', methods=['GET','POST'])
def signup():
    name = None
    form = UserForm()
    # validation
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash the password!!
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data , address=form.address.data, password_hash=hashed_pw)
            # user = Users(name=form.name.data, email=form.email.data , address=form.address.data, password_hash=form.password_hash.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data 
        # then I clear the form
        # form.username.data = ''
        form.username.data = ''
        form.name.data = ''
        form.email.data = ''  
        form.address.data = ''
        form.password_hash = ''
        flash("User Added Successfully!")
    # our_users = Users.query.limit(3).all()
    our_users = Users.query.order_by(Users.date_added)
    return render_template("signup.html" ,name = name,form = form, our_users=our_users)



# Update Database Record
@app.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    id = current_user.id or current_user.id == 1
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.username = request.form["username"]
        name_to_update.email = request.form["email"]
        name_to_update.about_author = request.form["about_author"]
        name_to_update.address = request.form["address"]
        
        # check for profile pic
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files["profile_pic"]
            # Grab Image Name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            # set UUID this make ramdom number
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Last Save That Image
            saver = request.files['profile_pic']
            # change it to a string to save to db
            name_to_update.profile_pic = pic_name 
            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfully!")
                return render_template("dashboard.html", form=form, name_to_update=name_to_update)
            except:
                flash("Error! Looks like there was a problem try again")
                return render_template("update.html", form=form, name_to_update=name_to_update)
        else:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)


@app.route('/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete(id):
    if id  == current_user.id or current_user.id == 1:
        user_to_delete = Users.query.get_or_404(id)
        name = None
        form = UserForm()
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Deleted Successfully")
            our_users = Users.query.order_by(Users.date_added)
            return render_template("signup.html", name=name, form=form, our_users=our_users)
        except:
            flash("Whoops! There was a problem deleting user try again.....")    
            return render_template("signup.html", name=name, form=form, our_users=our_users)
    else:
        flash("Sorry, You can't delete that user! ")
        return redirect(url_for('dashboard'))

@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
    return render_template("name.html", name=name, form=form)    


@app.route('/password_test', methods=['GET','POST'])
def password_test():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # clear the form
        form.email.data = ''
        form.password_hash.data = ''


        # Look up by Email Address
        pw_to_check = Users.query.filter_by(email=email).first()
        # flash("Form Submitted Successfully!")
        
        #check Hashed Password
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template("password_test.html", email=email, password=password, form=form, pw_to_check=pw_to_check, passed=passed)    


# JSON is open standard file format and date interchange that uses human-readable 
# text to store and transmit data objects consisting of attibute-value pairs and arrays.
@app.route('/date')
def get_current_date():
    return {"date": datetime.today()}

# Add Or Create Blog Post
@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    author = current_user.id
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=author, slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        # form.author.data = ''
        form.slug.data = ''
        # add blog post data to database
        db.session.add(post)
        db.session.commit()
        flash("Blog Post Submitted Successfully!")
        return render_template('add_post.html', form=form)  
    flash("Blog Post Submitted Successfully!")
    return render_template('add_post.html', form=form)        

# Show Blog Page 
@app.route('/blog')
def blog():
    # Grab all the blog posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("blog.html", posts=posts)

# Read more blog page add 
@app.route('/blog/<int:id>')
def blogs(id):
    blogs = Posts.query.get_or_404(id)
    return render_template('blogs.html', blogs=blogs)

# Edit or Update Blog Post
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_blog(id):
    post = Posts.query.get_or_404(id)
    form= PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update database
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!")
        return redirect(url_for('blogs',id=post.id))
    if current_user.id == post.poster_id or current_user.id == 1:    
        form.title.data = post.title
        # form.author.data = post.author
        form.content.data = post.content
        form.slug.data = post.slug
        return render_template('edit_post.html', form=form)   
    else:
        flash("You Aren't Authorized to Edit This Post...")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("blog.html", posts=posts)

# Delete The blogs
@app.route('/blog/delete/<int:id>')
@login_required
def delete_blog(id):
    post_to_delete = Posts.query.get_or_404(id)
    id= current_user.id
    if id == post_to_delete.poster.id or id == 1:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            # Return A Message
            flash("Blog Post Was Deleted!")

            # Grab all the blog posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("blog.html", posts=posts)    
        except:
            # Reurn an error message
            flash("Whoops! There was a problem deleting post, try again...")
            
            # Grab all the blog posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("blog.html", posts=posts)    
    else:
        # return a message
        flash("You Aren't Authorized to Delete That Post!")   
        # Grab all the blog posts from the database
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("blog.html", posts=posts)    

        
# Create Login Page
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Succesfull!!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again!") 
        else:
            flash("That User Doesn't Exist! Try Again....")           
    return render_template('login.html',form=form)


# Create Logout Page
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out! Thanks ")
    return redirect(url_for('login'))


# Create Dashboard Page
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


# PAss stuff to navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get data from submited form
        postsearched = form.searched.data
        # Query the database
        posts = posts.filter(Posts.content.like('%' + postsearched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template('search.html', form=form, searched = postsearched, posts=posts)


@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template("admin.html")
    else:
        flash("Sorry you must be the admin to access the Admin Page.....")
        return redirect(url_for('dashboard'))    


@app.route('/events')   
def events():
    return render_template("events.html")     

@app.route('/abouts')   
def abouts():
    return render_template("abouts.html")     




@app.route('/event', methods=['GET', 'POST'])
@login_required
def event():
    form= PostForm()
    author = current_user.id
    if request.method == 'POST':
        # content = request.form.get('content')
        post = Posts(title=form.title.data, content=form.content.data, author=author, slug=form.slug.data)
        comments = request.form.get('comment')
        print(post, comments)
        if not post:
            flash('Can\'t post without any words!', category='error')
        else:
            new_post = Posts(post=post, author=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post successfully added!', category='success')
            return redirect(url_for('/'))

    # posts = Posts.query.all()
    posts = Posts.query.order_by(Posts.date_posted)
    correct_time = timedelta(hours=4)
    return render_template('new-events.html', user=author, posts=posts, correct_time=correct_time, form=form)

@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = Users.query.filter_by(username=username).first()
    if not user:
        flash('Hey! that user does not exist', category='error')
    users_posts = user.posts
    correct_time = timedelta(hours=4)
    username = user.username
    return render_template('profile.html', user=current_user, users_posts=users_posts,
                           correct_time=correct_time, username=username)


# @app.route('/delete-acct/<username>', methods=['GET', 'POST'])
# @login_required
# def delete_acct(username):
#     user = Users.query.filter_by(username=username).first()
#     if not user:
#         flash('Sorry that user doesn\'t exist.', category='error')
#     elif current_user.id != user.id:
#         flash('you aren\'t authorized to delete this acct', category='error')
#     else:
#         if user.likes:
#             [db.session.delete(i) for i in user.likes]
#         if user.comments:
#             [db.session.delete(i) for i in user.comments]
#         if user.posts:
#             [db.session.delete(i) for i in user.posts]
#         db.session.delete(user)
#         db.session.commit()
#         flash('user successfully deleted!', category='success')
#     print([i for i in Users.query.all()])
#     return redirect(url_for('home'))


# @app.route('/delete-post/<post_id>', methods=['GET', 'POST'])
# @app.route('/profile/delete-post/<post_id>', methods=['GET', 'POST'])
# @login_required
# def delete_post(post_id):
#     post = Posts.query.filter_by(id=post_id).first()
#     if not post:
#         return jsonify({'error': 'this post either doesn\'t exist or can\'t be deleted'})

#     elif post.author != current_user.id:
#         flash('You are not authorized to delete this post', category='error')

#     else:
#         if post.likes:
#             [db.session.delete(i) for i in post.likes]
#         if post.comments:
#             [db.session.delete(i) for i in post.comments]
#         db.session.delete(post)
#         db.session.commit()
#         flash('Post successfully deleted!', category='success')
#     return jsonify({'success': 'facts',
#                     'postId': post_id})


@app.route('/add-comment/<post_id>', methods=['GET', 'POST'])
@login_required
def add_comment(post_id):
    if request.method == 'POST':
        comment = request.form.get('comment')
        if not comment:
            return jsonify({'error': 'No comment to add'}, 400)
        else:
            post = Posts.query.filter_by(id=post_id).first()
            if post:
                new_comment = Comment(text=comment,
                                      author=current_user.id, post_id=post_id)
                db.session.add(new_comment)
                db.session.commit()
                flash('Successfully posted comment!', category='success')

            else:
                flash('No post available', category='error')
    post = Posts.query.filter_by(id=post_id).first()
    postId = post.id
    return jsonify({'success': 'facts', 'postId': postId})


@app.route('/delete-comment/<comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        return jsonify({'error': 'Comment doesn\'t exist'}, 400)
        # flash('Comment doesn\'t exist', category='error')

    elif current_user.id != comment.user.id and current_user.id != comment.post.author:
        flash('You are not authorized to delete this post', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment successfully deleted', category='success')
    postId = comment.post_id
    post = Posts.query.filter_by(id=postId).first()
    print(postId)
    return jsonify({'success': 'facts',
                    'postId': postId,
                    'commentLen': len(post.comments)})


@app.route('/like-post/<post_id>', methods=['GET', 'POST'])
@login_required
def like_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post doesn\'t exist'}, 400)

    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({'likes': len(post.likes),
                    'liked': current_user.id in map(lambda n: n.author, post.likes)})






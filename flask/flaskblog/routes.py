import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ProfProfile
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    if current_user.is_authenticated == True:
        posts = Post.query.filter_by(user_id=current_user.id)
    return render_template('profile.html', posts=posts)





@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.creditcard = form.creditcard.data
        current_user.expdate = form.expdate.data
        current_user.cvc = form.cvc.data
        current_user.bill_address = form.bill_address.data
        current_user.bill_zip = form.bill_zip.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        try:
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.name.data = current_user.name
            form.creditcard.data = current_user.creditcard
            form.expdate.data = current_user.expdate
            form.cvc.data = current_user.cvc
            form.bill_address.data = current_user.bill_address
            form.bill_zip.data = current_user.bill_zip
        except:
            form.username.data = current_user.username
            form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        print("HEREEEEE!!!!!!!!!!")
        print(form.resume.data)
        if form.resume.data:
            print("It submittedd>>>>>>>>>>>")
            picture_file = save_picture(form.resume.data)
            resume = picture_file
            post = Post(name=form.name.data, title=form.title.data, email=form.email.data, author=current_user, phone=form.phone.data, linkedin=form.linkedin.data, reference1_name=form.reference1_name.data, reference1_number=form.reference1_number.data, reference2_name=form.reference2_name.data, reference2_number=form.reference2_number.data, reference3_name=form.reference3_name.data, reference3_number=form.reference3_number.data, resume=resume) 
        else:
            print("FUCKKKKKK")
            post = Post(name=form.name.data, title=form.title.data, email=form.email.data, author=current_user, phone=form.phone.data, linkedin=form.linkedin.data, reference1_name=form.reference1_name.data, reference1_number=form.reference1_number.data, reference2_name=form.reference2_name.data, reference2_number=form.reference2_number.data, reference3_name=form.reference3_name.data, reference3_number=form.reference3_number.data)     
        db.session.add(post)
        db.session.commit()
        flash('Your profile has been created! Your account was charged $0.50', 'success')
        return redirect(url_for('about'))
    return render_template('create_post.html', title='New Post',
                          form=form, legend='New Post')
    
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('about'))

@app.route("/computer_science_resume_user_1", methods=['GET'])
@login_required
def resume_cs():
    post = Post.query.filter_by(user_id=current_user.id).first()
    phone = post.phone
    name = post.name
    title = post.title
    email = post.email
    linkedin = post.linkedin
    ref1 = post.reference1_name
    ref1num = post.reference1_number
    ref2 = post.reference2_name
    ref2num = post.reference2_number
    ref3 = post.reference3_name
    ref3num = post.reference3_number
    resume = post.resume
    resume_file = url_for('static', filename='profile_pics/claire.jpg')
    home = url_for('static', filename='profile_pics/house.png')
    work = url_for('static', filename='profile_pics/fol.png')
    contact = url_for('static', filename='profile_pics/env.png')
    linkimg = home = url_for('static', filename='profile_pics/li.png')
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('prof_profile.html', home=home, work=work, linkimg=linkimg, contact=contact, phone=phone, image_file=image_file, title=title, name=name, email=email, linkedin=linkedin, ref1=ref1, ref1num=ref1num, ref2=ref2, ref2num=ref2num, ref3=ref3, ref3num=ref3num, resume=resume_file)
    
import os

from flask import render_template, flash, redirect, url_for, request, current_app
from pathsixgames import app, db, bcrypt
from pathsixgames.forms import RegistrationForm, LoginForm, UpdateEmailForm, PostForm, PostImageForm
from pathsixgames.models import User, Post, GalleryImage
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from PIL import Image

from PIL import Image

def save_image(image_file):
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(current_app.root_path, 'static/images', filename)

    # Open and resize the image using Pillow
    image = Image.open(image_file)
    max_width = 300
    max_height = 300
    image.thumbnail((max_width, max_height))
    
    # Convert image to RGB if needed
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Save image
    image.save(filepath, optimize=True, quality=85)

    # Check and enforce the 10-image limit
    enforce_gallery_limit()

    return filename

def enforce_gallery_limit():
    # Count current images
    image_count = GalleryImage.query.count()

    if image_count > 10:
        # Get the oldest image
        oldest_image = GalleryImage.query.order_by(GalleryImage.date_uploaded.asc()).first()
        
        if oldest_image:
            # Delete image file from static/images
            image_path = os.path.join(current_app.root_path, 'static/images', oldest_image.image)
            if os.path.exists(image_path):
                os.remove(image_path)

            # Remove database reference
            db.session.delete(oldest_image)
            db.session.commit()



@app.route('/')
def index():
    images = GalleryImage.query.all()  # Fetch all gallery images
    latest_post = Post.query.order_by(Post.date_posted.desc()).first()  # Get latest post
    
    # Extract first paragraph
    first_paragraph = None
    if latest_post:
        paragraphs = latest_post.content.split("\n")  # Split content by new lines
        first_paragraph = paragraphs[0] if paragraphs else ""  # Take the first paragraph

    return render_template('index.html', images=images, latest_post=latest_post, first_paragraph=first_paragraph)

@app.route('/dice')
def dice():
    return render_template('dice.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/book1')
def book1():
    posts=Post.query.all()
    return render_template('RoW_book1.html', posts=posts)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    post_form = PostForm()
    image_form = PostImageForm()

    if post_form.validate_on_submit():
        image_filename = None
        if post_form.image.data:
            image_filename = save_image(post_form.image.data)

        post = Post(
            title=post_form.title.data,
            content=post_form.content.data,
            image=image_filename,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('dashboard'))

    if image_form.validate_on_submit():
        image_filename = save_image(image_form.image.data)
        gallery_image = GalleryImage(image=image_filename)
        db.session.add(gallery_image)
        db.session.commit()
        flash('Image uploaded to gallery!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', post_form=post_form, image_form=image_form)

@app.route('/register', methods=['GET', 'POST']) 
def register():
    if current_user.is_authenticated:
        return redirect(url_for('book1'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created , please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login' , methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('book1'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('book1'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Your email has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('account.html', form=form)

@app.route('/gallery')
def gallery():
    images = GalleryImage.query.all()
    return render_template('index.html', images=images)
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, abort
from pathsixgames import db
from pathsixgames.posts.forms import PostForm, PostImageForm
from pathsixgames.models import Post, GalleryImage
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from pathsixgames.posts.utils import save_image 
import os

posts = Blueprint('posts', __name__)

@posts.route("/book1")
def book1():
    order = request.args.get('order', 'newest')
    if order == 'oldest':
        posts = Post.query.order_by(Post.date_posted.asc()).all()
    else:  # defaults to newest
        posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('RoW_book1.html', posts=posts)


@posts.route('/dashboard', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.dashboard'))

    if image_form.validate_on_submit():
        image_filename = save_image(image_form.image.data)
        gallery_image = GalleryImage(image=image_filename)
        db.session.add(gallery_image)
        db.session.commit()
        flash('Image uploaded to gallery!', 'success')
        return redirect(url_for('posts.dashboard'))

    return render_template('post_form.html', post_form=post_form, image_form=image_form, post=None)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    post_form = PostForm()
    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.content = post_form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.book1'))
    elif request.method == 'GET':
        post_form.title.data = post.title
        post_form.content.data = post.content

    return render_template('post_form.html', post_form=post_form, post=post)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # If there's an associated image, delete it from the filesystem
    if post.image:
        image_path = os.path.join(current_app.root_path, 'static/images', post.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete the post from the database
    db.session.delete(post)
    db.session.commit()
    
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('posts.book1'))
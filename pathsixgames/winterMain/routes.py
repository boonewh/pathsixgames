from flask import Blueprint, render_template
from pathsixgames.models import GalleryImage, Post

winterMain = Blueprint('winterMain', __name__)

@winterMain.route('/')
def index():
    images = GalleryImage.query.all()  # Fetch all gallery images
    latest_post = Post.query.order_by(Post.date_posted.desc()).first()  # Get latest post
    
    # Extract first paragraph
    first_paragraph = None
    if latest_post:
        paragraphs = latest_post.content.split("\n")  # Split content by new lines
        first_paragraph = paragraphs[0] if paragraphs else ""  # Take the first paragraph

    return render_template('index.html', images=images, latest_post=latest_post, first_paragraph=first_paragraph)

@winterMain.route('/dice')
def dice():
    return render_template('dice.html')

@winterMain.route('/rules')
def rules():
    return render_template('rules.html')
import os
from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps
from pathsixgames import db
from pathsixgames.models import GalleryImage

def save_image(image_file):
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(current_app.root_path, 'static/images', filename)

    # Open the image and apply orientation correction
    image = Image.open(image_file)
    image = ImageOps.exif_transpose(image)  # This fixes the orientation

    # Calculate aspect ratio-preserving dimensions
    max_size = (300, 300)
    image.thumbnail(max_size, Image.Resampling.LANCZOS)  # LANCZOS provides better quality
    
    # Convert image to RGB if needed
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Save image with optimization
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
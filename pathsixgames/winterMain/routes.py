from flask import Blueprint, render_template, request, jsonify
from pathsixgames.models import GalleryImage, Post
from .forms import DiceRollForm
from .utils import roll_dice, get_total, clear_results, ROLL_RESULTS

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

@winterMain.route('/rules')
def rules():
    return render_template('rules.html')

@winterMain.route("/dice", methods=["GET", "POST"])
def dice():
    form = DiceRollForm()
    results = {dice: ROLL_RESULTS[dice] for dice in ROLL_RESULTS}
    grand_total = get_total()

    if request.method == "POST":
        # Handle clear action
        if "clear" in request.form:
            clear_results()
            results = {dice: [] for dice in ROLL_RESULTS}
            grand_total = 0
        else:
            # Handle dice rolls
            for dice_type in ROLL_RESULTS.keys():
                if f"roll_{dice_type}" in request.form:
                    num_dice = int(request.form.get(dice_type, 1))
                    roll_dice(dice_type, num_dice)
                    results = {dice: ROLL_RESULTS[dice] for dice in ROLL_RESULTS}
                    grand_total = get_total()
                    break

        # If it's an AJAX request, return JSON
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({
                'results': results,
                'grand_total': grand_total
            })

    # For regular requests, return the full page
    return render_template("dice.html", 
                         form=form, 
                         results=results, 
                         grand_total=grand_total)
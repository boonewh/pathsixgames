from flask import Blueprint, render_template, request, jsonify, session
from pathsixgames.models import GalleryImage, Post
from .forms import DiceRollForm
from .utils import roll_dice, get_grand_total, clear_dice_results, clear_all_results, get_results

winterMain = Blueprint('winterMain', __name__)

@winterMain.route('/')
def index():
    images = GalleryImage.query.all()
    latest_post = Post.query.order_by(Post.date_posted.desc()).first()

    first_paragraph = None
    if latest_post:
        paragraphs = latest_post.content.split("\n")
        first_paragraph = paragraphs[0] if paragraphs else ""

    return render_template('index.html', images=images, latest_post=latest_post, first_paragraph=first_paragraph)


@winterMain.route('/rules')
def rules():
    return render_template('rules.html')


@winterMain.route("/dice", methods=["GET", "POST"])
def dice():
    form = DiceRollForm()

    results = get_results()
    grand_total = get_grand_total()

    if request.method == "POST":
        # Handle clear all results
        if "clear_all" in request.form:
            clear_all_results()
            results = get_results()
            grand_total = 0

        # Clear specific dice
        elif any(f"clear_{dice}" in request.form for dice in results):
            for dice_type in results:
                if f"clear_{dice_type}" in request.form:
                    clear_dice_results(dice_type)
                    break
            results = get_results()
            grand_total = get_grand_total()

        # Roll dice
        elif any(f"roll_{dice}" in request.form for dice in results):
            for dice_type in results:
                if f"roll_{dice_type}" in request.form:
                    num_dice = int(request.form.get(dice_type, 1))
                    roll_dice(dice_type, num_dice)
                    break
            results = get_results()
            grand_total = get_grand_total()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({
                'results': results,
                'grand_total': grand_total,
                'success': True
            })

    return render_template("dice.html", form=form, results=results, grand_total=grand_total)

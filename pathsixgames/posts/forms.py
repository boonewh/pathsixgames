from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from pathsixgames.models import Book
from wtforms.validators import DataRequired



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    book = SelectField('Book', coerce=int)
    submit = SubmitField('Post')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.book.choices = [(book.id, book.title) for book in Book.query.order_by(Book.title).all()]

class PostImageForm(FlaskForm):
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    submit = SubmitField('Upload')
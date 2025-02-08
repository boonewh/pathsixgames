# forms.py
# forms.py
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class DiceRollForm(FlaskForm):
    d4 = IntegerField("Roll d4", validators=[DataRequired(), NumberRange(min=1)], default=1)
    d6 = IntegerField("Roll d6", validators=[DataRequired(), NumberRange(min=1)], default=1)
    d8 = IntegerField("Roll d8", validators=[DataRequired(), NumberRange(min=1)], default=1)
    d10 = IntegerField("Roll d10", validators=[DataRequired(), NumberRange(min=1)], default=1)
    d12 = IntegerField("Roll d12", validators=[DataRequired(), NumberRange(min=1)], default=1)
    d20 = IntegerField("Roll d20", validators=[DataRequired(), NumberRange(min=1)], default=1)
    percentile = IntegerField("Roll Percentile", validators=[DataRequired(), NumberRange(min=1)], default=1)

    roll_d4 = SubmitField("Roll d4")
    roll_d6 = SubmitField("Roll d6")
    roll_d8 = SubmitField("Roll d8")
    roll_d10 = SubmitField("Roll d10")
    roll_d12 = SubmitField("Roll d12")
    roll_d20 = SubmitField("Roll d20")
    roll_percentile = SubmitField("Roll Percentile")
    clear = SubmitField("Clear Results")

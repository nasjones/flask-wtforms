from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, URL, Optional, NumberRange


class AddPetForm(FlaskForm):
    """Form for adding a pet"""
    name = StringField("Pet's Name", validators=[
                       InputRequired(message="Please enter a name")])

    species = SelectField("Pet's Species", choices=[
        ('Dog', 'Dog'), ('Cat', 'Cat'), ('Porcupine', 'Porcupine')])

    photo_url = StringField("Photo URL of the pet", validators=[
                            Optional(), URL(message="Please enter a valid URL")])

    age = IntegerField("Pet's Age", validators=[
                       InputRequired(), NumberRange(min=0, max=30)])

    notes = TextAreaField("Notes about the pet", validators=[Optional()])


class EditPetForm(FlaskForm):
    """Form to edit pet"""
    photo_url = StringField("Photo URL of the pet", validators=[
        URL(message="Please enter a valid URL")])

    notes = TextAreaField("Notes about the pet", validators=[Optional()])

    available = SelectField("Available", choices=[
                            (True, 'True'), ("", 'False')], coerce=bool)

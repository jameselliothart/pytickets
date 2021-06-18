from flask_wtf import FlaskForm
from wtforms.fields.simple import HiddenField, SubmitField, TextAreaField
from .domain import SCHEMA
from wtforms import validators
from wtforms.fields.core import StringField


class CreateTicketForm(FlaskForm):
    summary = StringField(
        'Summary', [validators.Length(min=10, max=SCHEMA['summary'])])
    description = StringField(
        'Description', [validators.Length(max=SCHEMA['description'])])


class CompleteTicketForm(FlaskForm):
    resolution = TextAreaField('Resolution')
    submit = SubmitField('Done!')

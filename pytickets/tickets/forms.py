from flask_wtf import FlaskForm
from .domain import SCHEMA
from wtforms import validators
from wtforms.fields.core import StringField


class CreateTicketForm(FlaskForm):
    summary = StringField(
        'Summary', [validators.Length(min=10, max=SCHEMA['summary'])])
    description = StringField(
        'Description', [validators.Length(max=SCHEMA['description'])])

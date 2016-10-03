# -*- coding: utf-8 -*-

import re
from flask_wtf import FlaskForm
from wtforms import StringField, validators, ValidationError


__author__ = 'sobolevn'
__author__ = 'alex-px'


class BlogPostForm(FlaskForm):
    title = StringField(label='Title', validators=[
        validators.Length(min=4, max=140),
    ])
    text = StringField(label='Article Text', validators=[
        validators.Length(min=10, max=3500),
    ])
    author = StringField(label='Author', validators=[
        validators.Regexp(r'^\S+\s+\S+(\s+\S+)*',
                          message='Must have first name and last name')
    ])

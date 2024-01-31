# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators


class LoginForm(Form):
    username = StringField('Username:', validators=[validators.DataRequired(), validators.Length(min=1, max=30)])
    password = StringField('Password:', validators=[validators.DataRequired(), validators.Length(min=1, max=30)])
    email = StringField('Email:', validators=[validators.optional(), validators.Length(min=0, max=50)])

class CommentForm(Form):
    activeFile = StringField('activeFile:', validators=[validators.DataRequired(), validators.Length(min=1, max=500)])
    selectedText = StringField('selectedText:', validators=[validators.DataRequired(), validators.Length(min=1, max=500)])
    comment = StringField('comment:', validators=[validators.optional(), validators.Length(min=0, max=500)])
    tag = StringField('tag:', validators=[validators.optional(), validators.Length(min=0, max=500)])
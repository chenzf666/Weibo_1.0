# -*- coding: utf-8 -*-
from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email

from ..models.role_model import Role
from ..models.user_model import User


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('自我简介')
    submit = SubmitField('确认')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)], )
    confirmed = BooleanField('确认')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('自我简介')
    submit = SubmitField('确认')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册。')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('已存在用户名')


class PostForm(FlaskForm):
    body = PageDownField("有什么新鲜事想告诉大家?")
    image = FileField("添加图片")
    submit = SubmitField('确认')


class CommentForm(FlaskForm):
    body = PageDownField('', validators=[DataRequired()])
    submit = SubmitField('确认')

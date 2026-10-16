from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class NoteForm(FlaskForm):
    title = StringField(
        'Заголовок', validators=[DataRequired(), Length(max=200)]
    )
    content = TextAreaField('Содержание', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField(
        'Имя пользователя', validators=[DataRequired(), Length(max=80)]
    )
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class FeedbackForm(FlaskForm):
    message = TextAreaField(
        'Сообщение', validators=[DataRequired(), Length(max=1000)]
    )
    submit = SubmitField('Отправить отзыв')

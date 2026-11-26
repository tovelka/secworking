from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class NoteForm(FlaskForm):
    title = StringField(
        'Заголовок', validators=[DataRequired(), Length(max=200)]
    )
    content = TextAreaField('Содержание', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(message='Поле обязательно для заполнения'),
            Length(
                min=3, max=50, message='Имя должно быть от 3 до 50 символов'
            ),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message='Недопустимые символы в имени пользователя',
            ),
        ],
    )
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message='Недопустимые символы в имени пользователя',
            ),
        ],
    )
    password = PasswordField(
        'Пароль', validators=[DataRequired(), Length(min=6)]
    )
    submit = SubmitField('Зарегистрироваться')


class FeedbackForm(FlaskForm):
    message = TextAreaField(
        'Сообщение', validators=[DataRequired(), Length(max=1000)]
    )
    submit = SubmitField('Отправить отзыв')

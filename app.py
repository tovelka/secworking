import psycopg
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
    abort,
    flash,
)
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_wtf.csrf import CSRFProtect

from config import Config
from database import db
from models import Note, User
from schemas import NoteForm, LoginForm, RegisterForm, FeedbackForm


app = Flask(__name__)

app.secret_key = Config.SECRET_KEY

csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql+psycopg://{Config.DB_USER}:{Config.DB_PASSWORD}'
    f'@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}'
)
db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = (
    'Пожалуйста, войдите в систему для доступа к этой странице.'
)

with app.app_context():
    db.create_all()

mydb = psycopg.connect(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    dbname=Config.DB_NAME,
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def index():
    form = NoteForm()
    feedback_form = FeedbackForm()
    notes = Note.query.filter_by(user_id=current_user.id)
    return render_template(
        'index.html', notes=notes, form=form, feedback_form=feedback_form
    )


@app.route('/add', methods=['POST'])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,
        )
        db.session.add(note)
        db.session.commit()
        flash('Заметка добавлена успешно')
        return redirect(url_for('index'))


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        abort(403)

    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Заметка обновлена успешно')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, note=note)


@app.route('/delete/<int:note_id>')
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        abort(403)

    db.session.delete(note)
    db.session.commit()
    flash('Заметка удалена успешно')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует')
            return render_template('register.html', form=form)

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Регистрация прошла успешно. Теперь вы можете войти.')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Вы успешно вошли в систему')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    feedback_text = request.form.get('message')
    if feedback_text:
        flash(f'{current_user.username}, спасибо за ваш отзыв!')
    else:
        flash('Пожалуйста, введите текст отзыва')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

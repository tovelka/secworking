import mysql.connector
from flask import Flask, escape, redirect, render_template, request, url_for

from config import Config


app = Flask(__name__)

mydb = mysql.connector.connect(
    host=Config.DB_HOST,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME,
)


@app.route('/')
def index():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    cursor.close()
    return render_template('index.html', notes=notes)


@app.route('/add', methods=['POST'])
def add_note():
    cursor = mydb.cursor()
    cursor.execute(
        'INSERT INTO notes(title, content) VALUES (%s, %s)',
        (request.form.get('title'), request.form.get('content')),
    )
    mydb.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    cursor = mydb.cursor()
    if request.method == 'POST':
        cursor.execute(
            'UPDATE notes SET title = %s, content = %s WHERE id = %s',
            (request.form['title'], request.form['content'], note_id),
        )
        mydb.commit()
        cursor.close()
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM notes WHERE id = %s', (note_id,))
    note = cursor.fetchone()
    cursor.close()
    return render_template('edit.html', note=note)


@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    cursor = mydb.cursor()
    cursor.execute('DELETE FROM notes WHERE id = %s', (note_id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    username = escape(request.form['username'])
    feedback = escape(request.form['feedback'])
    return f'Отзыв получен: {feedback} от {username}'


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

DB_NAME = 'membros.db'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
""
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS membros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_game TEXT NOT NULL,
            numero_real TEXT NOT NULL,
            local TEXT NOT NULL,
            recrutador TEXT NOT NULL,
            imagem1 TEXT,
            imagem2 TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome_game = request.form['nome_game']
        numero_real = request.form['numero_real']
        local = request.form['local']
        recrutador = request.form['recrutador']

        imagem1 = request.files.get('imagem1')
        imagem2 = request.files.get('imagem2')

        filename1 = None
        filename2 = None

        if imagem1 and allowed_file(imagem1.filename):
            filename1 = secure_filename(imagem1.filename)
            imagem1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

        if imagem2 and allowed_file(imagem2.filename):
            filename2 = secure_filename(imagem2.filename)
            imagem2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO membros (nome_game, numero_real, local, recrutador, imagem1, imagem2)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome_game, numero_real, local, recrutador, filename1, filename2))
        conn.commit()
        conn.close()

        return redirect('/')

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM membros ORDER BY id ASC')
    membros = c.fetchall()
    conn.close()

    return render_template('index.html', membros=membros)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = 'gestão de usuarios'
    usuarios = [
        {"nome": "Guilherme", "membroativo": True},
        {"nome": "Zé", "membroativo": False},
        {"nome": "Carlo", "membroativo": False},
        {"nome": "jinjin", "membroativo": True},
    ]
    return render_template('indexx.html', title=title, usuarios=usuarios)

app.run(debug=True)
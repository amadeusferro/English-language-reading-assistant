from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/app')
def application():
    return render_template('app.html')

app.run(debug=True)
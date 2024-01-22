from flask import Flask, url_for, render_template, redirect, send_file
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../BACK/')))
from app import en_reading_assistant, generateDownloadList

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    return redirect(url_for('application'))

@app.route('/application')
def application():
    file_path = "pdfs/example2.pdf"
    my_book = en_reading_assistant(file_path)
    generateDownloadList(my_book)
    counter = 0
    return render_template('app.html', my_book=my_book, counter=counter)

@app.route('/download-list')
def download_list():
    file_path = "../Vocabulary List.txt"
    return send_file(file_path,
                     as_attachment=True,
                     download_name='Vocabulary_List.txt',
                     mimetype='text/plain')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
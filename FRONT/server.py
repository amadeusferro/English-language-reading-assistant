from flask import Flask, url_for, render_template, redirect, send_file, request
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
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file and file.filename.endswith('.pdf'):
        pdfs_directory = 'pdfs'
        if not os.path.exists(pdfs_directory):
            os.makedirs(pdfs_directory)

        file_path = os.path.join(pdfs_directory, 'uploaded_file.pdf')
        file.save(file_path)
        return redirect(url_for('application', file_path=file_path))
    else:
        return redirect(url_for('index'))


@app.route('/application')
def application():
    file_path = request.args.get('file_path', 'pdfs/example2.pdf')
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


@app.errorhandler(Exception)
def handle_error(error):
    return render_template('error.html', error_message=str(error))


if __name__ == "__main__":
    app.run(debug=True)
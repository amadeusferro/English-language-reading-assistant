from flask import Flask, url_for, render_template, redirect
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../BACK/')))
from app import en_reading_assistant, downloadList

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
    downloadList(my_book)
    counter = 0
    return render_template('app.html', my_book=my_book, counter=counter)

app.run(debug=True)

#principal (main)
# def main():
#     file_path = "pdfs/example.pdf"
#     my_book = app.en_reading_assistant(file_path)
#     app.downloadList(my_book)

# if __name__ == "__main__":
#     main()
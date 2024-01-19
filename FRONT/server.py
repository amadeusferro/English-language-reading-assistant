from flask import Flask, url_for, render_template
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../BACK/')))
from app import en_reading_assistant, downloadList

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/application')
def application():
    file_path = "pdfs/example2.pdf"
    my_book = en_reading_assistant(file_path)
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
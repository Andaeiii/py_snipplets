import os  # to handles the files
import hashlib  # to hashstrings...
from flask import Flask, render_template, url_for, request, redirect


from werkzeug.utils import secure_filename
from time import sleep
from flask import copy_current_request_context
import threading  # for large files...
import datetime


__author__ = 'Andaeiii'

app = Flask(__name__)

# ~ get_directory_name_of ( the_absolute_path_of ( thisfile ))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template('upload.html')

# helper functions new filenames...


def mkFileName(filename):
    # string..encode('utf-8') - encoded before hashing...
    return str(datetime.datetime.now().timestamp()) + '_' + filename


# for simple file upload...

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')  # folder stored in images....
    print(target)

    # if the folder does not exists...
    if not os.path.isdir(target):
        os.mkdir(target)  # makeit..

    filesArray = request.files.getlist("imgfile")

    for file in filesArray:
        print(file)
        filename = mkFileName(file.filename)

        destination = '/'.join([target, filename])
        print(destination)

        file.save(destination)

    return render_template('complete.html')


# for large file upload...
@app.route('/upload_large', methods=['POST', 'GET'])
def uploadLargeFiles():
    @copy_current_request_context
    def save_file(closeAfterWrite):
        print(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S') + " i am doing")
        f = request.files['vidfile']
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(
            basepath, 'images/', secure_filename(mkFileName(f.filename)))
        f.save(upload_path)
        closeAfterWrite()
        print(datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S') + " write done")

    def passExit():
        pass

    if request.method == 'POST':
        f = request.files['vidfile']
        normalExit = f.stream.close
        f.stream.close = passExit
        t = threading.Thread(target=save_file, args=(normalExit,))
        t.start()
        return redirect(url_for('uploadLargeFiles'))

    return render_template('complete.html')


if __name__ == '__main__':  # to ensure that the app is run on its own.
    app.run(port=4555, debug=True)

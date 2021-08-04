import os  # to handles the files
from flask import Flask, render_template, url_for, request

__author__ = 'Andaeiii'

app = Flask(__name__)

# ~ get_directory_name_of ( the_absolute_path_of ( thisfile ))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template('upload.html')


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
        filename = file.filename

        destination = '/'.join([target, filename])
        print(destination)

        file.save(destination)

    return render_template('complete.html')


if __name__ == '__main__':  # to ensure that the app is run on its own.
    app.run(port=4555, debug=True)

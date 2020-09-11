import os
from flask import (
    Blueprint, current_app,
    flash, redirect, request,
    url_for, send_from_directory)
from werkzeug.utils import secure_filename

# FILES
bp = Blueprint(
    "uploads", __name__,
    url_prefix='/uploads')


def allowed_file(filename):
    return '.' in filename \
        and filename.rsplit('.', 1)[1].lower() \
        in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        pdf = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if pdf.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if pdf and allowed_file(pdf.filename):
            filename = secure_filename(pdf.filename)
            savepath = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            pdf.save(savepath)

            return redirect(
                url_for('uploads.uploaded_file', filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@bp.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'], filename)

import os
from flask import (
    Blueprint, current_app,
    redirect, request,
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


@bp.route('/', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part'

    pdf = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if pdf.filename == '':
        return 'No selected file'

    if pdf and allowed_file(pdf.filename):
        filename = secure_filename(pdf.filename)
        savepath = os.path.join(
            current_app.config['UPLOAD_FOLDER'], filename)
        pdf.save(savepath)
        # DB call???(filename)
        """
        return redirect(
            url_for(
                'uploaded_file',
                filename=filename))
        """
        return filename
    return 'File not allowed.'


@bp.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        filename)
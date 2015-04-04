from flask import request, send_from_directory
from werkzeug import secure_filename
from sleepypuppy import app, csrf_protect
import os
from PIL import Image

# Only allow png extensions, which is the filetype we generate using HTML5 canvas.
ALLOWED_EXTENSIONS = set(['png'])

def allowed_file(filename):
    """
    Method to filter out bad filenames and prevent dir traversal.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@csrf_protect.exempt
@app.route('/up', methods=['GET', 'POST'])
def upload_file():
    """
    Store filename by timestamp and resize file for thumbnail.
    """
    size = 256, 256
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Prevent dir traversal/NUL byte injection
            filename = secure_filename(file.filename)

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(app.config['UPLOAD_FOLDER'] + '/small_' + filename, "PNG")
    return ""

@app.route('/up/<filename>')
def uploaded_file(filename):
    """
    Route to retrieve screenshot when requested.
    """
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )

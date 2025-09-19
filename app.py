from flask import Flask, request, render_template, send_file, flash, redirect, url_for
import os
import tempfile
from werkzeug.utils import secure_filename
from epub_converter import convert_epub
import shutil

app = Flask(__name__)
app.secret_key = 'epub_converter_secret_key_2024'

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'epub'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file = request.files['file']
        output_format = request.form.get('format', 'txt')

        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            try:
                # Save uploaded file
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Convert the file
                output_file = convert_epub(filepath, output_format, app.config['OUTPUT_FOLDER'])

                # Clean up uploaded file
                os.remove(filepath)

                # Get just the filename for display
                output_filename = os.path.basename(output_file)

                return render_template('result.html',
                                     filename=output_filename,
                                     format=output_format.upper())

            except Exception as e:
                # Clean up uploaded file if it exists
                if 'filepath' in locals() and os.path.exists(filepath):
                    os.remove(filepath)

                flash(f'Error converting file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload an EPUB file.')
            return redirect(request.url)

    return render_template('index.html')


@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            flash('File not found')
            return redirect(url_for('upload_file'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}')
        return redirect(url_for('upload_file'))


@app.route('/cleanup')
def cleanup_files():
    """Clean up old files"""
    try:
        # Clean uploads folder
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Clean outputs folder
        for filename in os.listdir(app.config['OUTPUT_FOLDER']):
            file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        flash('Files cleaned up successfully')
    except Exception as e:
        flash(f'Error cleaning up files: {str(e)}')

    return redirect(url_for('upload_file'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, request
from werkzeug.utils import secure_filename
import os

from file_processor import set_output

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def allowed_file(filename):
    """Check if the uploaded file is a PDF."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'document' not in request.files:
        return redirect(url_for('home'))
    
    document = request.files['document']

    if document.filename == '':
        return redirect(url_for('home'))

    if not allowed_file(document.filename):
        return redirect(url_for('home'))
    
    filename = secure_filename(document.filename)
    document_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    document.save(document_path)

    # Process the document and render the results
    content_blocks = set_output(filename)
    return render_template('result.html', content_blocks=content_blocks, filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve the uploaded file from the uploads directory."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

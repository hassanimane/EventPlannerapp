# server.py
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the upload folder (inside the static directory)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/event/<name>', methods=['GET', 'POST'])
def event(name):
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Save the file securely
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Redirect to refresh the page after upload
            return redirect(url_for('event', name=name))
    
    # List all uploaded images
    image_files = os.listdir(app.config['UPLOAD_FOLDER'])
    # Create relative paths for each image (to be used in the template)
    images = [os.path.join('static', 'uploads', image) for image in image_files]
    return render_template('event.html', name=name, images=images)

if __name__ == '__main__':
    # Listen on all interfaces so your app is accessible locally and via port forwarding
    app.run(host='0.0.0.0', port=5000)

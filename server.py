import os
import qrcode
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure the upload folder for image uploads
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the uploaded file's extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    """
    This route lets the event planner input an event name.
    It then generates an event URL (with 'lng=eng' as a query parameter)
    and creates a QR code from that URL.
    """
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        if not event_name:
            return redirect(request.url)
        
        # Generate the event URL with a query parameter for language
        event_url = url_for('event', name=event_name, lng='eng', _external=True)
        
        # Generate a QR Code for the event URL
        qr = qrcode.make(event_url)
        qr_filename = f"qr_{secure_filename(event_name)}.png"  # Example: qr_MyWedding.png
        qr_filepath = os.path.join('static', qr_filename)
        qr.save(qr_filepath)
        
        return render_template('qr_result.html', event_url=event_url, qr_filename=qr_filename)
    return render_template('create_event.html')

@app.route('/event/<name>', methods=['GET', 'POST'])
def event(name):
    """
    This route is for guests who scan the QR code.
    It displays event details and an upload form for photos.
    """
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('event', name=name))
    
    image_files = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [os.path.join('static', 'uploads', image) for image in image_files]
    return render_template('event.html', name=name, images=images)

if __name__ == '__main__':
    # For compatibility with deployment platforms (e.g., Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

import os
import qrcode
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the uploaded file's extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/event/<name>', methods=['GET', 'POST'])
def event(name):
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

@app.route('/generate_qr', methods=['GET', 'POST'])
def generate_qr():
    """Generate a QR code for the entered event URL."""
    if request.method == 'POST':
        event_url = request.form.get('event_url')
        qr = qrcode.make(event_url)
        qr_path = os.path.join('static', 'generated_qr.png')
        qr.save(qr_path)
        return render_template('qr_result.html', qr_path=qr_path)
    return render_template('generate_qr.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Ensure compatibility with Render
    app.run(host='0.0.0.0', port=port)

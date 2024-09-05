from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from PIL import Image
import os

# Create an instance of the Flask class
app = Flask(__name__)

# Configuration for file upload and thumbnail storage
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Directory for uploaded images
app.config['THUMBNAIL_FOLDER'] = 'static/thumbnails/'  # Directory for thumbnails
app.secret_key = 'your_secret_key'  # Secret key for flashing messages

# Ensure the upload and thumbnail directories exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['THUMBNAIL_FOLDER']):
    os.makedirs(app.config['THUMBNAIL_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle both GET and POST requests for the index route
    if request.method == 'POST':
        # Check if an image was uploaded
        if 'image' not in request.files or request.files['image'].filename == '':
            # No image selected, flash a message and reload the page
            flash('No image selected. Please upload an image to convert.')
            return render_template('index.html')

        # Get the uploaded image and desired format
        image = request.files['image']
        format = request.form['format']
        if image:
            filename = image.filename
            file_ext = os.path.splitext(filename)[1]  # Get file extension
            base_filename = os.path.splitext(filename)[0]  # Get base filename
            new_filename = f"{base_filename}.{format}"  # New filename with desired format
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)  # Full path for saving the image
            image.save(file_path)  # Save the uploaded image

            # Create a thumbnail of the image
            with Image.open(file_path) as img:
                img.thumbnail((200, 200))  # Resize to thumbnail dimensions
                thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], new_filename)  # Path for thumbnail
                img.save(thumbnail_path)  # Save the thumbnail

            # Render the result page with the converted image and thumbnail
            return render_template('result.html', converted_image=new_filename, thumbnail_path=f'thumbnails/{new_filename}')
    
    # Render the index page for GET requests
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Serve the uploaded file for download
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

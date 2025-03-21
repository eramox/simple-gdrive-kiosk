from flask import Flask, jsonify, send_from_directory, abort
from flask_cors import CORS, cross_origin
import os
import yaml
import random

# Configuration
IMAGE_FOLDER = os.path.abspath('images')  # Folder containing your images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
TRIGGER_REFRESH = os.path.join(IMAGE_FOLDER, 'refresh')
SLIDESHOW_FILE = os.path.join(IMAGE_FOLDER, 'slideshow.yaml')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Ensure the image folder exists
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Track the images we've sent to implement looping
class ImageTracker:
    def __init__(self):
        self.images = []
        self.duration = {}
        self.current_index = 0
        self.refresh_images()
    
    def refresh_images(self):

        app.logger.info("Refreshing slideshow")

        self.images = []
        self.duration = {}
    
        with open(SLIDESHOW_FILE) as slideshow:
            data = yaml.safe_load(slideshow)['slideshow']

            if data:
                self.images = [ list(e)[0] for e in data ]
                app.logger.info(f"{self.images=}")
                self.duration = {}
                for e in data:
                    self.duration.update(e)
                app.logger.info(f"{self.duration=}")

        self.current_index = 0

    def get_next_image(self):

        # If the file 'refresh' exists, refresh the list
        if os.path.exists(TRIGGER_REFRESH):
            self.refresh_images()
            os.remove(TRIGGER_REFRESH)

        if self.current_index >= len(self.images):
            # Reset to beginning of the loop
            self.current_index = 0
        
        image = self.images[self.current_index]
        self.current_index += 1
        return image

# Initialize the image tracker
image_tracker = ImageTracker()

@app.route('/get_image')
@cross_origin()
def get_image():
    """Endpoint to get the next image in the rotation"""

    image_name = image_tracker.get_next_image()
    
    if not image_name:
        return jsonify({'error': 'No images found in the folder'}), 404
    
    # Return the URL to the image
    return jsonify({'name': f'{image_name}'})

@app.route('/get_duration/<filename>')
@cross_origin(origin='*')
def serve_duration(filename):
    """Serve the duration for the image"""
    try:
        duration = image_tracker.duration[filename]
    except TypeError as te:
        app.logger.error(f"Failed to retrieve duration for '{filename}' from {image_tracker.duration}: {te}")
        return abort(500)

    return jsonify({'duration': f'{duration}'})

@app.route('/images/<filename>')
@cross_origin(origin='*')
def serve_image(filename):
    """Serve the image file"""
    return send_from_directory(IMAGE_FOLDER, filename)

# Serve the HTML page
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    print(f"Starting server. Images will be served from the '{IMAGE_FOLDER}' folder.")
    print(f"Found {len(image_tracker.images)} images.")
    app.run(debug=True)

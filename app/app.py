from flask import Flask, render_template, request, send_file, abort
import os
from urllib.parse import unquote

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'images')

image_names = {
    'Ash.jpg': 'Ash',
    'Mello.jpg': 'Mello',
    'Bob.jpg': 'Bob'
}

@app.route('/')
def index():
    images = list(image_names.items())
    return render_template('index.html', images=images)


@app.route('/image')
def view_image():
    img = request.args.get('img', '')
    img = unquote(img)
    sanitized_img = img.replace('../', '')

    image_name = image_names.get(sanitized_img, sanitized_img)
    
    return render_template('image.html', img=sanitized_img, name=image_name)


@app.route('/image/content')
def serve_image():
    img = request.args.get('img', '')

    file_path = os.path.join(IMAGES_DIR, img)

    if os.path.exists(file_path):
        return send_file(file_path)
    
    abort(404, description='Invalid')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)

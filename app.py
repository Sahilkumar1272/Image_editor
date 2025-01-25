# Importing necessary libraries
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from PIL import Image, ImageFilter, ImageEnhance
from shutil import copyfile
import os
import glob

# Function to get an image
def get_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print('Unable to load image')


# Function to duplicate an image
def duplicate_image(image_path, options):
    if options == 'copy':
        copyfile(image_path, image_path + '.copy')
    elif options == 'replace':
        copyfile(image_path + '.copy', image_path)


# Default slider values
def default_slider():
    return {'color': 1, 'bright': 1, 'contrast': 1, 'sharp': 1}


# Function to get image size
def image_size(image):
    return image.width, image.height


# Applying enhancers to an image
def apply_enhancers(image, image_path, slider):
    colorer = ImageEnhance.Color(image)
    image = colorer.enhance(slider['color'])
    brighter = ImageEnhance.Brightness(image)
    image = brighter.enhance(slider['bright'])
    contraster = ImageEnhance.Contrast(image)
    image = contraster.enhance(slider['contrast'])
    sharper = ImageEnhance.Sharpness(image)
    image = sharper.enhance(slider['sharp'])

    image.save(image_path)


# Finding dominant colors in an image
def dominant_colors(image_path, colors_count=5):
    image = get_image(image_path)
    width, height = image_size(image)
    colors = image.getcolors(maxcolors=width * height)
    return sorted(colors, reverse=True)[:colors_count]


# BLUR function
def blur(image_path, options):
    image = get_image(image_path)

    if options == "0":
        image = image.filter(ImageFilter.BLUR)
    elif options == "1":
        image = image.filter(ImageFilter.BoxBlur(1))
    elif options == "2":
        image = image.filter(ImageFilter.GaussianBlur)

    image.save(image_path)


# SHARPEN function
def sharpen(image_path, options):
    image = get_image(image_path)

    if options == "0":
        image = image.convert("L")
    elif options == "1":
        threshold=100
        image = image.convert('L')  # Convert the image to grayscale
        image = image.point(lambda x: 0 if x < threshold else 255, '1') # Convert to black and white
    elif options == "2":
        image = image.filter(ImageFilter.DETAIL)
    elif options == "3":
        image = image.filter(ImageFilter.UnsharpMask)

    image.save(image_path)


# ROTATE function
def rotate(image_path, angle):
    image = get_image(image_path)
    image = image.rotate(angle)
    image.save(image_path)


# RESIZE function
def resize(image_path, width, height):
    image = get_image(image_path)
    image = image.resize((width, height), Image.BICUBIC)
    image.save(image_path)


# CROP function
def crop(image_path, start_x, start_y, end_x, end_y):
    image = get_image(image_path)
    image = image.crop((start_x, start_y, end_x, end_y))
    image.save(image_path)


# Function to clear data
def clear_data():
    CLEANUP_FOLDER = os.getcwd() + '/static/*'
    items = glob.glob(CLEANUP_FOLDER)
    for item in items:
        if os.path.isfile(item):
            os.remove(item)



# Configuration variables
UPLOAD_FOLDER = os.getcwd() + '/static'  # Define the upload folder path
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])  # Define the set of allowed file extensions
INPUT_FILENAME = ''  # Initialize the input filename variable



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Global variables for image processing
image, slider = None, None
colors = []
width, height = 0, 0

# Function to refresh parameters after image processing
def refresh_parameters(image_path):
    global image, slider, hue_angle, colors, width, height
    image = get_image(image_path)
    slider = default_slider()
    width, height = image_size(image)
    colors = dominant_colors(image_path)


# Ensure no caching
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route('/', methods=['GET', 'POST'])
def home():
    global INPUT_FILENAME
    clear_data()

    if request.method == 'POST':
        submit_button = request.form.get('submit_button')

        if submit_button == 'upload_image':
            # check if the post request has the file part
            if 'file' not in request.files:
                return redirect(request.url)

            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return redirect(request.url)

            if file and allowed_file(file.filename):
                INPUT_FILENAME = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME))
                duplicate_image(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), 'copy')
                refresh_parameters(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME))
                return redirect(url_for('uploaded'))

    return render_template('home.html')


@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
    global image, slider

    if INPUT_FILENAME:
        if request.method == 'POST':
            # Nav
            original_button = request.form.get('original_button')
            download_button = request.form.get('download_button')
            # Sliders
            enhance_button = request.form.get('enhance_button')
            # Filters
            blur_button = request.form.get('blur_button')
            sharpen_button = request.form.get('sharpen_button')
            # Rotate/resize/crop
            rotate_button = request.form.get('rotate_button')
            resize_button = request.form.get('resize_button')
            crop_button = request.form.get('crop_button')

            if original_button:
                duplicate_image(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), 'replace')
            if download_button:
                return send_file(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), as_attachment=True)

            if enhance_button:
                slider = {key: float(request.form.get(key)) for key, value in slider.items()}
                apply_enhancers(image, os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), slider)
            

            if blur_button:
                blur(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), blur_button)
            elif sharpen_button:
                sharpen(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), sharpen_button)
            

            if rotate_button:
                angle = int(request.form.get('angle'))
                rotate(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), angle)
            elif resize_button:
                n_width = int(request.form.get('width'))
                n_height = int(request.form.get('height'))
                resize(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), n_width, n_height)
            elif crop_button:
                start_x = int(request.form.get('start_x'))
                start_y = int(request.form.get('start_y'))
                end_x = int(request.form.get('end_x'))
                end_y = int(request.form.get('end_y'))
                crop(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME), start_x, start_y, end_x, end_y)

            if any([original_button, blur_button, sharpen_button, rotate_button, resize_button, crop_button]):
                refresh_parameters(os.path.join(UPLOAD_FOLDER, INPUT_FILENAME))

        return render_template('uploaded.html', slider=slider, colors=colors, width=width, height=height, filename=INPUT_FILENAME)
    else:
        return render_template('uploaded.html', slider=slider)


if __name__ == "__main__":
    app.run(debug=True)

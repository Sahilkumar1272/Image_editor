# Image Editor

This is a Flask-based image processing web application that allows users to upload, enhance, and manipulate images through various tools like color adjustment, brightness, contrast, sharpness, blur, sharpen, rotate, resize, and crop. The application also provides the ability to download the processed image or reset it to its original state.

## Features

- **Upload Image**: Users can upload images in supported formats (PNG, JPEG, JPG).
- **Enhance Image**: Users can adjust color, brightness, contrast, and sharpness using sliders.
- **Apply Filters**: Blur or sharpen the image using different filter options.
- **Transformations**: Rotate, resize, and crop the image.
- **Download Image**: Users can download the processed image.
- **Reset Image**: Restore the image to its original state.
- **View Image Information**: Displays the image size and dominant colors.

## Technologies Used

- **Backend**: Flask (Python)
- **Image Processing**: Pillow (PIL)
- **File Handling**: werkzeug for file handling and Flask for routing
- **Frontend**: HTML, CSS (for basic layout and styling)

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask
- Pillow
- werkzeug

### Installation

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/Sahilkumar1272/Image_editor.git
2. Install the required dependencies using `pip`.

  ```bash
    pip install -r requirements.txt

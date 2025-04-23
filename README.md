# Python Image Filtering Application

A powerful and user-friendly image filtering application built with Python. This desktop application allows you to apply various filters and transformations to your images with an intuitive interface.

## Features

### Core Features
- **Image Upload & Viewing**
  - Upload from local drive (supports JPG, PNG, BMP, and more)
  - Drag & drop support (requires TkinterDnD2 library)
  - Display original image
  - Reset to original option

- **Filter Options** Drag & drop support
  - Display original image
  - Reset to original option

- **Filter Options**
  - Grayscale
  - Sepia
  - Negative
  - Black & White Threshold
  - Brightness / Contrast
  - Sharpen / Blur
  - Edge Detection
  - Color Inversion
  - Vignette / Vintage look
  - Saturation adjustments

- **Basic Editing Tools**
  - Crop
  - Rotate (90°, 180°, 270°)
  - Flip (horizontal/vertical)
  - Zoom in/out (for preview)

- **Exporting & Saving**
  - Save processed image with custom filename
  - Format options (JPG, PNG, WebP)
  - Quality/Compression settings
  - Option to save before & after side by side

## Installation

### Prerequisites
- Python 3.6 or higher
- Dependencies:
  - tkinter (usually comes with Python)
  - Pillow (PIL)
  - NumPy
  - OpenCV (cv2)
  - TkinterDnD2 (for drag and drop functionality)

### Setup

1. Clone or download this repository to your local machine.

2. Install the required dependencies:
   ```
   pip install pillow numpy opencv-python tkinterdnd2
   ```

3. Run the application:
   ```
   python image_filter_app.py
   ```

## Usage

### Loading Images
- Click the "Upload Image" button to select an image from your computer
- You can also drag and drop images onto the application window

### Applying Filters
1. Select the desired filter from the tabs on the left panel
2. Click on a filter button or adjust sliders to apply effects
3. You can combine multiple filters and adjustments

### Editing Images
- Use the rotation and flip buttons to transform your image
- Click the "Crop" button and then drag to select the area you want to keep

### Saving Your Work
- Enter a filename in the export options section
- Select the desired format (PNG, JPEG, WebP)
- Adjust quality settings if needed
- Click "Save Image" to save your edited image
- Use "Save Before/After" to create a side-by-side comparison image

## Project Structure

- `image_filter_app.py` - Main application code

## Development

### Technical Stack
- **Frontend/UI**: Tkinter (Python's standard GUI toolkit)
- **Image Processing**: 
  - PIL/Pillow for basic image operations
  - OpenCV for advanced filters
  - NumPy for numerical operations

### Adding New Filters
To add a new filter, you would:
1. Create a new method in the `ImageFilterApp` class
2. Add a button in the appropriate tab in the UI
3. Connect the button to your new filter method

## License

This software is open-source. Feel free to modify and distribute as needed.

## Credits

Created based on requirements for an image filtering application with Python. Uses Tkinter for the UI and PIL/OpenCV for image processing.
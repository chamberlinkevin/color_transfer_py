# ColorTransferPy

ColorTransferPy is a Python library that allows you to transfer the color attributes (Hue, Saturation, Lightness) from one image to another. It uses the Pillow and OpenCV libraries to achieve this.

## Features

- Extracts HSL (Hue, Saturation, Lightness) values from a source image.
- Applies the extracted HSL values to a target image.
- Saves the modified image with the color attributes of the source image.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/chamberlinkevin/ColorTransferPy.git
    ```

2. Navigate to the project directory:
    ```bash
    cd ColorTransferPy
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Example Script

Create a Python script to use the library. Here is an example script:

```python
from ColorTransferPy import transfer_image_colors

source_image_path = 'source.jpg'
target_image_path = 'target.jpg'
output_image_path = 'output.jpg'

transfer_image_colors(source_image_path, target_image_path, output_image_path)

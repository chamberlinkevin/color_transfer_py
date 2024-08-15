from check_and_install_requirements import check_and_install_requirements

check_and_install_requirements()

from PIL import Image
import cv2
import numpy as np
import colorsys

def image_to_hsl(image_path):
    image = Image.open(image_path)
    pixels = list(image.getdata())
    hsl_pixels = [colorsys.rgb_to_hls(*[x/255.0 for x in pixel]) for pixel in pixels]
    return hsl_pixels

def hsl_to_image(hsl_pixels, size):
    rgb_pixels = [tuple(int(x * 255) for x in colorsys.hls_to_rgb(*pixel)) for pixel in hsl_pixels]
    image = Image.new('RGB', size)
    image.putdata(rgb_pixels)
    return image

def standardize_array(array):
    """Standardizes the input array by scaling to zero mean and unit variance."""
    mean = np.mean(array, axis=(0, 1), keepdims=True)
    std = np.std(array, axis=(0, 1), keepdims=True)
    standardized_array = (array - mean) / (std + 1e-8)  # Add a small epsilon to avoid division by zero
    return standardized_array

def transfer_image_colors(source_image_path, target_image_path, output_image_path):
    # Read source and target images
    source_image = cv2.imread(source_image_path)
    target_image = cv2.imread(target_image_path)

    if source_image is None or target_image is None:
        raise FileNotFoundError("One of the image files was not found or could not be read.")

    # Convert images to float32 for precision
    source_image = source_image.astype(np.float32) / 255.0
    target_image = target_image.astype(np.float32) / 255.0

    # Convert source image to HLS
    source_hls = cv2.cvtColor(source_image, cv2.COLOR_BGR2HLS)
    
    # Extract H, L, and S channels from source image
    source_h, source_l, source_s = cv2.split(source_hls)

    # Convert target image to HLS
    target_hls = cv2.cvtColor(target_image, cv2.COLOR_BGR2HLS)

    # Standardize the HLS channels of the target image
    target_hls_standardized = standardize_array(target_hls)

    # Compute mean and std of source HLS channels
    source_mean = np.mean(source_hls, axis=(0, 1), keepdims=True)
    source_std = np.std(source_hls, axis=(0, 1), keepdims=True)

    # Standardize the source HLS channels
    source_hls_standardized = standardize_array(source_hls)

    # Transfer color characteristics
    transferred_hls = source_hls_standardized * source_std + source_mean
    transferred_hls = np.clip(transferred_hls, 0, 1)  # Clip to valid range

    # Convert back to BGR color space
    transferred_image = cv2.cvtColor(transferred_hls, cv2.COLOR_HLS2BGR)

    # Convert image back to uint8
    transferred_image = (transferred_image * 255.0).astype(np.uint8)

    # Save the output image
    cv2.imwrite(output_image_path, transferred_image)

if __name__ == "__main__":
    # Example usage
    source_image_path = 'source.jpg'
    target_image_path = 'target.jpg'
    output_image_path = 'output.jpg'
    transfer_image_colors(source_image_path, target_image_path, output_image_path)

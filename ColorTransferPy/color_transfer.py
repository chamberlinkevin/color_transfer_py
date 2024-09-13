from check_and_install_requirements import check_and_install_requirements

check_and_install_requirements()

from PIL import Image
import cv2
import numpy as np
import colorsys

def standardize_array(array):
    """Standardizes the input array by scaling to zero mean and unit variance."""
    mean = np.mean(array, axis=(0, 1), keepdims=True)
    std = np.std(array, axis=(0, 1), keepdims=True)
    standardized_array = (array - mean) / (std + 1e-8)  # Add a small epsilon to avoid division by zero
    return standardized_array

def transfer_image_colors(source_image_path, target_image_path, output_image_path):
    """Transfers color characteristics from target image to source image."""
    # Load images
    source_image = cv2.imread(source_image_path)
    target_image = cv2.imread(target_image_path)

    if source_image is None or target_image is None:
        raise FileNotFoundError("One of the image files was not found or could not be read.")
    
    # Convert images to float32 for precision
    source_image = source_image.astype(np.float32) / 255.0
    target_image = target_image.astype(np.float32) / 255.0

    # Convert images from BGR to HLS color space
    source_hls = cv2.cvtColor(source_image, cv2.COLOR_BGR2HLS)
    target_hls = cv2.cvtColor(target_image, cv2.COLOR_BGR2HLS)

    # Separate the H, L, S channels
    source_hue, source_lightness, source_saturation = cv2.split(source_hls)
    target_hue, target_lightness, target_saturation = cv2.split(target_hls)

    # Standardize lightness and saturation, but NOT hue
    source_lightness_standardized = standardize_array(source_lightness)
    source_saturation_standardized = standardize_array(source_saturation)

    # Get mean and std of target lightness and saturation
    target_lightness_mean = np.mean(target_lightness, axis=(0, 1), keepdims=True)
    target_lightness_std = np.std(target_lightness, axis=(0, 1), keepdims=True)

    target_saturation_mean = np.mean(target_saturation, axis=(0, 1), keepdims=True)
    target_saturation_std = np.std(target_saturation, axis=(0, 1), keepdims=True)

    # Apply target's mean and std to standardized source lightness and saturation
    transferred_lightness = source_lightness_standardized * target_lightness_std + target_lightness_mean
    transferred_saturation = source_saturation_standardized * target_saturation_std + target_saturation_mean

    # Clip lightness and saturation to valid range (0-255)
    transferred_lightness = np.clip(transferred_lightness, 0, 255)
    transferred_saturation = np.clip(transferred_saturation, 0, 255)

    # Combine transferred H, L, S
    transferred_hls = cv2.merge((source_hue, transferred_lightness, transferred_saturation))

    # Convert back to BGR color space
    transferred_image = cv2.cvtColor(transferred_hls.astype(np.float32), cv2.COLOR_HLS2BGR)

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

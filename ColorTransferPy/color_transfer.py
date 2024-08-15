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

def transfer_image_colors(source_image_path, target_image_path, output_image_path):
    # Read source and target images
    source_image = cv2.imread(source_image_path)
    target_image = cv2.imread(target_image_path)

    # Convert source image to HLS
    source_hls = cv2.cvtColor(source_image, cv2.COLOR_BGR2HLS)
    
    # Extract H, L, and S channels from source image
    source_h, source_l, source_s = cv2.split(source_hls)

    # Convert target image to HLS
    target_hls = cv2.cvtColor(target_image, cv2.COLOR_BGR2HLS)

    # Replace target H, L, and S channels with those from the source image
    target_hls[:, :, 0] = source_h
    target_hls[:, :, 1] = source_l
    target_hls[:, :, 2] = source_s

    # Convert back to BGR
    output_image = cv2.cvtColor(target_hls, cv2.COLOR_HLS2BGR)

    # Save the output image
    cv2.imwrite(output_image_path, output_image)

if __name__ == "__main__":
    # Example usage
    source_image_path = 'source.jpg'
    target_image_path = 'target.jpg'
    output_image_path = 'output.jpg'
    transfer_image_colors(source_image_path, target_image_path, output_image_path)

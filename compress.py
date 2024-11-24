from PIL import Image  # Importing the Python Imaging Library (Pillow)

def compress_image(input_path, output_path, max_width, max_height):
    """
    Compresses an image to fit within the specified dimensions while maintaining its aspect ratio.
    Ensures minimal quality degradation for the output image.

    Parameters:
        input_path (str): The file path of the input image.
        output_path (str): The file path where the compressed image will be saved.
        max_width (int): The maximum width of the resized image.
        max_height (int): The maximum height of the resized image.
    """
    try:
        # Open the input image file
        with Image.open(input_path) as img:
            # Resize the image to fit within the specified dimensions
            # while maintaining the original aspect ratio
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Save the resized image to the specified output path with high quality
            img.save(output_path, quality=95, optimize=True)
            
            # Print success message
            print(f"Image saved to: {output_path} with preserved quality.")
    except Exception as e:
        # Print error message if any issue occurs
        print(f"Error resizing image: {e}")

# Example usage:
# Compress an image located at 'test_images/1640697060491.jpg'
# and save the resized image to 'resized.jpg' with a max size of 2000x2000 pixels
compress_image("test_images/1640697060491.jpg", "resized.jpg", 2000, 2000)

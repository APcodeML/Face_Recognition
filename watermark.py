from PIL import Image

def add_logo_watermark(input_image_path, output_image_path, logo_path, position="bottom-right", opacity=250):
    # Open the input image and logo
    base_image = Image.open(input_image_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    # Resize the logo relative to the input image size
    base_width, base_height = base_image.size
    logo_width, logo_height = logo.size

    # Scale the logo to 10% of the image width
    scale_factor = base_width * 0.1 / logo_width
    new_logo_width = int(logo_width * scale_factor)
    new_logo_height = int(logo_height * scale_factor)
    logo = logo.resize((new_logo_width, new_logo_height), Image.Resampling.LANCZOS)

    # Adjust logo transparency
    logo_with_opacity = Image.new("RGBA", logo.size)
    for x in range(logo.width):
        for y in range(logo.height):
            r, g, b, a = logo.getpixel((x, y))
            logo_with_opacity.putpixel((x, y), (r, g, b, int(a * (opacity / 255))))

    # Determine logo position
    if position == "bottom-right":
        x = base_width - new_logo_width - 10
        y = base_height - new_logo_height - 10
    elif position == "top-left":
        x = 10
        y = 10
    elif position == "top-right":
        x = base_width - new_logo_width - 10
        y = 10
    elif position == "bottom-left":
        x = 10
        y = base_height - new_logo_height - 10
    else:  # Center
        x = (base_width - new_logo_width) // 2
        y = (base_height - new_logo_height) // 2

    # Paste the logo onto the base image
    base_image.paste(logo_with_opacity, (x, y), logo_with_opacity)

    # Save the final image
    if output_image_path.lower().endswith(".jpg") or output_image_path.lower().endswith(".jpeg"):
        base_image = base_image.convert("RGB")  # Convert to RGB mode for JPEG
    base_image.save(output_image_path)

# Example usage
input_image = "test_images/1640697060482.jpg"  # Input image file
output_image = "example_with_logo.jpeg"  # Output file
logo_image = "logo.png"  # Path to your logo
add_logo_watermark(input_image, output_image, logo_image, position="bottom-right", opacity=180)

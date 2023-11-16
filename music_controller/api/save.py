import base64
import imghdr
import io
from PIL import Image


def save_base64_image(query_image, file_path):
    try:
        # Decode base64 data
        binary_data = base64.b64decode(query_image)

        # Check the image format before attempting to open
        img_format = imghdr.what(None, h=binary_data)
        print(img_format)
        if img_format not in ['jpeg', 'png', 'gif', 'bmp', 'webp']:
            raise ValueError("Invalid image format")

        # Open the image using PIL
        img = Image.open(io.BytesIO(binary_data))

        # Save the image to the specified file path
        img.save(file_path)
        print(f"Image saved to: {file_path}")

    except Exception as e:
        print(f"Error saving image: {e}")

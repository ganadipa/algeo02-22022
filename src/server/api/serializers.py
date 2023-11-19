from rest_framework import serializers
from .models import ImageModel
import base64
from PIL import Image
from io import BytesIO



class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('id', 'image', 'uploaded_at')

def base64_to_image(base64_string, output_path):
    if 'base64,' in base64_string:
        base64_string = base64_string.split('base64,')[1]
    
    # Decode the base64 string
    img_data = base64.b64decode(base64_string)
    
    # Convert to image
    img = Image.open(BytesIO(img_data))
    
    # Save the image
    img.save(output_path)

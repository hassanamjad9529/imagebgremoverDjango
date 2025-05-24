from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
from rembg import remove
from PIL import Image
import io
import base64
import requests

IMGBB_API_KEY = '88a44a310032eb395b35940653283f59'  # Replace this with your actual key

class RemoveBackgroundAPIView(APIView):
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            try:
                # Step 1: Convert uploaded image to bytes
                input_image = Image.open(image).convert("RGBA")
                buffered = io.BytesIO()
                input_image.save(buffered, format="PNG")
                img_bytes = buffered.getvalue()

                # Step 2: Remove background
                output_bytes = remove(img_bytes)

                # Step 3: Convert to base64
                output_buffer = io.BytesIO()
                Image.open(io.BytesIO(output_bytes)).save(output_buffer, format='PNG')
                base64_img = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

                # Step 4: Upload to ImgBB
                response = requests.post(
                    'https://api.imgbb.com/1/upload',
                    data={
                        'key': IMGBB_API_KEY,
                        'image': base64_img
                    }
                )

                if response.status_code == 200:
                    image_url = response.json()['data']['url']
                    return Response({
                        "status": "success",
                        "image_url": image_url
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "error",
                        "message": "Failed to upload image to ImgBB",
                        "details": response.text
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({
                    "status": "error",
                    "message": "Image processing failed",
                    "details": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

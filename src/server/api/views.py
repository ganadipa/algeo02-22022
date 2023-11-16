from rest_framework import status
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, ImageModelSerializer
from .models import Room, ImageModel
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import JsonResponse
# include cbir_texture.py in cbir folder
# include CBIR_Algorithm folder
import os
from api.CBIR_Algorithm.CBIR_Texture import similarityTexture
# Create your views here.
from django.conf import settings
import time
import zipfile
from api.CBIR_Algorithm.Driver import getSimiliarity
import shutil
from pathlib import Path
import base64
from django.core.files.base import ContentFile
import io
import base64
from PIL import Image
# from api.save import save_base64_image
from api.serializers import base64_to_image
from api.Web_Scraper.start_scrape import runScrape


class RoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    def post(self, request, format=None):
        try:

            # Check if 'query' and 'dataset' are in the uploaded files
            if 'query' not in request.FILES or 'dataset[0]' not in request.FILES:
                raise ValueError(
                    "Both 'query' and 'dataset' files are required in the request")

            # Get the uploaded query file name

            # Get the uploaded dataset files
            uploaded_query_name = request.FILES['query'].name

            # Process the query file as needed
            # For example, you can save the file to a specific directory
            # Make sure the 'MEDIA_ROOT' and 'MEDIA_URL' settings are configured in your Django project
            # Example:
            # from django.core.files.storage import default_storage
            # from django.core.files.base import ContentFile
            # query_path = default_storage.save('path/to/save/' + uploaded_query_name, ContentFile(request.FILES['query'].read()))

            # Process each uploaded dataset file as needed
            processed_dataset_names = []
            for i in range(len(request.FILES)-1):
                # Here, you can process each dataset file as needed
                # For example, you can save the file to a specific directory
                # Make sure the 'MEDIA_ROOT' and 'MEDIA_URL' settings are configured in your Django project
                # Example:
                # from django.core.files.storage import default_storage
                # from django.core.files.base import ContentFile
                # dataset_path = default_storage.save('path/to/save/' + uploaded_dataset.name, ContentFile(uploaded_dataset.read()))
                processed_dataset_names.append(request.FILES[f'dataset[{i}]'])

            # Include additional request information in the response
            response_data = {
                'uploaded_query_name': uploaded_query_name,
                'processed_dataset_names': processed_dataset_names,
                'method': request.method,
                'headers': dict(request.headers),
                # Add more fields as needed
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # if not self.request.session.exists(self.request.session.session_key):
        #     self.request.session.create()

        # serializer = self.serializer_class(data=request.data)
        # if (serializer.is_valid):
        #     guest_can_pause = serializer.data.guest_can_pause
        #     votes_to_skip = serializer.data.votes_to_skip
        #     host = self.request.session.session_key
        #     queryset = Room.objects.filter(host=host)
        #     if queryset.exists():
        #         room = queryset[0]
        #         room.guest_can_pause = guest_can_pause
        #         room.votes_to_skip = votes_to_skip
        #         room.save(update_field=['guest_can_pause', 'votes_to_skip'])
        #     else:
        #         room = Room(host=host, guest_can_pause=guest_can_pause,
        #                     votes_to_skip=votes_to_skip)
        #         room.save()

        #     return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        # return Response({'Bad Request': 'invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


# class ImageUploadView(APIView):
#     def post(self, request, format=None):
#         try:
#             # Check if 'image' is in the uploaded files
#             if 'image' not in request.FILES:
#                 raise ValueError("No 'image' file in the request")

#             # Save the uploaded image to the model
#             uploaded_image = ImageModel(image=request.FILES['image'])
#             uploaded_image.save()

#             # Serialize the model instance for the response
#             serializer = ImageModelSerializer(uploaded_image)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class ImageUploadView(APIView):
#     parser_classes = (FormParser, MultiPartParser)

#     def post(self, request, format=None):
#         try:
#             # Check if 'query' is in the uploaded files
#             if 'query' not in request.FILES:
#                 raise ValueError("No 'query' file in the request")

#             # Save the query image to the model
#             query_image = ImageModel(image=request.FILES['query'])
#             query_image.save()

#             # Save the dataset images to the model
#             dataset_images = [ImageModel(image=file) for file in request.FILES.getlist('dataset')]
#             ImageModel.objects.bulk_create(dataset_images)

#             # Serialize the model instances for the response
#             query_serializer = ImageModelSerializer(query_image)
#             dataset_serializer = ImageModelSerializer(dataset_images, many=True)

#             return Response({'query_image': query_serializer.data, 'dataset_images': dataset_serializer.data}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class ImageUploadView(APIView):
#     parser_classes = (FormParser, MultiPartParser)

#     def post(self, request, format=None):
#         try:
#             # Save the query image to the local folder
#             query_image = request.FILES['query_image']
#             query_image_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_images', query_image.name)
#             with open(query_image_path, 'wb') as f:
#                 for chunk in query_image.chunks():
#                     f.write(chunk)

#             # Get the path to the dataset folder
#             dataset_folder_path = os.path.join(settings.MEDIA_ROOT, 'dataset_images')

#             # Calculate image similarities
#             similarities = similarityTexture(query_image_path, dataset_folder_path)

#             return Response({'similar_images': similarities}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImageUploadView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    root = os.path.abspath("./") + "\\"

    def image_similarity(query_image_path, dataset_folder_path):
        similarities = []
        for dataset_image_name in os.listdir(dataset_folder_path):
            dataset_image_path = os.path.join(
                dataset_folder_path, dataset_image_name)
            similarity_score = similarityTexture(
                query_image_path, dataset_image_path)
            if similarity_score > 0.6:
                similarities.append(
                    {'image_path': dataset_image_path, 'similarity_score': similarity_score})

        return similarities

    def post(self, request, format=None):
        NUM_THREAD = 10

        start = time.time()
        # try:

        # return JsonResponse({'message': len(request.FILES)}, status=status.HTTP_201_CREATED)

        query_folder_path = os.path.join(
            settings.MEDIA_ROOT, 'uploaded_images')
        for existing_image_name in os.listdir(query_folder_path):
            existing_image_path = os.path.join(
                query_folder_path, existing_image_name)
            os.remove(existing_image_path)
            print(f"Existing query image deleted: {existing_image_path}")

        isTexture = request.POST.get("search_method") == "texture"

        query_image = request.FILES.get('query')
        isScraping = False

        if query_image:
            query_image_path = os.path.join(
                settings.MEDIA_ROOT, 'uploaded_images', query_image.name)
            with open(query_image_path, 'wb') as f:
                for chunk in query_image.chunks():
                    f.write(chunk)
            print(f"Query image saved to: {query_image_path}")
        else:
            # using base64
            query_image = request.POST.get('query')
            query_image_path = os.path.join(
                settings.MEDIA_ROOT, 'uploaded_images', "query.png")
            print(query_image)
            base64_to_image(query_image, query_image_path)
            # img.save(query_image_path)

        dataset_folder_path = Path(settings.MEDIA_ROOT) / 'dataset_images'
        for existing_image_path in dataset_folder_path.iterdir():
            existing_image_path.unlink()
            # print(f"Existing dataset image deleted: {existing_image_path}")

        for i in range(len(request.FILES)-1):
            dataset_image = request.FILES.get(f'dataset[{i}]')
            if dataset_image:
                dataset_image_path = os.path.join(
                    settings.MEDIA_ROOT, 'dataset_images', dataset_image.name)
                with open(dataset_image_path, 'wb') as f:
                    for chunk in dataset_image.chunks():
                        f.write(chunk)
                # print(f"Dataset image saved to: {dataset_image_path}")

        if (isScraping):
            scrapeString = "nyoman"
            limit = 10
            runScrape(scrapeString, limit)

        end = time.time()
        response = getSimiliarity(
            self.root+query_image_path, isTexture, NUM_THREAD)  # MODE TEKSTUR/WARNA
        response.__setitem__("upload_time", end-start)

        # similarities = self.image_similarity(
        #     query_image_path, dataset_folder_path)
        # print(f"Similarities: {similarities}")

        return JsonResponse(response, status=status.HTTP_201_CREATED)
        # except Exception as e:
        #     return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

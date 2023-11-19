from rest_framework import status
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import  ImageModelSerializer
from .models import  ImageModel
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from django.http import JsonResponse

import os
from api.CBIR_Algorithm.CBIR_Texture import similarityTexture

from django.conf import settings
import time

from api.CBIR_Algorithm.Driver import getSimiliarity
import shutil
from pathlib import Path
import base64
from django.core.files.base import ContentFile
import io
import base64
from PIL import Image

from api.serializers import base64_to_image
from api.Web_Scraper.start_scrape import runScrape




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


        query_folder_path = os.path.join(
            settings.MEDIA_ROOT, 'uploaded_images')
        for existing_image_name in os.listdir(query_folder_path):
            existing_image_path = os.path.join(
                query_folder_path, existing_image_name)
            os.remove(existing_image_path)
            print(f"Existing query image deleted: {existing_image_path}")

        isTexture = request.POST.get("search_method") == "texture"

        query_image = request.FILES.get('query')
        print(request.POST.get('scrape'))
        isScraping = request.POST.get(
            'scrape') != "" and request.POST.get('scrape') != None
        print(isScraping)

        if query_image:
            query_image_path = os.path.join(
                settings.MEDIA_ROOT, 'uploaded_images', query_image.name)
            with open(query_image_path, 'wb') as f:
                for chunk in query_image.chunks():
                    f.write(chunk)
            print(f"Query image saved to: {query_image_path}")
        else:
            
            query_image = request.POST.get('query')
            query_image_path = os.path.join(
                settings.MEDIA_ROOT, 'uploaded_images', "query.png")
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

            start = time.time()
            scrapeString = request.POST.get("scrape")
            limit = 3
            runScrape(scrapeString, limit)
            print("done")

        end = time.time()
        response = getSimiliarity(
            self.root+query_image_path, isTexture, NUM_THREAD, isScraping)  # MODE TEKSTUR/WARNA
        response.__setitem__("upload_time", end-start)


        return JsonResponse(response, status=status.HTTP_201_CREATED)


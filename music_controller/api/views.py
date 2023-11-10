from rest_framework import status
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer,ImageModelSerializer
from .models import Room, ImageModel
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
# Create your views here.


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


class ImageUploadView(APIView):
    def post(self, request, format=None):
        try:
            # Check if 'image' is in the uploaded files
            if 'image' not in request.FILES:
                raise ValueError("No 'image' file in the request")

            # Save the uploaded image to the model
            uploaded_image = ImageModel(image=request.FILES['image'])
            uploaded_image.save()

            # Serialize the model instance for the response
            serializer = ImageModelSerializer(uploaded_image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework import status
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class RoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    def post(self, request, format=None):
        try:
            # Check if 'image' is in the uploaded files
            if 'image' not in request.FILES:
                raise ValueError("No 'image' file in the request")

            # Get the uploaded image file name
            uploaded_image_name = request.FILES['image'].name

            # Include additional request information
            response_data = {
                'uploaded_image_name': uploaded_image_name,
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

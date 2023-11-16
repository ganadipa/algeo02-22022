from django.urls import path
from .views import RoomView, CreateRoomView,ImageUploadView

urlpatterns = [
    path('room', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view()),
    path('upload-image/', ImageUploadView.as_view(), name='image-upload'),
    # path('scraping/', ScrapingView.as_view())
]

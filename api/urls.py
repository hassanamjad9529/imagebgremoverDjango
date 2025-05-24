from .views import RemoveBackgroundAPIView
from django.urls import path

urlpatterns = [
    path('remove-background/', RemoveBackgroundAPIView.as_view(), name='remove-background'),
]
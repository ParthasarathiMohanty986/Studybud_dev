from django.urls import path
from . import views

urlpatterns = [  # Corrected spelling
    path('', views.getRoutes),  # Maps the root of the API to the getRoutes view
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
]

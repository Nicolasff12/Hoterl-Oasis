from django.urls import path, include
from rest_framework import routers
from hotel_oasis import views

router = routers.DefaultRouter()
router.register(r'cities', views.CitiesView, basename='cities')  # Update this line

urlpatterns = [
    path("api/", include(router.urls)),  # Keep the trailing slash
]
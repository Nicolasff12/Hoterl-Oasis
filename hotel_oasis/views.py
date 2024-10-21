from rest_framework import viewsets
from .serializers import CitiesSerializer
from .models import Cities

# Create your views here.
class CitiesView(viewsets.ModelViewSet):
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer
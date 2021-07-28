from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, generics, permissions
from .models import *
from rest_framework.permissions import IsAuthenticated

class koordinatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Koordinat
        fields =  ['segmen', 'longitude','lat', 'alt']

class KoordinatViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Koordinat.objects.all()
    serializer_class = koordinatSerializer


# Create your views here.

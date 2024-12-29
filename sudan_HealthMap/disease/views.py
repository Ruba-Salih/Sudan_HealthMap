from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Disease
from .serializers import DiseaseSerializer

class DiseaseListAPIView(APIView):
    """
    API view to list all diseases.
    """
    def get(self, request):
        diseases = Disease.objects.all()
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

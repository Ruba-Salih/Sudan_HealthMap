from rest_framework import serializers
from disease.serializers import DiseaseSerializer
from supervisor.serializers import HospitalSerializer, StateSerializer
from case.serializers import CaseSerializer
from .models import DiseaseStatistics

class DiseaseStatisticsSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()
    disease = DiseaseSerializer()
    case_details = CaseSerializer(many=True)

    class Meta:
        model = DiseaseStatistics
        fields = ['id', 'hospital', 'disease', 'cases', 'deaths', 'date_reported', 'case_details']
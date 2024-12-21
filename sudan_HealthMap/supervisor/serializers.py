from rest_framework import serializers
from disease.models import Disease

class DiseaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Disease model.
    Converts Disease model instances to JSON and validates input data.
    """
    class Meta:
        model = Disease
        fields = ['id', 'name', 'description', 'created_by']
        read_only_fields = ['id', 'created_by']  # Prevent 'id' and 'created_by' from being modified

from rest_framework import serializers
from hospital.models import Hospital
from disease.models import Disease

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'state', 'username', 'password', 'supervisor']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        hospital = Hospital(**validated_data)
        hospital.set_password(password)
        hospital.save()
        return hospital
    

class DiseaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Disease model.
    Converts Disease model instances to JSON and validates input data.
    """
    class Meta:
        model = Disease
        fields = ['id', 'name', 'description', 'created_by']
        read_only_fields = ['id', 'created_by']

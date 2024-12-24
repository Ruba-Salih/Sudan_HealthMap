from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.response import Response
from state.models import State
from hospital.models import Hospital
from disease.models import Disease

class HospitalSerializer(serializers.ModelSerializer):

    state_name = serializers.ReadOnlyField(source='state.name')

    class Meta:
        model = Hospital
        fields = ['id', 'name', 'state', 'state_name', 'username', 'password', 'supervisor']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Override create method to hash the password before saving.
        """
        password = validated_data.pop('password', None)
        hospital = Hospital(**validated_data)
        if password:
            hospital.password = make_password(password)  # Hash the password
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


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from state.models import State
from hospital.models import Hospital
from disease.models import Disease
from supervisor.models import Supervisor


class HospitalSerializer(serializers.ModelSerializer):
    state_name = serializers.ReadOnlyField(source='state.name')

    class Meta:
        model = Hospital
        fields = ['id', 'name', 'state', 'state_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Override create method to hash the password and assign a supervisor.
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("A logged-in supervisor is required to create a hospital.")

        supervisor = request.user
        print(f"Supervisor assigned: {supervisor}")
        # Assign the supervisor to the hospital
        validated_data['supervisor'] = supervisor

        # Hash the password before saving
        password = validated_data.pop('password', None)
        hospital = Hospital(**validated_data)
        if password:
            hospital.password = make_password(password)

        # Save the hospital object
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

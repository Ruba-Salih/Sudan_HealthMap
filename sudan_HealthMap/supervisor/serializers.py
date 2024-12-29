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
        fields = ['id', 'name', 'state', 'state_name', 'username', 'password', 'supervisor']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Override create method to hash the password and assign a supervisor.
        """
        email = validated_data.get('username')

        # Check if the supervisor with this email already exists
        supervisor = Supervisor.objects.filter(email=email).first()
        if not supervisor:
            # Create a new supervisor if it doesn't exist
            supervisor = Supervisor.objects.create_user(
                email=email,
                name=validated_data.get('name'),
                password=validated_data.pop('password'),
                role='hospital',
            )

        # Associate the supervisor with the hospital
        validated_data['supervisor'] = supervisor
        validated_data['user'] = supervisor

        # Hash the password before saving the hospital
        password = validated_data.pop('password', None)
        hospital = Hospital(**validated_data)
        if password:
            hospital.password = make_password(password)
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

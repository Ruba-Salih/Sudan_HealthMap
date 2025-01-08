from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Hospital

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

        validated_data['supervisor'] = supervisor

        password = validated_data.pop('password', None)
        hospital = Hospital(**validated_data)
        if password:
            hospital.password = make_password(password)

        hospital.save()

        return hospital

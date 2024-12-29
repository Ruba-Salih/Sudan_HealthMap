from rest_framework import serializers
from disease.serializers import DiseaseSerializer
from .models import Case

class CaseSerializer(serializers.ModelSerializer):

    disease = DiseaseSerializer(read_only=True)

    class Meta:
        model = Case
        fields = '__all__'
        extra_kwargs = {'hospital': {'read_only': True}}
    
    def create(self, validated_data):
        user = self.context['request'].user
        print(f"User Role in Serializer: {user.role}")
        validated_data['hospital'] = user.hospitals.first()  # Fetch hospital from user
        return super().create(validated_data)

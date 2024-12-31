from rest_framework import serializers
from hospital.models import Hospital
from disease.models import Disease
from .models import Case

class CaseSerializer(serializers.ModelSerializer):

    disease = serializers.PrimaryKeyRelatedField(queryset=Disease.objects.all())
    disease_name = serializers.CharField(source="disease.name", read_only=True)

    class Meta:
        model = Case
        fields = '__all__'
        extra_kwargs = {'hospital': {'read_only': True}}

    def create(self, validated_data):

        user = self.context['request'].user
        print(f"Logged-in User in Serializer: {user} ({user.role})")

        hospital = Hospital.objects.filter(email=user.email).first()
        print(f"Associated Hospital in Serializer: {hospital}")

        if not hospital:
            raise serializers.ValidationError("No associated hospital from serializers")

        validated_data['hospital'] = hospital

        return super().create(validated_data)

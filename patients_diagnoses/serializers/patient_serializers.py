from rest_framework import serializers
from ..models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'  # O lista explícita si quieres: ['id', 'name', ...]

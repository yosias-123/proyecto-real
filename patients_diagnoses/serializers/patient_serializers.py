from rest_framework import serializers
from ..models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'  
class SearchPatientsRequest(serializers.Serializer):
    document_number = serializers.CharField(required=False, allow_blank=True, max_length=20)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)
    sex = serializers.ChoiceField(choices=['M', 'F'], required=False)
    region = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False, min_value=1)
    per_page = serializers.IntegerField(required=False, min_value=1, max_value=100)

    def validate(self, attrs):
        return attrs
from rest_framework import generics
from ..models import Patient
from ..serializers import PatientSerializer
from ..pagination import PatientPagination

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.filter(deleted_at__isnull=True)
    serializer_class = PatientSerializer
    pagination_class = PatientPagination

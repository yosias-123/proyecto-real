from rest_framework.views import APIView
from rest_framework.response import Response
from patients_diagnoses.serializers.PatientService import PatientService

class PatientController(APIView):
    
    def get(self, request):
        """
        Lista paginada de pacientes (index)
        """
        data = PatientService.getPaginated(request)
        return Response(data)
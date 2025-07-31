from django.core.paginator import Paginator
from django.db.models import Q
from patients_diagnoses.models import Patient
from patients_diagnoses.serializers.patient_serializers import PatientSerializer
from patients_diagnoses.serializers.search_serializers import SearchPatientsRequest


class PatientService:

    @staticmethod
    def getPaginated(request):
        patients = Patient.objects.all().order_by('id')
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('per_page', 10)

        paginator = Paginator(patients, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = PatientSerializer(page_obj, many=True)

        return {
            'current_page': page_obj.number,
            'data': serializer.data,
            'first_page_url': f"{request.path}?page=1",
            'from': page_obj.start_index(),
            'last_page': paginator.num_pages,
            'last_page_url': f"{request.path}?page={paginator.num_pages}",
            'links': PatientService.build_links(request, paginator, page_obj),
            'next_page_url': f"{request.path}?page={page_obj.next_page_number()}" if page_obj.has_next() else None,
            'path': request.build_absolute_uri().split('?')[0],
            'per_page': int(page_size),
            'prev_page_url': f"{request.path}?page={page_obj.previous_page_number()}" if page_obj.has_previous() else None,
            'to': page_obj.end_index(),
            'total': paginator.count
        }

    @staticmethod
    def build_links(request, paginator, page_obj):
        current_page = page_obj.number
        last_page = paginator.num_pages
        links = []

        # Prev
        links.append({
            'url': f"{request.path}?page={current_page - 1}" if page_obj.has_previous() else None,
            'label': '« Previous',
            'active': False
        })

        # Pages
        for i in range(1, min(last_page, 10) + 1):
            links.append({
                'url': f"{request.path}?page={i}",
                'label': str(i),
                'active': (i == current_page)
            })

        if last_page > 10:
            links.append({'url': None, 'label': '...', 'active': False})
            links.append({'url': f"{request.path}?page={last_page - 1}", 'label': str(last_page - 1), 'active': False})
            links.append({'url': f"{request.path}?page={last_page}", 'label': str(last_page), 'active': False})

        # Next
        links.append({
            'url': f"{request.path}?page={current_page + 1}" if page_obj.has_next() else None,
            'label': 'Next »',
            'active': False
        })

        return links

    @staticmethod
    def searchByTerm(queryset, term):
        return queryset.filter(
            Q(name__icontains=term) |
            Q(paternal_lastname__icontains=term) |
            Q(maternal_lastname__icontains=term) |
            Q(document_number__icontains=term)
        )

    @staticmethod
    def searchPatients(request):
        serializer = SearchPatientsRequest(data=request.GET)
        serializer.is_valid(raise_exception=True)
        term = serializer.validated_data.get('term', '')
        queryset = Patient.objects.all().order_by('id')

        if term:
            queryset = PatientService.searchByTerm(queryset, term)

        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('per_page', 10)

        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = PatientSerializer(page_obj, many=True)

        return {
            'current_page': page_obj.number,
            'data': serializer.data,
            'first_page_url': f"{request.path}?page=1",
            'from': page_obj.start_index(),
            'last_page': paginator.num_pages,
            'last_page_url': f"{request.path}?page={paginator.num_pages}",
            'links': PatientService.build_links(request, paginator, page_obj),
            'next_page_url': f"{request.path}?page={page_obj.next_page_number()}" if page_obj.has_next() else None,
            'path': request.build_absolute_uri().split('?')[0],
            'per_page': int(page_size),
            'prev_page_url': f"{request.path}?page={page_obj.previous_page_number()}" if page_obj.has_previous() else None,
            'to': page_obj.end_index(),
            'total': paginator.count
        }
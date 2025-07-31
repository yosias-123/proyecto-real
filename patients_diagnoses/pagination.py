# pacientes_diagnosticos/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class PatientPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'current_page': self.page.number,
            'data': data,
            'first_page_url': self.get_first_page_url(),
            'from': self.page.start_index(),
            'last_page': self.page.paginator.num_pages,
            'last_page_url': self.get_last_page_url(),
            'links': self.build_links(),
            'next_page_url': self.get_next_link(),
            'path': self.request.build_absolute_uri(self.request.path),
            'per_page': self.get_page_size(self.request),
            'prev_page_url': self.get_previous_link(),
            'to': self.page.end_index(),
            'total': self.page.paginator.count,
        })

    def get_first_page_url(self):
        return self.request.build_absolute_uri('?page=1')

    def get_last_page_url(self):
        last_page = self.page.paginator.num_pages
        return self.request.build_absolute_uri(f'?page={last_page}')

    def build_links(self):
        current = self.page.number
        last = self.page.paginator.num_pages
        links = []

        # Previous
        links.append({
            'url': self.get_previous_link(),
            'label': '« Previous',
            'active': False,
        })

        # Pages 1-10
        for i in range(1, min(last + 1, 11)):
            links.append({
                'url': self.request.build_absolute_uri(f'?page={i}'),
                'label': str(i),
                'active': i == current,
            })

        # "..." y últimas páginas
        if last > 10:
            links.append({'url': None, 'label': '...', 'active': False})
            links.append({'url': self.request.build_absolute_uri(f'?page={last-1}'), 'label': str(last - 1), 'active': False})
            links.append({'url': self.request.build_absolute_uri(f'?page={last}'), 'label': str(last), 'active': False})

        # Next
        links.append({
            'url': self.get_next_link(),
            'label': 'Next »',
            'active': False,
        })

        return links

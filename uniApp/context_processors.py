from django.urls import reverse, resolve
from university.models import University
from django.conf import settings


def breadcrumb(request):
    breadcrumb_items = [{'title': 'Home', 'url': reverse('home')}]

    resolver_match = resolve(request.path)
    current_view = resolver_match.view_name

    if current_view == 'university_detail':
        university_id = resolver_match.kwargs.get('pk') 
        try:
            university = University.objects.get(pk=university_id)
            MAX_NAME_LENGTH = 20  

            if university.name and len(university.name) > MAX_NAME_LENGTH and university.abbreviation:
                display_name = university.abbreviation
            else:
                display_name = university.name

            # Append 'Institutions' and the current university
            breadcrumb_items.append({'title': 'Institutions', 'url': reverse('search-page')})
            breadcrumb_items.append({'title': display_name, 'url': ''})  # Current page; no URL
        except University.DoesNotExist:
            # Fallback to default breadcrumb generation
            path = request.path.strip('/').split('/')
            titles = {
                '': 'Home',
                'institutions': 'Institutions',
                'about': 'About Us',
                'contact': 'Contact Us',
                'search-page': 'Search Page',
                'courses': 'Courses',
                'faculties': 'Faculties',
                'departments': 'Departments',
                'programs': 'Programs',
                'students': 'Students',
                'staff': 'Staff',
                'admissions': 'Admissions',
                'research': 'Research',
                'news': 'News',
                'events': 'Events',
                'library': 'Library',
                'profile': 'Profile',
                'settings': 'Settings',
            }

            current_url = ''
            for segment in path:
                current_url += f'/{segment}'
                title = titles.get(segment, segment.replace('-', ' ').title())
                breadcrumb_items.append({
                    'title': title,
                    'url': current_url
                })

    else:
        # Standard breadcrumb generation based on path segments
        path = request.path.strip('/').split('/')
        titles = {
            '': 'Home',
            'institutions': 'Institutions',
            'about': 'About Us',
            'contact': 'Contact Us',
            'search-page': 'Search Page',
            'courses': 'Courses',
            'faculties': 'Faculties',
            'departments': 'Departments',
            'programs': 'Programs',
            'students': 'Students',
            'staff': 'Staff',
            'admissions': 'Admissions',
            'research': 'Research',
            'news': 'News',
            'events': 'Events',
            'library': 'Library',
            'profile': 'Profile',
            'settings': 'Settings',
        }

        current_url = ''
        for segment in path:
            current_url += f'/{segment}'
            title = titles.get(segment, segment.replace('-', ' ').title())
            breadcrumb_items.append({
                'title': title,
                'url': current_url
            })

    return {'breadcrumb': breadcrumb_items}
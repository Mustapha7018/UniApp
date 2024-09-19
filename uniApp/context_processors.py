from django.urls import resolve, reverse
from django.apps import apps

def breadcrumb(request):
    path = request.path.strip('/').split('/')
    breadcrumb_items = []

    titles = {
        '': 'Home',
        'institutions': 'Universities',
        'about': 'About Us',
        'contact': 'Contact Us',
        'search-page': 'Search page',
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

    # Add the home breadcrumb item
    breadcrumb_items.append({
        'title': 'Home',
        'url': reverse('home')
    })

    current_url = ''
    for segment in path:
        current_url += f'/{segment}'
        title = titles.get(segment, segment.replace('-', ' ').title())
        breadcrumb_items.append({
            'title': title,
            'url': current_url
        })

    return {'breadcrumb': breadcrumb_items}
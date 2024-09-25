from django.views.generic import ListView, DetailView
from .models import University, Location  
from django.db.models import Q

class UniversityListView(ListView):
    model = University
    template_name = 'pages/search_page.html'
    context_object_name = 'universities'
    paginate_by = 10

    def get_queryset(self):
        queryset = University.objects.all()
        search_query = self.request.GET.get('search', '').strip()
        sort_by = self.request.GET.get('sort', 'name')
        filter_type = self.request.GET.get('type', '')
        filter_location = self.request.GET.get('location', '')
        self.search_performed = bool(search_query or filter_type or filter_location)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(region__icontains=search_query)
            )

        if filter_type:
            if filter_type == 'Private':
                filter_type = 'PRI'
            elif filter_type == 'Public':
                filter_type = 'PUB'
            queryset = queryset.filter(type=filter_type)

        if filter_location:
            queryset = queryset.filter(location__name=filter_location)

        if sort_by == 'A-Z':
            queryset = queryset.order_by('name')
        elif sort_by == 'Z-A':
            queryset = queryset.order_by('-name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_performed'] = self.search_performed
        context['locations'] = Location.objects.all()  
        return context

class UniversityDetailView(DetailView):
    model = University
    template_name = 'pages/institution.html'
    context_object_name = 'university'

    def get_queryset(self):
        return super().get_queryset().select_related('location').prefetch_related(
            'academic_programs',
            'general_requirements',
            'resources'
        )
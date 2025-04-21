import django_filters
from .models import Workspace
from django.db.models import Q

class WorkspaceFilter(django_filters.FilterSet):
    amenities = django_filters.CharFilter(method='filter_amenities')
    location = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Workspace
        fields = ['location', 'is_available', 'workspace_type', 'min_capacity', 'max_capacity']

    def filter_amenities(self, queryset, name, value):
        amenities_list = [v.strip() for v in value.split(',')]
        for amenity_name in amenities_list:
            queryset = queryset.filter(amenities__name__icontains=amenity_name)
        return queryset

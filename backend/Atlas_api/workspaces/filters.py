# filters.py
import django_filters
from .models import Workspace

class WorkspaceFilter(django_filters.FilterSet):
    amenities = django_filters.CharFilter(method='filter_by_amenity_name')
    location = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Workspace
        fields = ['location', 'is_available', 'workspace_type', 'min_capacity', 'max_capacity']

    def filter_by_amenity_name(self, queryset, name, value):
        return queryset.filter(amenities__name__icontains=value)

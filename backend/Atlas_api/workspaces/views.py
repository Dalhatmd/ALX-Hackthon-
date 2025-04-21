from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Workspace, Amenity, WorkspaceType
from .serializers import (
    WorkspaceListSerializer,
    WorkspaceDetailSerializer,
    WorkspaceCreateUpdateSerializer,
    AmenitySerializer,
    WorkspaceTypeSerializer,
)
from .filters import WorkspaceFilter


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users with OWNER type to create workspaces.
    """
    def has_permission(self, request, view):
        # Allow all read-only requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for OWNER type users
        return request.user and hasattr(request.user, 'user_type') and request.user.user_type == request.user.UserType.OWNER


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.AllowAny]


class WorkspaceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkspaceType.objects.all()
    serializer_class = WorkspaceTypeSerializer
    permission_classes = [permissions.AllowAny]


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = WorkspaceFilter
    search_fields = ['name', 'description', 'location', 'address']
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return WorkspaceListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return WorkspaceCreateUpdateSerializer
        return WorkspaceDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """
        Check workspace availability for specific date/time range
        """
        workspace = self.get_object()
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        
        if not start_time or not end_time:
            return Response(
                {"error": "Both start_time and end_time query parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from django.utils.dateparse import parse_datetime
            start_dt = parse_datetime(start_time)
            end_dt = parse_datetime(end_time)
            
            if not start_dt or not end_dt:
                return Response(
                    {"error": "Invalid datetime format. Use ISO format (YYYY-MM-DDThh:mm:ss)"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            is_available = workspace.is_available_during(start_dt, end_dt)
            return Response({"is_available": is_available})
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


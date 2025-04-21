from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Booking
from .serializers import BookingSerializer, AdminBookingSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAdminOrTeamLeaderOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if user.is_team_leader():
            return obj.user in request.user.team_members.all()
        return obj.user == request.user




class BookingViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['workspace', 'status', 'start_time', 'end_time']
    search_fields = ['workspace__name', 'notes']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['-start_time']
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeamLeaderOrOwner]
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Admin users can see all bookings
            return Booking.objects.all()
        if user.is_team_leader():
            team_member_ids = user.team_members.values_list('id', flat=True)
            return Booking.objects.filter(user__in=list(team_member_ids) + [user.id])
        # Regular users can only see their own bookings
        return Booking.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminBookingSerializer
        return BookingSerializer
    
    
    def perform_create(self, serializer):
        user = self.request.user

        # If staff, they can specify user freely
        if user.is_staff and 'user' in self.request.data:
            serializer.save()
            return

        # If team leader, allow booking for team members
        if user.is_team_leader():
            booking_user_id = self.request.data.get('user')
            if booking_user_id:
                try:
                    booking_user = User.objects.get(id=booking_user_id)
                except User.DoesNotExist:
                    raise ValidationError("Invalid user ID")

                # Check if the booking_user is in a team led by current user
                if not team:
                    raise ValidationError("You can only book for your own team members")
                serializer.save(user=booking_user)
                return

        # Regular users — force booking for themselves
        serializer.save(user=user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        
        # Check if booking can be cancelled (only pending or confirmed)
        if booking.status not in [Booking.Status.PENDING, Booking.Status.CONFIRMED]:
            return Response(
                {"error": "Only pending or confirmed bookings can be cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = Booking.Status.CANCELLED
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        
        # Only admin users can confirm bookings
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin users can confirm bookings"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if booking can be confirmed (only pending)
        if booking.status != Booking.Status.PENDING:
            return Response(
                {"error": "Only pending bookings can be confirmed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = Booking.Status.CONFIRMED
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)


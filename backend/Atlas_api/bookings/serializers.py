from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    workspace_name = serializers.ReadOnlyField(source='workspace.name')
    user_email = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'workspace', 'workspace_name', 'user_email',
            'start_time', 'end_time', 'status', 'notes',
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
                'user': {'read_only': True}
                }
        read_only_fields = ['created_at', 'updated_at']
   
    def create (self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def validate(self, data):
        # Validate booking times
        if data.get('end_time') <= data.get('start_time'):
            raise serializers.ValidationError("End time must be after start time")
        
        # Check if workspace is available
        workspace = data.get('workspace')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if not workspace.is_available_during(start_time, end_time):
            raise serializers.ValidationError("Workspace is not available during this time")
        
        # Check for overlapping bookings (excluding current booking if updating)
        instance = self.instance
        instance_id = instance.id if instance else None
        
        overlapping = Booking.objects.filter(
            workspace=workspace,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED]
        ).exclude(pk=instance_id)
        
        if overlapping.exists():
            raise serializers.ValidationError("This booking overlaps with an existing one")
        
        return data


class AdminBookingSerializer(BookingSerializer):
    """
    Serializer for admin users who can book on behalf of others
    """
    class Meta(BookingSerializer.Meta):
        # Admin can specify the user
        read_only_fields = ['created_at', 'updated_at']

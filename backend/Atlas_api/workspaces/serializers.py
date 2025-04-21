# workspaces/serializers.py
from rest_framework import serializers
from .models import Workspace, Amenity, WorkspaceType


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'description', 'icon']


class WorkspaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceType
        fields = ['id', 'name', 'description']


class WorkspaceListSerializer(serializers.ModelSerializer):
    workspace_type = WorkspaceTypeSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    is_open = serializers.SerializerMethodField()
    opening_hours = serializers.SerializerMethodField()
    
    class Meta:
        model = Workspace
        fields = [
            'id', 'name', 'description', 'is_available', 'location',
            'workspace_type', 'amenities', 'price_per_hour',
            'min_capacity', 'max_capacity', 'is_open', 'opening_hours',
            'thumbnail'
        ]
    
    def get_is_open(self, obj):
        return obj.is_open_now()
    
    def get_opening_hours(self, obj):
        return obj.get_opening_hours_display()


class WorkspaceDetailSerializer(WorkspaceListSerializer):
    class Meta(WorkspaceListSerializer.Meta):
        fields = WorkspaceListSerializer.Meta.fields + ['address', 'created_at', 'updated_at']


class WorkspaceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = [
            'name', 'description', 'is_available', 'opening_time', 'closing_time',
            'location', 'address', 'amenities', 'max_capacity', 'min_capacity',
            'workspace_type', 'price_per_hour', 'thumbnail'
        ]
    
    def validate(self, data):
        """
        Check that opening time is before closing time and max capacity > min capacity
        """
        if 'opening_time' in data and 'closing_time' in data:
            if data['opening_time'] >= data['closing_time']:
                raise serializers.ValidationError(
                    {"closing_time": "Closing time must be after opening time"}
                )
        
        if 'max_capacity' in data and 'min_capacity' in data:
            if data['max_capacity'] <= data['min_capacity']:
                raise serializers.ValidationError(
                    {"max_capacity": "Max capacity must be greater than min capacity"}
                )
        
        return data

from rest_framework import serializers
from .models import Workspace, Booking, Notification, WorkspaceUsageReport
from users.models import CustomUser


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    workspace = WorkspaceSerializer(read_only=True)
    workspace_id = serializers.PrimaryKeyRelatedField(
        queryset=Workspace.objects.filter(is_active=True),
        source="workspace",
        write_only=True,
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["status", "created_at", "updated_at"]

    def validate(self, data):
        if data["end_time"] <= data["start_time"]:
            raise serializers.ValidationError("End time must be after start time.")

        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            workspace=data["workspace"],
            start_time__lt=data["end_time"],
            end_time__gt=data["start_time"],
            status="confirmed",
        ).exists()

        if overlapping:
            raise serializers.ValidationError(
                "This workspace is already booked for the selected time."
            )

        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["is_read", "created_at"]


class WorkspaceUsageReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceUsageReport
        fields = "__all__"
        read_only_fields = ["generated_by", "created_at"]

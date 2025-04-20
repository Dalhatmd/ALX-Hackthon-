from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from workspaces.models import Workspace

User = get_user_model()

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        COMPLETED = 'COMPLETED', 'Completed'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    def clean(self):
        """Validate booking times"""
        super().clean()
        
        # Ensure end time is after start time
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")
        
        # Ensure booking is within workspace hours
        if not self.workspace.is_available_during(self.start_time, self.end_time):
            raise ValidationError("Booking outside workspace operating hours")
        
        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            workspace=self.workspace,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk if self.pk else None)
        
        if overlapping.exists():
            raise ValidationError("This booking overlaps with an existing one")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.workspace.name} ({self.start_time} to {self.end_time})"

    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['workspace', 'start_time', 'end_time']),
            models.Index(fields=['user', 'start_time']),
        ]

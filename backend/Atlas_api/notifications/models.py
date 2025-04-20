from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from bookings.models import Booking

User = get_user_model()

class Notification(models.Model):
    class Type(models.TextChoices):
        BOOKING_CREATED = 'BOOKING_CREATED', 'Booking Created'
        BOOKING_CONFIRMED = 'BOOKING_CONFIRMED', 'Booking Confirmed'
        BOOKING_CANCELLED = 'BOOKING_CANCELLED', 'Booking Cancelled'
        BOOKING_REMINDER = 'BOOKING_REMINDER', 'Booking Reminder'
        BOOKING_COMPLETED = 'BOOKING_COMPLETED', 'Booking Completed'
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=50,
        choices=Type.choices
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()
    
    def __str__(self):
        return f"Notification for {self.user.email}: {self.notification_type}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['booking', 'notification_type']),
        ]


# Signal handlers to automatically create notifications
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=Booking)
def create_booking_notification(sender, instance, created, **kwargs):
    """Creates notifications when a booking is created or updated"""
    if created:
        # New booking created
        Notification.objects.create(
            user=instance.user,
            booking=instance,
            notification_type=Notification.Type.BOOKING_CREATED,
            message=f"You've booked {instance.workspace.name} from {instance.start_time.strftime('%Y-%m-%d %H:%M')} to {instance.end_time.strftime('%Y-%m-%d %H:%M')}"
        )
    else:
        # Check if status changed
        if instance.status == Booking.Status.CONFIRMED:
            Notification.objects.create(
                user=instance.user,
                booking=instance,
                notification_type=Notification.Type.BOOKING_CONFIRMED,
                message=f"Your booking for {instance.workspace.name} has been confirmed"
            )
        elif instance.status == Booking.Status.CANCELLED:
            Notification.objects.create(
                user=instance.user,
                booking=instance,
                notification_type=Notification.Type.BOOKING_CANCELLED,
                message=f"Your booking for {instance.workspace.name} has been cancelled"
            )
        elif instance.status == Booking.Status.COMPLETED:
            Notification.objects.create(
                user=instance.user,
                booking=instance,
                notification_type=Notification.Type.BOOKING_COMPLETED,
                message=f"Your booking for {instance.workspace.name} has been completed"
            )


#Function to send booking reminders
def send_booking_reminders():
    """
    Create reminder notifications for upcoming bookings
    This function can be called by a scheduled task (e.g., Celery)
    """
    # Find bookings that are starting within the next 24 hours
    reminder_time = timezone.now() + timezone.timedelta(hours=24)
    upcoming_bookings = Booking.objects.filter(
        status=Booking.Status.CONFIRMED,
        start_time__lte=reminder_time,
        start_time__gte=timezone.now()
    )
    
    for booking in upcoming_bookings:
        # Check if reminder already sent
        reminder_exists = Notification.objects.filter(
            booking=booking,
            notification_type=Notification.Type.BOOKING_REMINDER
        ).exists()
        
        if not reminder_exists:
            Notification.objects.create(
                user=booking.user,
                booking=booking,
                notification_type=Notification.Type.BOOKING_REMINDER,
                message=f"Reminder: You have a booking for {booking.workspace.name} starting at {booking.start_time.strftime('%Y-%m-%d %H:%M')}"
            )

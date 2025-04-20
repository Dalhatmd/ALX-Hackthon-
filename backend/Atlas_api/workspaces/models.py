from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For UI icons

    def __str__(self):
        return self.name


class WorkspaceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Workspace(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="workspaces",
        limit_choices_to={"user_type": User.UserType.OWNER},
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    location = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    max_capacity = models.PositiveIntegerField()
    min_capacity = models.PositiveIntegerField(default=1)
    workspace_type = models.ForeignKey(
        WorkspaceType, on_delete=models.SET_NULL, null=True, blank=True
    )
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to="workspace_thumbnails/", blank=True)

    def clean(self):
        super().clean()
        if self.opening_time and self.closing_time:
            if self.opening_time >= self.closing_time:
                raise ValidationError(
                    {"closing_time": "Closing time must be after opening time"}
                )
        if self.max_capacity <= self.min_capacity:
            raise ValidationError({
                'max_capacity': 'Max capacity must be greater than min capacity'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def is_open_now(self):
        """This implementation utilizes datetime.time as I do not
            expect people to want to work past 6pm and it is easier 
            to test please update to datetime.datetime if I happen to be wrong"""
        from django.utils import timezone

        now = timezone.now().time()
        return self.opening_time <= now <= self.closing_time

    def get_opening_hours_display(self):
        """Format opening hours for display"""
        return f"{self.opening_time.strftime('%I:%M %p')} - {self.closing_time.strftime('%I:%M %p')}"

    def is_available_during(self, start_dt, end_dt):
        """Check if workspace is available during specified datetime range"""
        # Convert datetimes to times for daily schedule check
        start_time = start_dt.time()
        end_time = end_dt.time()
    
        # Check if within operating hours (handles overnight cases)
        if self.opening_time < self.closing_time:
            # Normal hours (e.g., 9AM-5PM)
            if not (self.opening_time <= start_time <= end_time <= self.closing_time):
                return False
        else:
            # Overnight hours (e.g., 10PM-6AM)
            if not ((start_time >= self.opening_time or start_time <= self.closing_time) and
                (end_time >= self.opening_time or end_time <= self.closing_time)):
                return False
    
        # Check for conflicting bookings
        conflicting_bookings = self.bookings.filter(
            start_time__lt=end_dt,
            end_time__gt=start_dt,
            status__in=['Booking.Status.CONFIRMED', 'Booking.Status.PENDING']
        ).exists()
    
        return not conflicting_bookings

    def __str__(self):
        return f"{self.name} - {self.location}"

    class Meta:
        ordering = ["-created_at"]

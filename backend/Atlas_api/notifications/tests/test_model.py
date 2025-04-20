from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from notifications.models import Notification, send_booking_reminders
from bookings.models import Booking
from workspaces.models import Workspace, WorkspaceType
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import time, timedelta

User = get_user_model()

class NotificationTests(TestCase):
    def setUp(self):
        # Create Owner and Client users
        self.owner = User.objects.create_user(
            email='owner@example.com',
            password='password123',
            user_type=User.UserType.OWNER
        )
        self.client = User.objects.create_user(
            email='client@example.com',
            password='password123',
            user_type=User.UserType.GENERAL
        )

        # Create a Workspace Type and Workspace
        self.workspace_type = WorkspaceType.objects.create(name="Private Office")
        self.workspace = Workspace.objects.create(
            owner=self.owner,
            name="Cozy Workspace",
            description="A nice cozy place to work",
            is_available=True,
            opening_time=time(8, 0),
            closing_time=time(18, 0),
            location="Remote City",
            max_capacity=10,
            min_capacity=1,
            workspace_type=self.workspace_type,
            price_per_hour=100.00,
            thumbnail=SimpleUploadedFile("thumb.jpg", b"file_content", content_type="image/jpeg")
        )
        
        self.start_time = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0)
        self.end_time = self.start_time + timedelta(hours=2)

        # Create a Booking
        self.booking = Booking.objects.create(
            user=self.client,
            workspace=self.workspace,
            start_time=self.start_time,
            end_time=self.end_time,
            status=Booking.Status.PENDING
        )

    def test_notification_created_on_booking(self):
        notifications = Notification.objects.filter(booking=self.booking)
        self.assertTrue(notifications.exists())
        self.assertEqual(notifications.first().notification_type, Notification.Type.BOOKING_CREATED)

    def test_notifications_created_on_status_change(self):
        # Confirmed
        self.booking.status = Booking.Status.CONFIRMED
        self.booking.save()
        confirm_notification = Notification.objects.filter(
            booking=self.booking,
            notification_type=Notification.Type.BOOKING_CONFIRMED
        )
        self.assertTrue(confirm_notification.exists())

        # Cancelled
        self.booking.status = Booking.Status.CANCELLED
        self.booking.save()
        cancel_notification = Notification.objects.filter(
            booking=self.booking,
            notification_type=Notification.Type.BOOKING_CANCELLED
        )
        self.assertTrue(cancel_notification.exists())

        # Completed
        self.booking.status = Booking.Status.COMPLETED
        self.booking.save()
        complete_notification = Notification.objects.filter(
            booking=self.booking,
            notification_type=Notification.Type.BOOKING_COMPLETED
        )
        self.assertTrue(complete_notification.exists())

    def test_mark_notification_as_read(self):
        notification = Notification.objects.filter(booking=self.booking).first()
        self.assertFalse(notification.is_read)

        notification.mark_as_read()
        notification.refresh_from_db()

        self.assertTrue(notification.is_read)
        self.assertIsNotNone(notification.read_at)

    def test_send_booking_reminders(self):
        # Set booking to tomorrow morning inside workspace hours
        now = timezone.now()
        tomorrow_morning = (now + timezone.timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)

        self.booking.status = Booking.Status.CONFIRMED
        self.booking.start_time = tomorrow_morning
        self.booking.end_time = tomorrow_morning + timezone.timedelta(hours=2)
        self.booking.save()

        self.assertFalse(Notification.objects.filter(
            booking=self.booking,
            notification_type=Notification.Type.BOOKING_REMINDER
        ).exists())

        # Call reminder function
        send_booking_reminders()

        self.assertTrue(Notification.objects.filter(
            booking=self.booking,
            notification_type=Notification.Type.BOOKING_REMINDER
        ).exists())

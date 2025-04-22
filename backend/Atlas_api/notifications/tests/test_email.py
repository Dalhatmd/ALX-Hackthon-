from django.test import TestCase
from django.core import mail
from django.utils import timezone
from django.contrib.auth import get_user_model

from bookings.models import Booking
from workspaces.models import Workspace, WorkspaceType
from notifications.models import Notification

User = get_user_model()

class NotificationModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            user_type=User.UserType.OWNER
        )

        # Create a workspace type
        self.workspace_type = WorkspaceType.objects.create(
            name="Private Office",
            description="Quiet space"
        )

        # Create a workspace
        self.workspace = Workspace.objects.create(
            owner=self.user,
            name="Test Workspace",
            description="A quiet place to work",
            is_available=True,
            opening_time=timezone.datetime(2024, 1, 1, 9, 0).time(),  # 9:00 AM
            closing_time=timezone.datetime(2024, 1, 1, 17, 0).time(), # 5:00 PM
            location="Test Location",
            max_capacity=10,
            min_capacity=1,
            workspace_type=self.workspace_type,
            price_per_hour=20.00
        )

        # Create a booking
        self.booking = Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            start_time=timezone.now().replace(hour=10, minute=0, second=0, microsecond=0),  # 10:00 AM
            end_time=timezone.now().replace(hour=12, minute=0, second=0, microsecond=0),    # 12:00 PM
            status=Booking.Status.CONFIRMED
        )

    def test_notification_sends_email_on_create(self):
        """Test that creating a notification sends an email"""

        # Clear the outbox before
        mail.outbox = []

        # Create notification
        Notification.objects.create(
            user=self.user,
            booking=self.booking,
            notification_type=Notification.Type.BOOKING_CONFIRMED,
            message="Your booking has been confirmed!"
        )

        # Check that one email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check the subject of the email
        email = mail.outbox[0]
        self.assertIn('Notification: Booking Confirmed', email.subject)
        self.assertEqual(email.to, [self.user.email])
        self.assertTrue(email.alternatives)  # Check that html_message exists

    def test_notification_mark_as_read(self):
        """Test that mark_as_read method works"""
        notification = Notification.objects.create(
            user=self.user,
            booking=self.booking,
            notification_type=Notification.Type.BOOKING_CONFIRMED,
            message="Your booking has been confirmed!"
        )

        self.assertFalse(notification.is_read)
        self.assertIsNone(notification.read_at)

        notification.mark_as_read()

        self.assertTrue(notification.is_read)
        self.assertIsNotNone(notification.read_at)

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, time
from ..models import Booking
from workspaces.models import Workspace
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
TEST_LOCATION = "123 ALX city"

class BookingModelTests(TestCase):
    def setUp(self):
        # Create owner user (must be UserType.OWNER)
        self.owner = User.objects.create_user(
            email='owner@example.com',
            password='testpass123',
            user_type=User.UserType.OWNER
        )
        
        # Create regular user
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        
        # Create valid workspace with all required fields
        self.workspace = Workspace.objects.create(
            owner=self.owner,
            name='Test Workspace',
            description='Test workspace',
            opening_time=time(9, 0),  # 9 AM
            closing_time=time(17, 0), # 5 PM
            location=TEST_LOCATION,
            max_capacity=10,
            min_capacity=1,
            price_per_hour=25.00
        )
        
        # Set up valid booking times (within workspace hours)
        self.start_time = timezone.now() + timedelta(days=1)
        self.start_time = self.start_time.replace(hour=10, minute=0)  # Set to 10 AM for valid range
        self.end_time = self.start_time + timedelta(hours=2)  # Set to 12 PM for valid range

    def test_create_booking(self):
        """Test creating a valid booking"""
        booking = Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            start_time=self.start_time,
            end_time=self.end_time
        )
        self.assertEqual(booking.status, Booking.Status.PENDING)
        self.assertEqual(booking.user.email, 'user@example.com')
        self.assertEqual(booking.workspace.name, 'Test Workspace')

    def test_time_validation(self):
        """Test booking time validation"""
        # Case 1: End before start
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                workspace=self.workspace,
                start_time=self.start_time,
                end_time=self.start_time - timedelta(hours=1)
            )
            booking.full_clean()
        
        # Case 2: Outside workspace hours (before opening time)
        early_start = self.start_time.replace(hour=8, minute=0)  # 8 AM
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                workspace=self.workspace,
                start_time=early_start,
                end_time=early_start + timedelta(hours=1)
            )
            booking.full_clean()

    def test_overlap_validation(self):
        """Test overlapping booking prevention"""
        # Create initial booking within valid hours
        Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            start_time=self.start_time,
            end_time=self.end_time
        )
        
        # Try overlapping booking (e.g., 1 hour overlap)
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                workspace=self.workspace,
                start_time=self.start_time + timedelta(minutes=30),
                end_time=self.end_time + timedelta(minutes=30)
            )
            booking.full_clean()

    def test_workspace_availability(self):
        """Test that a booking is only allowed within workspace hours"""
        # Case 1: Start time is before workspace opening time (8 AM)
        early_start = self.start_time.replace(hour=8, minute=0)  # 8 AM
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                workspace=self.workspace,
                start_time=early_start,
                end_time=early_start + timedelta(hours=1)
            )
            booking.full_clean()
        
        # Case 2: End time is after workspace closing time (6 PM)
        late_end = self.start_time.replace(hour=18, minute=0)  # 6 PM
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                workspace=self.workspace,
                start_time=self.start_time,
                end_time=late_end
            )
            booking.full_clean()

    def test_str_method(self):
        """Test the __str__ method of Booking"""
        booking = Booking.objects.create(
            user=self.user,
            workspace=self.workspace,
            start_time=self.start_time,
            end_time=self.end_time
        )
        expected_str = f"{self.user.email} - {self.workspace.name} ({self.start_time} to {self.end_time})"
        self.assertEqual(str(booking), expected_str)

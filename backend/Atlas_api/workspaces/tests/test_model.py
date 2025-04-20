# workspaces/tests/test_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import time, timedelta
from django.contrib.auth import get_user_model
from ..models import Workspace, Amenity, WorkspaceType
import unittest.mock

User = get_user_model()

class WorkspaceModelTests(TestCase):
    def setUp(self):
        # Create test data
        self.owner = User.objects.create_user(
            email='owner@example.com',
            password='testpass123',
            user_type=User.UserType.OWNER
        )
        
        self.workspace_type = WorkspaceType.objects.create(
            name='Meeting Room',
            description='For team meetings'
        )
        
        self.amenity1 = Amenity.objects.create(
            name='Wi-Fi',
            description='High-speed internet'
        )
        
        self.amenity2 = Amenity.objects.create(
            name='Projector',
            description='HD projector'
        )
        
        self.valid_workspace_data = {
            'owner': self.owner,
            'name': 'Test Workspace',
            'description': 'A great workspace',
            'opening_time': time(9, 0),  # 9:00 AM
            'closing_time': time(17, 0), # 5:00 PM
            'location': 'Test Location',
            'max_capacity': 10,
            'min_capacity': 2,
            'workspace_type': self.workspace_type,
            'price_per_hour': 25.00
        }

    def test_create_workspace(self):
        """Test creating a workspace with valid data"""
        workspace = Workspace.objects.create(**self.valid_workspace_data)
        self.assertEqual(workspace.name, 'Test Workspace')
        self.assertEqual(workspace.owner, self.owner)
        self.assertTrue(workspace.is_available)
        
    def test_opening_closing_time_validation(self):
        """Test that closing time must be after opening time"""
        # Test invalid times (closing before opening)
        invalid_data = self.valid_workspace_data.copy()
        invalid_data['opening_time'] = time(18, 0)  # 6:00 PM
        invalid_data['closing_time'] = time(9, 0)    # 9:00 AM
        
        workspace = Workspace(**invalid_data)
        with self.assertRaises(ValidationError):
            workspace.full_clean()
            
        # Test equal times
        invalid_data['opening_time'] = time(9, 0)
        invalid_data['closing_time'] = time(9, 0)
        workspace = Workspace(**invalid_data)
        with self.assertRaises(ValidationError):
            workspace.full_clean()
            
    def test_amenities_relationship(self):
        """Test many-to-many relationship with amenities"""
        workspace = Workspace.objects.create(**self.valid_workspace_data)
        workspace.amenities.add(self.amenity1, self.amenity2)
        
        self.assertEqual(workspace.amenities.count(), 2)
        self.assertIn(self.amenity1, workspace.amenities.all())
        
    def test_is_open_now(self):
        """Test the is_open_now method"""
        workspace = Workspace.objects.create(**self.valid_workspace_data)
    
        # Test with actual time comparisons (no mocking needed)
        # Since we're using time() in the method now
    
        # During open hours
        workspace.opening_time = time(9, 0)
        workspace.closing_time = time(17, 0)
        with unittest.mock.patch('django.utils.timezone.now') as mock_now:
            # Mock to return a datetime at 12:00 PM
            mock_now.return_value = timezone.datetime(2023, 1, 1, 12, 0)
            self.assertTrue(workspace.is_open_now())
    
        # Before opening
        with unittest.mock.patch('django.utils.timezone.now') as mock_now:
            # Mock to return a datetime at 8:00 AM
            mock_now.return_value = timezone.datetime(2023, 1, 1, 8, 0)
            self.assertFalse(workspace.is_open_now())
    
        # After closing
        with unittest.mock.patch('django.utils.timezone.now') as mock_now:
            # Mock to return a datetime at 6:00 PM
            mock_now.return_value = timezone.datetime(2023, 1, 1, 18, 0)
            self.assertFalse(workspace.is_open_now())
    def test_get_opening_hours_display(self):
        """Test the opening hours display formatting"""
        workspace = Workspace.objects.create(**self.valid_workspace_data)
        self.assertEqual(
            workspace.get_opening_hours_display(),
            "09:00 AM - 05:00 PM"
        )
        
    def test_owner_constraint(self):
        """Test that only OWNER users can be workspace owners"""
        non_owner = User.objects.create_user(
            email='user@example.com',
            password='testpass123',
            user_type=User.UserType.FREELANCER
        )
        
        invalid_data = self.valid_workspace_data.copy()
        invalid_data['owner'] = non_owner
        
        workspace = Workspace(**invalid_data)
        with self.assertRaises(ValidationError):
            workspace.full_clean()
            
    def test_capacity_validation(self):
        """Test that max capacity must be greater than min capacity"""
        invalid_data = self.valid_workspace_data.copy()
        invalid_data['max_capacity'] = 5
        invalid_data['min_capacity'] = 10  # Min > Max
        
        workspace = Workspace(**invalid_data)
        with self.assertRaises(ValidationError):
            workspace.full_clean()
            
    def test_string_representation(self):
        """Test the __str__ method"""
        workspace = Workspace.objects.create(**self.valid_workspace_data)
        self.assertEqual(
            str(workspace),
            "Test Workspace - Test Location"
        )

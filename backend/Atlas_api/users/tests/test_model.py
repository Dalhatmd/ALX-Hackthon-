"""
test module for user model
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user(self):
        """Test creating a basic user works"""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123", user_type="GENERAL"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertEqual(user.user_type, "GENERAL")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Test creating a superuser works"""
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123",
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.user_type, "ADMIN")

    def test_email_required(self):
        """Test that email is required"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="", password="testpass123", user_type="GENERAL"
            )

    def test_user_type_default(self):
        """Test that user_type defaults to GENERAL"""
        user = User.objects.create_user(
            email="default@example.com", password="testpass123"
        )
        self.assertEqual(user.user_type, "GENERAL")

    def test_user_type_validation(self):
        """Test that invalid user types are rejected"""
        with self.assertRaises(ValidationError):
            user = User(
                email="invalid@example.com",
                password="testpass123",
                user_type="INVALID_TYPE",
            )
            user.full_clean()  # This triggers validation

    def test_is_owner_method(self):
        """Test the is_owner() helper method"""
        owner = User.objects.create_user(
            email="owner@example.com", password="testpass123", user_type="OWNER"
        )
        non_owner = User.objects.create_user(
            email="regular@example.com", password="testpass123", user_type="GENERAL"
        )
        self.assertTrue(owner.is_owner())
        self.assertFalse(non_owner.is_owner())

    def test_is_admin_method(self):
        """Test the is_admin() helper method"""
        admin = User.objects.create_user(
            email="admin@example.com", password="testpass123", user_type="ADMIN"
        )
        non_admin = User.objects.create_user(
            email="regular@example.com", password="testpass123", user_type="GENERAL"
        )
        self.assertTrue(admin.is_admin())
        self.assertFalse(non_admin.is_admin())

    def test_string_representation(self):
        """Test the string representation of the user"""
        user = User.objects.create_user(
            email="stringtest@example.com", password="testpass123"
        )
        self.assertEqual(str(user), "stringtest@example.com")

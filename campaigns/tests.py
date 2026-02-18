"""Tests for the campaigns application."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Campaign, Setting
from .serializers import CampaignSerializer, SettingSerializer


class CampaignModelTest(TestCase):
    """Test cases for the Campaign model."""

    def setUp(self):
        """Set up test data."""
        self.campaign = Campaign.objects.create(
            name="Test Campaign",
            override_price=100.00,
            start_date=timezone.now(),
        )

    def test_campaign_creation(self):
        """Test that a campaign can be created with valid data."""
        self.assertEqual(self.campaign.name, "Test Campaign")
        self.assertEqual(self.campaign.override_price, 100.00)
        self.assertIsNotNone(self.campaign.start_date)
        self.assertEqual(str(self.campaign), "Test Campaign")

    def test_campaign_str_method(self):
        """Test the string representation of a campaign."""
        self.assertEqual(str(self.campaign), "Test Campaign")

    def test_campaign_fields(self):
        """Test campaign field types and constraints."""
        # Test CharField max_length
        campaign = Campaign.objects.create(
            name="A" * 255,  # Maximum length
            override_price=50.00,
            start_date=timezone.now(),
        )
        self.assertEqual(len(campaign.name), 255)

    def test_campaign_with_settings_relationship(self):
        """Test campaign relationship with settings."""
        setting = Setting.objects.create(
            campaign=self.campaign, max_price=200.00, enabled=True
        )

        # Test reverse relationship
        self.assertEqual(self.campaign.setting_set.count(), 1)
        self.assertEqual(self.campaign.setting_set.first(), setting)


class SettingModelTest(TestCase):
    """Test cases for the Setting model."""

    def setUp(self):
        """Set up test data."""
        self.campaign = Campaign.objects.create(
            name="Parent Campaign",
            override_price=75.00,
            start_date=timezone.now(),
        )
        self.setting = Setting.objects.create(
            campaign=self.campaign, max_price=150.00, enabled=True
        )

    def test_setting_creation(self):
        """Test that a setting can be created with valid data."""
        self.assertEqual(self.setting.campaign, self.campaign)
        self.assertEqual(self.setting.max_price, 150.00)
        self.assertTrue(self.setting.enabled)

    def test_setting_str_method(self):
        """Test the string representation of a setting."""
        expected_str = f"Setting for {self.campaign.name}"
        self.assertEqual(str(self.setting), expected_str)

    def test_setting_default_values(self):
        """Test default values for setting fields."""
        setting = Setting.objects.create(
            campaign=self.campaign,
            max_price=100.00,
            # enabled should default to False
        )
        self.assertFalse(setting.enabled)

    def test_setting_cascade_delete(self):
        """Test that settings are deleted when campaign is deleted."""
        setting_id = self.setting.id
        campaign_id = self.campaign.id

        # Delete campaign
        self.campaign.delete()

        # Check that setting was also deleted
        with self.assertRaises(Setting.DoesNotExist):
            Setting.objects.get(id=setting_id)

        # Check that campaign was deleted
        with self.assertRaises(Campaign.DoesNotExist):
            Campaign.objects.get(id=campaign_id)


class CampaignSerializerTest(TestCase):
    """Test cases for CampaignSerializer."""

    def setUp(self):
        """Set up test data."""
        self.campaign = Campaign.objects.create(
            name="Serializer Test Campaign",
            override_price=125.00,
            start_date=timezone.now(),
        )
        Setting.objects.create(
            campaign=self.campaign, max_price=300.00, enabled=True
        )

    def test_campaign_serializer_valid_data(self):
        """Test serialization of valid campaign data."""
        serializer = CampaignSerializer(self.campaign)
        data = serializer.data

        self.assertEqual(data["name"], "Serializer Test Campaign")
        self.assertEqual(float(data["override_price"]), 125.00)
        self.assertIn("start_date", data)
        self.assertIn("settings", data)
        self.assertEqual(len(data["settings"]), 1)

    def test_campaign_serializer_create(self):
        """Test creating a campaign through serializer."""
        data = {
            "name": "New Campaign",
            "override_price": "99.99",
            "start_date": timezone.now().isoformat(),
        }
        serializer = CampaignSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        campaign = serializer.save()
        self.assertEqual(campaign.name, "New Campaign")

    def test_campaign_serializer_invalid_data(self):
        """Test serializer validation with invalid data."""
        data = {
            "name": "",  # Empty name should be invalid
            "override_price": "invalid_price",
            "start_date": "invalid_date",
        }
        serializer = CampaignSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("override_price", serializer.errors)
        self.assertIn("start_date", serializer.errors)


class SettingSerializerTest(TestCase):
    """Test cases for SettingSerializer."""

    def setUp(self):
        """Set up test data."""
        self.campaign = Campaign.objects.create(
            name="Setting Serializer Test",
            override_price=50.00,
            start_date=timezone.now(),
        )

    def test_setting_serializer_valid_data(self):
        """Test serialization of valid setting data."""
        setting = Setting.objects.create(
            campaign=self.campaign, max_price=250.00, enabled=False
        )
        serializer = SettingSerializer(setting)
        data = serializer.data

        self.assertEqual(float(data["max_price"]), 250.00)
        self.assertFalse(data["enabled"])
        self.assertEqual(data["campaign"], self.campaign.id)

    def test_setting_serializer_create(self):
        """Test creating a setting through serializer."""
        data = {
            "campaign": self.campaign.id,
            "max_price": "175.50",
            "enabled": True,
        }
        serializer = SettingSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        setting = serializer.save()
        self.assertEqual(setting.campaign, self.campaign)
        self.assertEqual(setting.max_price, 175.50)
        self.assertTrue(setting.enabled)


class CampaignAPITestCase(APITestCase):
    """Base test case for API tests with JWT authentication."""

    def setUp(self):
        """Set up test user and authentication."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.client = self.client_class()

        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Set authorization header
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        # Create test data
        self.campaign = Campaign.objects.create(
            name="API Test Campaign",
            override_price=200.00,
            start_date=timezone.now(),
        )
        self.setting = Setting.objects.create(
            campaign=self.campaign, max_price=500.00, enabled=True
        )

    def tearDown(self):
        """Clean up test data."""
        # Keep authentication for other tests


class CampaignAPITest(CampaignAPITestCase):
    """Test cases for Campaign API endpoints."""

    def test_list_campaigns_authenticated(self):
        """Test listing campaigns with authentication."""
        url = "/api/campaigns/campaign/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "API Test Campaign")

    def test_list_campaigns_unauthenticated(self):
        """Test that unauthenticated requests are rejected."""
        self.client.credentials()  # Remove authentication
        url = "/api/campaigns/campaign/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_campaign(self):
        """Test creating a new campaign."""
        url = "/api/campaigns/campaign/"
        data = {
            "name": "New API Campaign",
            "override_price": "150.75",
            "start_date": timezone.now().isoformat(),
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New API Campaign")
        self.assertEqual(float(response.data["override_price"]), 150.75)

    def test_retrieve_campaign(self):
        """Test retrieving a specific campaign."""
        url = f"/api/campaigns/campaign/{self.campaign.pk}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "API Test Campaign")
        self.assertEqual(len(response.data["settings"]), 1)

    def test_update_campaign(self):
        """Test updating a campaign."""
        url = f"/api/campaigns/campaign/{self.campaign.pk}/"
        data = {
            "name": "Updated Campaign",
            "override_price": "250.00",
            "start_date": self.campaign.start_date.isoformat(),
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Campaign")

    def test_partial_update_campaign(self):
        """Test partially updating a campaign."""
        url = f"/api/campaigns/campaign/{self.campaign.pk}/"
        data = {"name": "Partially Updated"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Partially Updated")

    def test_delete_campaign(self):
        """Test deleting a campaign."""
        url = f"/api/campaigns/campaign/{self.campaign.pk}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify campaign was deleted
        with self.assertRaises(Campaign.DoesNotExist):
            Campaign.objects.get(pk=self.campaign.pk)


class SettingAPITest(CampaignAPITestCase):
    """Test cases for Setting API endpoints."""

    def test_list_settings(self):
        """Test listing all settings."""
        url = "/api/campaigns/setting/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_setting(self):
        """Test creating a new setting."""
        url = "/api/campaigns/setting/"
        data = {
            "campaign": self.campaign.id,
            "max_price": "400.00",
            "enabled": False,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data["max_price"]), 400.00)
        self.assertFalse(response.data["enabled"])

    def test_retrieve_setting(self):
        """Test retrieving a specific setting."""
        url = f"/api/campaigns/setting/{self.setting.pk}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["campaign"], self.campaign.id)

    def test_update_setting(self):
        """Test updating a setting."""
        url = f"/api/campaigns/setting/{self.setting.pk}/"
        data = {
            "campaign": self.campaign.id,
            "max_price": "600.00",
            "enabled": False,
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data["max_price"]), 600.00)

    def test_delete_setting(self):
        """Test deleting a setting."""
        url = f"/api/campaigns/setting/{self.setting.pk}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class JWTAuthenticationTest(APITestCase):
    """Test cases for JWT authentication endpoints."""

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            username="authtest",
            email="auth@example.com",
            password="authpass123",
        )

    def test_obtain_token(self):
        """Test obtaining JWT tokens."""
        url = "/api/token/"
        data = {"username": "authtest", "password": "authpass123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token(self):
        """Test refreshing access token."""
        # First get tokens
        refresh = RefreshToken.for_user(self.user)
        refresh_token = str(refresh)

        url = "/api/token/refresh/"
        data = {"refresh": refresh_token}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_verify_token(self):
        """Test verifying token validity."""
        # Get access token
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        url = "/api/token/verify/"
        data = {"token": access_token}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_credentials(self):
        """Test obtaining token with invalid credentials."""
        url = "/api/token/"
        data = {"username": "authtest", "password": "wrongpassword"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

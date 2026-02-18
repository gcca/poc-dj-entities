"""Serializers for the campaigns application."""

from rest_framework import serializers

from .models import Campaign, Setting


class SettingSerializer(serializers.ModelSerializer):
    """Serializer for campaign settings."""

    class Meta:
        model = Setting
        fields = ["id", "max_price", "enabled", "campaign"]


class CampaignSerializer(serializers.ModelSerializer):
    """Serializer for campaigns with nested settings."""

    settings = SettingSerializer(
        many=True, read_only=True, source="setting_set"
    )

    class Meta:
        model = Campaign
        fields = ["id", "name", "override_price", "start_date", "settings"]

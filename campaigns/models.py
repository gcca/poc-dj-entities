"""Models for the campaigns application."""

from django.db import models


class Campaign(models.Model):
    """Represents a marketing campaign with pricing and timing information."""

    name = models.CharField(max_length=255)
    override_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Setting(models.Model):
    """Configuration settings for a campaign.

    Reverse relationship: Use campaign.setting_set.all() to access settings from a Campaign instance.
    """

    max_price = models.DecimalField(max_digits=15, decimal_places=2)
    enabled = models.BooleanField(default=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    def __str__(self):
        return f"Setting for {self.campaign.name}"

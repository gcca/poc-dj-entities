"""Admin configuration for the campaigns application."""

from django.contrib import admin

from .models import Campaign, Setting


class SettingInline(admin.TabularInline):
    """Inline admin for campaign settings."""

    model = Setting
    extra = 0


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """Admin interface for campaigns."""

    inlines = [SettingInline]
    list_display = ["name", "override_price", "start_date"]


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """Admin interface for settings."""

    list_display = ["campaign", "max_price", "enabled"]

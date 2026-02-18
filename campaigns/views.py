"""Views for the campaigns application."""

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from .models import Campaign, Setting
from .serializers import CampaignSerializer, SettingSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all campaigns",
        description="Retrieve a list of all event sales campaigns. These campaigns are used by organizers to manage and track their event sales activities. **Authentication required.**",
        tags=["Campaigns"],
    ),
    create=extend_schema(
        summary="Create a new campaign",
        description="Create a new event sales campaign with pricing and scheduling information. **Authentication required.**",
        tags=["Campaigns"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a campaign",
        description="Get detailed information about a specific event sales campaign, including all its associated settings. **Authentication required.**",
        tags=["Campaigns"],
    ),
    update=extend_schema(
        summary="Update a campaign",
        description="Update all fields of an existing event sales campaign. **Authentication required.**",
        tags=["Campaigns"],
    ),
    partial_update=extend_schema(
        summary="Partially update a campaign",
        description="Update specific fields of an existing event sales campaign. **Authentication required.**",
        tags=["Campaigns"],
    ),
    destroy=extend_schema(
        summary="Delete a campaign",
        description="Delete an event sales campaign and all its associated settings. **Authentication required.**",
        tags=["Campaigns"],
    ),
)
class CampaignViewSet(viewsets.ModelViewSet):
    """ViewSet for managing event sales campaigns.

    Event sales campaigns are core business entities that define pricing strategies and
    scheduling for event ticket sales. These campaigns are primarily read and managed by
    event organizers to optimize their sales processes.
    """

    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all settings",
        description="Retrieve a list of all campaign settings across all campaigns. Settings provide customizations and particularities for campaigns. **Authentication required.**",
        tags=["Settings"],
    ),
    create=extend_schema(
        summary="Create a new setting",
        description="Create a new setting for a campaign. Settings allow organizers to customize campaign behavior and pricing rules. **Authentication required.**",
        tags=["Settings"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a setting",
        description="Get detailed information about a specific campaign setting. **Authentication required.**",
        tags=["Settings"],
    ),
    update=extend_schema(
        summary="Update a setting",
        description="Update all fields of an existing campaign setting. **Authentication required.**",
        tags=["Settings"],
    ),
    partial_update=extend_schema(
        summary="Partially update a setting",
        description="Update specific fields of an existing campaign setting. **Authentication required.**",
        tags=["Settings"],
    ),
    destroy=extend_schema(
        summary="Delete a setting",
        description="Delete a campaign setting. **Authentication required.**",
        tags=["Settings"],
    ),
)
class SettingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing campaign settings.

    Campaign settings provide customizations and particularities that allow event
    organizers to adapt campaigns to their specific needs. Settings control pricing
    limits, enable/disable functionality, and provide flexibility in campaign
    management.
    """

    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

"""URL configuration for the campaigns application."""

from rest_framework import routers

from .views import CampaignViewSet, SettingViewSet

app_name = "campaigns"

router = routers.DefaultRouter()
router.register(r"campaign", CampaignViewSet)
router.register(r"setting", SettingViewSet)

urlpatterns = router.urls

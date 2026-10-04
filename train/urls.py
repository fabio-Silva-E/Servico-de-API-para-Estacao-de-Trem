from django.urls import path, include
from rest_framework.routers import DefaultRouter

from train.views import (
    StationViewSet,
    RouteViewSet,
    CrewViewSet,
    TrainTypeViewSet,
    TrainViewSet,
    JourneyViewSet,
    OrderViewSet,
)

router = DefaultRouter()
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("crew", CrewViewSet)
router.register("train-types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("journeys", JourneyViewSet)
router.register("orders", OrderViewSet)

app_name = "train"

urlpatterns = [
    path("", include(router.urls)),
]

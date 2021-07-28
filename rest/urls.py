
from rest_framework import routers
from django.urls import path
from django.conf.urls import include
from .views import BridgeDataList, BridgeIdentityViewSet, SensorStatusList

router = routers.DefaultRouter()
router.register(r'parameter', BridgeIdentityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('BridgeData/', BridgeDataList.as_view()),
    path('Sensor/', SensorStatusList.as_view()),
]

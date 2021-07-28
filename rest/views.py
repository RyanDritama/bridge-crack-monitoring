"""
est API view
"""
import time
from rest_framework import generics, permissions, viewsets
from django_plotly_dash.consumers import send_to_pipe_channel
from .serializers import BridgeDataSerializer, BridgeData, BridgeIdentity, BridgeIdentitySerializer,SensorStatus, SensorStatusSerializer

class BridgeDataList(generics.ListCreateAPIView):
    """Bridge data API VIEW"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = BridgeData.objects.all()
    serializer_class = BridgeDataSerializer

    def post(self, request, *args, **kwargs):
        """
        Override post function to call update signal via channels web socket.
        Must post first before signaling client
        """
        signal_channel()
        return super().post(request, *args, **kwargs)

class BridgeIdentityViewSet(viewsets.ModelViewSet):
    """Bridge identity and parameter API VIEW"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = BridgeIdentity.objects.all()
    serializer_class = BridgeIdentitySerializer

    def create(self, request, *args, **kwargs):
        signal_channel()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        signal_channel()
        return super().update(request, *args, **kwargs)
        
    def destroy(self, request, *args, **kwargs):
        signal_channel()
        return super().destroy(request, *args, **kwargs)


class SensorStatusList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SensorStatus.objects.all()
    serializer_class = SensorStatusSerializer
    def post(self, request, *args, **kwargs):
        """
        Override post function to call update signal via channels web socket.
        Must post first before signaling client
        """
        signal_channel()
        return super().post(request, *args, **kwargs)

def signal_channel():
    send_to_pipe_channel(
        channel_name="updater_channel",
        label="updater",
        value=time.time()
    )
# Create your views here.

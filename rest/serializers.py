"""base serializer"""
from rest_framework import serializers
from monitor.models import BridgeData, BridgeIdentity, SensorStatus

class BridgeDataSerializer(serializers.ModelSerializer):
    """Bridge sensor data table serializer"""
    class Meta:
        model = BridgeData
        fields = '__all__'

class BridgeIdentitySerializer(serializers.HyperlinkedModelSerializer):
    """Bridge identity and parameter serializer"""
    class Meta:
        model = BridgeIdentity
        fields = '__all__'

class SensorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorStatus
        fields = '__all__'

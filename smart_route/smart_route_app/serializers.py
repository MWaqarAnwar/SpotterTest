from rest_framework import serializers

class SmartRouteSerializer(serializers.Serializer):
    x1 = serializers.FloatField()
    y1 = serializers.FloatField()
    x2 = serializers.FloatField()
    y2 = serializers.FloatField()
    fuel_prices_csv = serializers.FileField()
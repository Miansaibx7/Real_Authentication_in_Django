from rest_framework import serializers


class TrendSerializer(serializers.Serializer):
    name = serializers.CharField()
    trend_score = serializers.IntegerField()


class ProductDemandSerializer(serializers.Serializer):
    name = serializers.CharField()
    demand_score = serializers.FloatField()
    trend_score = serializers.IntegerField()
    listing_count = serializers.IntegerField()
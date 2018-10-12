from rest_framework import serializers
from .models import EuropeanSun, WinterSki, ModelTraining

class EuropeanSunSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.ReadOnlyField()
    class Meta:
        model = EuropeanSun
        exclude = ['predicted_price']

class WinterSkiSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.ReadOnlyField()
    class Meta:
        model = WinterSki
        exclude = ['predicted_price']

class ModelTrainingSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.ReadOnlyField()
    class Meta:
        model = ModelTraining
        exclude = ['accuracy_r2']
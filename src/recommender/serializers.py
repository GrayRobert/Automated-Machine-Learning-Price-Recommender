from rest_framework import serializers
from .models import PricePrediction, ModelTraining

class PricePredictionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.ReadOnlyField()
    class Meta:
        model = PricePrediction
        fields = ('id', 'hotel_code', 'url', 'predicted_price')

class ModelTrainingSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.ReadOnlyField()
    class Meta:
        model = ModelTraining
        fields = ('id', 'user', 'url', 'trained_date', 'accuracy_r2')
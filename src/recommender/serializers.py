from rest_framework import serializers
from recommender.models import PricePrediction
from recommender.models import ModelTrainingHistory

class PricePredictionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.ReadOnlyField()
    class Meta:
        model = PricePrediction
        fields = ('id', 'url', 'predicted_price')

class ModelTrainingHistorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.ReadOnlyField()
    class Meta:
        model = ModelTrainingHistory
        fields = ('id', 'url', 'user', 'trained_date', 'accuracy_r2')
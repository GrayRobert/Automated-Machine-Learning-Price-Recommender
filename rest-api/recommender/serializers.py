from rest_framework import serializers
from .models import ModelTraining

class ModelTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTraining
        fields = '__all__'
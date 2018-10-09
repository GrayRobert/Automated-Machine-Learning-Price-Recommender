from recommender.models import PricePrediction
from recommender.models import ModelTrainingHistory
from recommender.serializers import PricePredictionSerializer
from recommender.serializers import ModelTrainingHistorySerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import list_route
from rest_framework.response import Response

# Create your views here.
class PricePredictionViewSet(viewsets.ModelViewSet):
  queryset = PricePrediction.objects.all()
  serializer_class = PricePredictionSerializer

  def perform_create(self, serializer):
    instance = serializer.save()
    instance.url = reverse('price-prediction-detail', args=[instance.pk], request=self.request)
    instance.save()

  def delete(self, request):
    PricePrediction.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class ModelTrainingHistoryViewSet(viewsets.ModelViewSet):
  queryset = ModelTrainingHistory.objects.all()
  serializer_class = ModelTrainingHistorySerializer

  def perform_create(self, serializer):
    instance = serializer.save()
    instance.url = reverse('model-training-history-detail', args=[instance.pk], request=self.request)
    instance.save()

  def delete(self, request):
    ModelTrainingHistory.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT) 
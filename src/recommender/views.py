from recommender.models import PricePrediction
from recommender.models import ModelTraining 
from recommender.serializers import PricePredictionSerializer
from recommender.serializers import ModelTrainingSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import list_route
from rest_framework.response import Response

# Create your views here.
class PricePredictionViewSet(viewsets.ModelViewSet):
  queryset = PricePrediction.objects.all()
  serializer_class = PricePredictionSerializer

class ModelTrainingViewSet(viewsets.ModelViewSet):
  queryset = ModelTraining.objects.all()
  serializer_class = ModelTrainingSerializer

class PredictPriceViewSet(viewsets.ViewSet):

  def list(self, request, format=None):
    serializer_class = PricePredictionSerializer
    hotelCode = request.query_params.get('hotel_code') if request.query_params.get('hotel_code') else 'TEST'
    prediction = '{"Hotel Code" : "%s", "Predicted Price": %d}' % (hotelCode,999.99)
    return Response(prediction)



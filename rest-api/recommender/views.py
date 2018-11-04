from recommender.models import EuropeanSun, WinterSki, ModelTraining 
from recommender.serializers import EuropeanSunSerializer, WinterSkiSerializer, ModelTrainingSerializer
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ParseError
from django.http import JsonResponse

import os

from recommender.services.train import ModelTrainingService
from recommender.services.upload import FileUploadService
from recommender.services.predict import ModelPredictionService







# Create your views here.
class EuropeanSunViewSet(viewsets.ModelViewSet):
  queryset = EuropeanSun.objects.all()
  serializer_class = EuropeanSunSerializer

class WinterSkiViewSet(viewsets.ModelViewSet):
  queryset = WinterSki.objects.all()
  serializer_class = WinterSkiSerializer

class ModelTrainingViewSet(viewsets.ModelViewSet):
  queryset = ModelTraining.objects.all()
  serializer_class = ModelTrainingSerializer


# Main Prediction Endpoint
class PredictPriceViewSet(viewsets.ViewSet):

  def list(self, request, format=None):
    hotelCode = request.query_params.get('hotel_code') if request.query_params.get('hotel_code') else 'TEST'
    independentVariables = {} #TBU
    modelType = request.query_params.get('model_type') if request.query_params.get('model_type') else 'RFR'

    modelPreditionService = ModelPredictionService(independentVariables,modelType)

    predictedPrice = modelPreditionService.predictPrice(request)
    prediction = {
      "HotelCode": str(hotelCode), 
      "RecommendedPrice": predictedPrice
    }
    return Response(prediction)


# Main Training Endpoint
class TrainModelViewSet(viewsets.ViewSet):
  
  def list(self, request, format=None):
    independentVariables = {} #TBU
    dependentVariable = 'price_per_person' #TBU
    modelType = request.query_params.get('model_type') if request.query_params.get('model_type') else 'RFR'

    # Train the model and return the accuracy
    model = ModelTrainingService(independentVariables, dependentVariable, modelType)
    accuracy = model.trainModel()
    return Response(accuracy)


# File Upload Endpoint
class FileUploadView(views.APIView):
  parser_classes = (MultiPartParser, FormParser,)

  def put(self, request, filename, format=None):

    # Quick sanity test before we do anything
    if 'file' not in request.data:
      raise ParseError("Empty content")

    TRAINING_DATA = 'training_data.csv'
    file = request.FILES['file']

    fileUploadService = FileUploadService(TRAINING_DATA)
    # Try save the file
    try:
      response = {
          "FileName": str(file), 
          "Status": "success"
      }
      fileUploadService.uploadFile(file)
      return Response(response, status=200)
    # Otherwise thow an error, this is returned to the client by Django
    except:
      raise ParseError("Failed to save file")



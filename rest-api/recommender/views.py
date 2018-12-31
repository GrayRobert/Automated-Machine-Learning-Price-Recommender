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
from recommender.models import ModelTraining
from recommender.serializers import ModelTrainingSerializer
from recommender.services.database import DatabaseStorageController
from recommender.services.delete import FileDeleteService


# Main Prediction Endpoint
class PredictPriceViewSet(viewsets.ViewSet):
  def list(self, request, format=None):

    modelPreditionService = ModelPredictionService(request)

    predictedPrice = modelPreditionService.predictPrice()
    prediction = {
      "RecommendedPrice": predictedPrice
    }
    return Response(prediction)


# Main Training Endpoint
class TrainModelView(views.APIView):
  parser_classes = (MultiPartParser, FormParser,)
  
  def post(self, request, format=None):
    
    # Get our independent variables
    if 'variables' not in request.data:
      raise ParseError("Missing Variables")
    independentVariables = request.data['variables'].split(',')
    print('Independent Variables are: ' + str(independentVariables))

    # Get our dependent variable
    if 'predict' not in request.data:
      raise ParseError("Missing Target Variable")
    dependentVariable = request.data['predict']
    print('Target Variable is: ' + dependentVariable)

    # Get our model description
    modelDescription = request.data['description']
    print('The model description is: ' + modelDescription)

    # Do we want to do a transformation on dependent variable
    transformation = request.data['transformation']
    print('Transformation is: ' + transformation)

    # Get our variables to encode
    encodeCatList = request.data['encodecat'].split(',')
    print('Categorical variables to encode: ' + str(encodeCatList))

    # Get our variables to encode
    encodeDateList = request.data['encodedate'].split(',')
    print('Date variables to encode: ' + str(encodeDateList))

    # Get our variables to drop
    dropList = request.data['drop'].split(',')
    print('Variables to drop: ' + str(dropList))

    # Get our model type
    if 'model' not in request.data:
      raise ParseError("Missing Model Type Selection")
    modelType = request.data['model']

    # Get our max allowed runtime
    maxAllowedRunTime = int(request.data['runtime']) or 60
    if maxAllowedRunTime > 1140:
      raise ParseError("Max Allowed Run Time is 24 hours")

    # Train the model and return the accuracy
    model = ModelTrainingService(independentVariables, dependentVariable, modelDescription, transformation, encodeCatList, encodeDateList, dropList, modelType, maxAllowedRunTime)
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

# Model Training History Endpoint
class ModelTrainingHistoryViewSet(viewsets.ModelViewSet):
  queryset = ModelTraining.objects.all()
  serializer_class = ModelTrainingSerializer

# Model Deletion Endpoint
class DeleteModelView(views.APIView):
  def delete(self, request, modelid, format=None):

    try:
      # Delete file ref from history
      database = DatabaseStorageController('UserID')
      file = database.deleteModelFile(modelid)

      # Delete file from system
      fileDeleteService = FileDeleteService('UserID')
      fileDeleteService.deleteFile(file)

      response = {
          "FileName": str(file), 
          "Status": "deleted"
      }
      return Response(response, status=200)
    # Otherwise thow an error, this is returned to the client by Django
    except:
      raise ParseError("Failed to delete file")



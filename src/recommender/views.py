from recommender.models import EuropeanSun, WinterSki, ModelTraining 
from recommender.serializers import EuropeanSunSerializer, WinterSkiSerializer, ModelTrainingSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.http import JsonResponse
import os
from sklearn.externals import joblib
import pandas as pd
import numpy as np

#SOME CONSTANTS
PROJECT_DIR = os.getcwd()
MODEL_DIR = os.path.join(PROJECT_DIR,'models')
EUR_SUN_MODEL_JOBLIB = os.path.join(MODEL_DIR, "european_sun_model.joblib")
summerFeatures = [
  'accom_stars',
  'staff_pick',
  'trip_adv_rating',
  'trip_adv_reviews',
  'has_swimming_pool',
  'has_sauna',
  'has_jacuzzi',
  'has_tv_in_room',
  'has_air_conditioning',
  'has_wifi',
  'has_hot_tub',
  'has_lift',
  'suitable_for_children',
  'has_child_care',
  'has_bar',
  'has_sea_view',
  'close_to_resort',
  'day_booked_before_travel',
  'holiday_duration',
  'travel_week',
  'booking_week'
]
#WINT_SKI_MODEL_JOBLIB = os.path.join(MODEL_DIR, "winter_ski_model.joblib")
#wintSkiModel = joblib.load(WINT_SKI_MODEL_JOBLIB)

# Function that calls the machine learning model
def predictPrice(request):
  model = joblib.load(EUR_SUN_MODEL_JOBLIB)

  df = pd.DataFrame(columns=summerFeatures)

  for feature in summerFeatures:
    #hotel_code if for reference only it's not part of the trained model
    if feature == 'hotel_code':
      continue
    df.loc[0,feature] = request.query_params.get(feature) if request.query_params.get(feature) else 0
  
  X=np.array(df)
  predictedPrice = model.predict(X)

  print(df.head())
  return predictedPrice



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

class PredictPriceViewSet(viewsets.ViewSet):

  def list(self, request, format=None):
    hotelCode = request.query_params.get('hotel_code') if request.query_params.get('hotel_code') else 'TEST'
    predictedPrice = predictPrice(request)
    prediction = {
      "Hotel Code": str(hotelCode), 
      "Recommended Price": predictedPrice
    }
    return Response(prediction)



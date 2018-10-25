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
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from scipy.stats import spearmanr, pearsonr
from sklearn.ensemble import RandomForestRegressor

#SOME CONSTANTS
PROJECT_DIR = os.getcwd()
FILES_DIR = os.path.join(PROJECT_DIR,'files')
EUR_SUN_MODEL_JOBLIB = os.path.join(FILES_DIR, "european_sun_model.joblib")
DATA_CSV = os.path.join(FILES_DIR, "training_data.csv")

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

def trainModel(request):
  print("Reading CSV training data...\n")
  data = pd.read_csv(DATA_CSV)

  ## Convert to dates
  data.travel_date = pd.to_datetime(data.travel_date, format='%Y/%m/%d')
  data.booking_date = pd.to_datetime(data.booking_date, format='%Y/%m/%d')

  ## Drop what we don't need
  data.dropna(inplace=True)
  data.drop('accomodation', axis=1, inplace=True)
  data.drop('accom_location', axis=1, inplace=True)
  data.drop('destination', axis=1, inplace=True)
  data.drop('accom_id', axis=1, inplace=True)
  data = data.drop('departure_airport', axis=1)
  data = data.drop('accom_type', axis=1)
  data = data.drop('accom_board_basis', axis=1)

  ## Add Weeks, important for seasonality
  data['travel_week'] = data['travel_date'].dt.week
  data['booking_week'] = data['booking_date'].dt.week

  data.drop('travel_date', axis=1, inplace=True)
  data.drop('booking_date', axis=1, inplace=True)

  ## Re-Index
  data.index = range(len(data))

  # Set predictor/target variable
  y=np.array(data.price_per_person)

  # Drop the target variable and create a numpy array of dataframe
  data.drop('price_per_person', axis=1, inplace=True)
  X=np.array(data)


  # ## Split data into training and test sets
  print("Train/Test Split...\n")
  X_train, X_test, y_train, y_test = train_test_split(
    X,y, test_size=0.33, random_state=42)


  # ## RandomForrestRegressor
  print("Training Model...\n")
  model = RandomForestRegressor(n_estimators=2000, min_samples_split=5, min_samples_leaf=1, max_features='log2',max_depth=178, bootstrap= True)
  model.fit(X_train, y_train)
  predicted_train = model.predict(X_train)
  predicted_test = model.predict(X_test)
  r2 = r2_score(y_test, predicted_test)
  spearman = spearmanr(y_test, predicted_test)
  pearson = pearsonr(y_test, predicted_test)

  accuracy = {
      "R2": str(r2), 
      "Spearman": str(spearman),
      "Pearson": str(pearson)
    }

  print("Accuract is: " + str(accuracy))
  #fig, ax = plt.subplots()
  #ax.scatter(y_test, predicted_test, edgecolors=(0, 0, 0))
  #ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
  #ax.set_xlabel('Actual')
  #ax.set_ylabel('Predicted')
  #plt.title('Plot of Predicted V Actual')
  #plt.savefig("PredictedVActual.pdf", format="pdf")
  #plt.show()
  print("Pickling Model...\n")
  joblib.dump(model, EUR_SUN_MODEL_JOBLIB)

  return accuracy



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
      "HotelCode": str(hotelCode), 
      "RecommendedPrice": predictedPrice
    }
    return Response(prediction)

class TrainModelViewSet(viewsets.ViewSet):
  
  def list(self, request, format=None):
    accuracy = trainModel(request)
    return Response(accuracy)



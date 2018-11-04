from sklearn.externals import joblib
import pandas as pd
import numpy as np
import os


# CONSTANTS
HARD_CODED_FEATURES = [
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
FILES_FOLDER = 'files'
JOBLIB_EXTENTION = '.joblib'

class ModelPredictionService():

    # DEFAULT CONSTRUCTOR
    def __init__(self, independentVariables, modelType):
        self.modelType = modelType
        self.independentVariables = HARD_CODED_FEATURES #TODO FIX
        self.projectDir = os.getcwd()
        self.filesDir = os.path.join(self.projectDir, FILES_FOLDER)
        self.pickledModel = os.path.join(self.filesDir, modelType + JOBLIB_EXTENTION)

    # Function that calls the machine learning model
    def predictPrice(self, request):
        model = joblib.load(self.pickledModel)

        df = pd.DataFrame(columns=self.independentVariables)

        for feature in self.independentVariables:
            #hotel_code if for reference only it's not part of the trained model
            if feature == 'hotel_code':
                continue
            df.loc[0,feature] = request.query_params.get(feature) if request.query_params.get(feature) else 0
        
        X=np.array(df)
        predictedPrice = model.predict(X)

        print(df.head())
        return predictedPrice

    
from sklearn.externals import joblib
import pandas as pd
import numpy as np
import os
import json

from recommender.services.database import DatabaseStorageController

class ModelPredictionService():

    # DEFAULT CONSTRUCTOR
    def __init__(self, request):
        self.request = request
        self.model = self.getModelDetails(self.request.query_params.get('model_id'))
        self.modelType = self.model.model_type
        self.independentVariables = json.loads(self.model.independent_variables)
        self.transformation = json.loads(self.model.transformation)
        self.encodeCatList = json.loads(self.model.encode_cat_list)
        self.encodeDateList = json.loads(self.model.encode_date_list)
        self.dropList = json.loads(self.model.drop_list)
        self.dummies = json.loads(self.model.dummies)
        self.pickledModel = self.model.model_file

    # Function that calls the machine learning model
    def predictPrice(self):
        print("loading model: " + str(self.pickledModel))
        model = joblib.load(self.pickledModel)
        request = self.request

        data = pd.DataFrame(columns=self.independentVariables)

        for feature in self.independentVariables:
            #print("Adding feature: " + feature + ":" + str(request.query_params.get(feature)) + "\n")
            data.loc[0,feature] = request.query_params.get(feature) if request.query_params.get(feature) else 0 # ToDo: this might break on different data

        # Encode Date Fields. ToDo: provide encoding options, default is week of the year
        if self.encodeDateList:
            for dateField in self.encodeDateList:
                #print("Date Field encoded as week: " + str(dateField))
                data[dateField] = pd.to_datetime(data[dateField], format='%Y/%m/%d').dt.week

        # Drop Fields
        if self.dropList:
            for dropField in self.dropList:
                #print("Field being dropped: " + dropField)
                data.drop(dropField, axis=1, inplace=True, errors='ignore')

        # Encode Categorical Fields & Dummy
        if self.encodeCatList:
            for catField in self.encodeCatList:
                if catField != '':
                    print("Field being enocded as dummy: " + catField)
                    data[catField] = data[catField].astype('category')

        # Encode Dummies For All Categorical Data
        if self.encodeCatList[0] != '':
            data=pd.get_dummies(data, prefix_sep="__", columns=self.encodeCatList)

        # Remove additional fields
        for field in data.columns:
            if ("__" in field) and (field.split("__")[0] in self.encodeCatList) and field not in self.dummies:
                #print("Removing additional feature {}".format(field))
                data.drop(field, axis=1, inplace=True)
        
        # Add additional columns missing in our test data
        for field in self.dummies:
            if field not in data.columns:
                #print("Adding missing feature {}".format(field))
                data[field] = 0

        # Re-Index
        data.index = range(len(data))

        pd.set_option("display.max_columns",999)
        #print(list(data.columns))
        
        X=np.array(data)
        predictedPrice = model.predict(X)

        # If the dependendent variable was has a log transformation we need to undo this to show the correct predicted price
        if self.transformation == 'log10':
            print("undoing log...")
            predictedPrice = np.power(10,predictedPrice)

        print(data.head())
        return predictedPrice

    def getModelDetails(self, modelId):
        database = DatabaseStorageController('UserID')

        try:
            model = database.getTrainedModel(modelId)
            print('Loaded model is: ' + model.model_type)
            return model
        except:
            print('Could not load model')
            return 0

    
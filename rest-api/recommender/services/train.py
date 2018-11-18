from sklearn.externals import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from scipy.stats import spearmanr, pearsonr
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from xgboost import XGBRegressor
from copy import copy
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from sklearn.preprocessing import FunctionTransformer
import os
import json

from recommender.services.database import DatabaseStorageController

# CONSTANTS
FILES_FOLDER = 'files'
TRAINING_DATA = 'training_data.csv'
JOBLIB_EXTENTION = '.joblib'

class ModelTrainingService():

    # CONSTRUCTOR
    def __init__(self, independentVariables, dependentVariable, encodeCatList, encodeDateList, dropList, modelType):
        self.independentVariables = independentVariables
        self.dependentVariable = dependentVariable
        self.encodeCatList = encodeCatList
        self.encodeDateList = encodeDateList
        self.dropList = dropList
        self.modelType = modelType
        self.projectDir = os.getcwd()
        self.filesDir = os.path.join(self.projectDir, FILES_FOLDER)
        self.trainingData = os.path.join(self.filesDir, TRAINING_DATA)

    # TRAIN MODEL
    def trainModel(self):
        print("Reading CSV training data...\n")
        data = pd.read_csv(self.trainingData)

        # Drop Fields
        if len(self.dropList) > 0:
            for dropField in self.dropList:
                print("Field being dropped: " + dropField)
                data.drop(dropField, axis=1, inplace=True, errors='ignore')

        # We store one record as a sample JSON object that will later be used to consturct test prediction form based on the fields of the model
        # This is because the model fields are dynamic and can vary from one trained model to another.
        testData = data.head(1)
        testData.drop(self.dependentVariable, axis=1, inplace=True)
        processedFields = list(testData.columns[:])

        # Encode Date Fields. ToDo: provide encoding options, default is week of the year
        if len(self.encodeDateList) > 0:
            for dateField in self.encodeDateList:
                print("Date Field encoded as week: " + str(dateField))
                data[dateField] = pd.to_datetime(data[dateField], format='%Y/%m/%d').dt.week

        # Encode Categorical Fields
        if len(self.encodeCatList) > 0:
            for catField in self.encodeCatList:
                if catField != '':
                    print("Field being enocded as dummy: " + catField)
                    data[catField] = data[catField].astype('category')

        # Encode Dummies For All Categorical Data
        if self.encodeCatList[0] != '':
            data=pd.get_dummies(data, prefix_sep="__", columns=self.encodeCatList)

        ## Put in zeros for any nulls
        data.fillna(inplace=True, value=0)

        # Re-Index
        data.index = range(len(data))

        # Store dummies and processed columns for later
        dummies = [col for col in data 
            if "__" in col 
            and col.split("__")[0] in self.encodeCatList]
        print("Dummies: " + str(dummies))

        # Show data
        print(data.head())

        # Set predictor/target variable
        y=np.array(data[self.dependentVariable])

        # Drop the target variable and create a numpy array of dataframe
        data.drop(self.dependentVariable, axis=1, inplace=True)
        X=np.array(data)


        # ## Split data into training and test sets
        print("Train/Test Split...\n")
        X_train, X_test, y_train, y_test = train_test_split(
            X,y, test_size=0.20, random_state=42)


        print("Training Model As: " + self.modelType + "\n")

        # ## Random Forrest Regressor
        if(self.modelType == 'RFR'):
            model = RandomForestRegressor(n_estimators=2000, min_samples_split=5, min_samples_leaf=1, max_features='log2',max_depth=178, bootstrap= True)
        # ## Extra Trees Regressor
        if(self.modelType == 'EXT'):
            model = make_pipeline(
                make_union(
                    FunctionTransformer(copy),
                    FunctionTransformer(copy)
                ),
                StackingEstimator(estimator=XGBRegressor(learning_rate=0.1, max_depth=5, min_child_weight=6, n_estimators=100, nthread=1, subsample=0.7000000000000001)),
                ExtraTreesRegressor(bootstrap=False, max_features=0.35000000000000003, min_samples_leaf=2, min_samples_split=15, n_estimators=100)
            )
        model.fit(X_train, y_train)
        predicted_test = model.predict(X_test)
        r2 = r2_score(y_test, predicted_test)
        spearman = spearmanr(y_test, predicted_test)
        pearson = pearsonr(y_test, predicted_test)

        accuracy = {
            "R2": str(r2), 
            "Spearman": str(spearman),
            "Pearson": str(pearson)
            }

        print("Accuracy is: " + str(accuracy))

        # Prepare some test data
        testJSON = testData.to_json(orient='records')
        # Store model training history
        database = DatabaseStorageController('UserID')
        modelID = database.storeTrainedModel(json.dumps(processedFields), json.dumps(self.dependentVariable), json.dumps(self.encodeCatList), json.dumps(self.encodeDateList), json.dumps(self.dropList), json.dumps(dummies), self.modelType, r2, 1.0, str(testJSON))

        modelFile = os.path.join(self.filesDir, self.modelType + str(modelID) + JOBLIB_EXTENTION)
        print("Pickling Model...\n")
        joblib.dump(model, modelFile)

        database.updateModelFile(modelID, modelFile)

        return accuracy
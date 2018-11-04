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

# CONSTANTS
FILES_FOLDER = 'files'
TRAINING_DATA = 'training_data.csv'
JOBLIB_EXTENTION = '.joblib'

class ModelTrainingService():

    # CONSTRUCTOR
    def __init__(self, independentVariables, dependentVariable, modelType):
        self.independentVariables = independentVariables
        self.dependentVariable = dependentVariable
        self.modelType = modelType
        self.projectDir = os.getcwd()
        self.filesDir = os.path.join(self.projectDir, FILES_FOLDER)
        self.trainingData = os.path.join(self.filesDir, TRAINING_DATA)
        self.pickledModel = os.path.join(self.filesDir, modelType + JOBLIB_EXTENTION)

    # TRAIN MODEL
    def trainModel(self):
        print("Reading CSV training data...\n")
        data = pd.read_csv(self.trainingData)

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
        data.drop(self.dependentVariable, axis=1, inplace=True)
        X=np.array(data)


        # ## Split data into training and test sets
        print("Train/Test Split...\n")
        X_train, X_test, y_train, y_test = train_test_split(
            X,y, test_size=0.33, random_state=42)


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
        joblib.dump(model, self.pickledModel)

        return accuracy
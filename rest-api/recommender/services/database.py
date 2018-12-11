
from recommender.models import ModelTraining

class DatabaseStorageController():

    def __init__(self, userID):
        # Empty Constructor
        self.userID = userID

    def storeTrainedModel(self, independentVariables, dependentVariable, transformation, encodeCatList, encodeDateList, dropList, dummies, modelType, accuracyR2, accuracyRMSE, testJSON, scatterPlot):
        # do something
        model = ModelTraining(
            independent_variables = independentVariables,
            dependent_variable = dependentVariable,
            transformation = transformation,
            encode_cat_list = encodeCatList,
            encode_date_list = encodeDateList,
            drop_list = dropList,
            dummies = dummies,
            model_type = modelType,
            user_id = self.userID,
            accuracy_r2 = accuracyR2,
            accuracy_rmse = accuracyRMSE,
            test_json = testJSON,
            scatter_plot = scatterPlot
        )

        result = model.save()
        print("Storing model training history record..." + str(result))
        return model.id

    def getTrainedModel(self, modelId):
        model = ModelTraining.objects.get(id = modelId)
        return model

    def getModelTrainingHistory(self):
        history = ModelTraining.objects.all()
        return history

    # Updates the filename of the model after it's pickled
    def updateModelFile(self, modelId, file):
        model = ModelTraining.objects.get(id = modelId)
        model.model_file = file
        model.save()

    # Deletes the filename of the model after deleting the pickled model file
    def deleteModelFile(self, modelId):
        model = ModelTraining.objects.get(id = modelId)
        modelFile = model.model_file
        model.model_file = None
        model.save()
        return modelFile

from django.conf.urls import url, include
from recommender.views import PredictPriceViewSet, TrainModelView, FileUploadView, ModelTrainingHistoryViewSet, DeleteModelView
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'model/predict', PredictPriceViewSet, base_name='predict-price')
router.register(r'model/traininghistory', ModelTrainingHistoryViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^file/upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
    url(r'^model/delete/(?P<modelid>[^/]+)$', DeleteModelView.as_view()),
    url(r'^model/train', TrainModelView.as_view()),
]
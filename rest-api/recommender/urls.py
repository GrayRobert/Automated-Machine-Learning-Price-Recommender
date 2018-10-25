from django.conf.urls import url, include
from recommender.views import PredictPriceViewSet, TrainModelViewSet, EuropeanSunViewSet, WinterSkiViewSet, ModelTrainingViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'european/sun', EuropeanSunViewSet)
router.register(r'winter/ski', WinterSkiViewSet)
router.register(r'model/training', ModelTrainingViewSet)
router.register(r'predict/price', PredictPriceViewSet, base_name='predict-price')
router.register(r'train/model', TrainModelViewSet , base_name='train-model')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]
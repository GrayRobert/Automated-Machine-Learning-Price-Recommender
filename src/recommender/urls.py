from django.conf.urls import url, include
from recommender.views import PredictPriceViewSet, PricePredictionViewSet, ModelTrainingViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'predictions', PricePredictionViewSet)
router.register(r'train', ModelTrainingViewSet)
router.register(r'predict', PredictPriceViewSet, base_name='predict')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]
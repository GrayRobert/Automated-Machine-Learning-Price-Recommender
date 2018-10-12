from django.contrib import admin
from .models import PricePrediction, ModelTraining
# Register your models here.

admin.site.register(PricePrediction)
admin.site.register(ModelTraining)
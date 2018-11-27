from django.db import models

class ModelTraining(models.Model):
    independent_variables = models.TextField(null=True, blank=True)
    dependent_variable = models.TextField(null=True, blank=True)
    encode_cat_list = models.TextField(null=True, blank=True)
    encode_date_list = models.TextField(null=True, blank=True)
    drop_list = models.TextField(null=True, blank=True)
    dummies = models.TextField(null=True, blank=True)
    model_type = models.TextField(null=True, blank=True)
    user_id = models.CharField(max_length=256, null=True, blank=True)
    trained_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    accuracy_r2 = models.FloatField(null=True, blank=True)
    accuracy_rmse = models.FloatField(null=True, blank=True)
    model_file = models.TextField(null=True, blank=True)
    test_json = models.TextField(null=True, blank=True)
    scatter_plot = models.TextField(null=True, blank=True)
from django.db import models

# Create your models here.
# This is just to get and idea of the model. ToDo: Split out holiday types to seperate models possibly.
class PricePrediction(models.Model):
    hotel_code = models.CharField(max_length=50, null=False, blank=False)
    accom_stars = models.IntegerField(null=True, blank=True)
    staff_pick = models.IntegerField(null=True, blank=True)
    trip_adv_rating = models.IntegerField(null=True, blank=True)
    trip_adv_reviews = models.IntegerField(null=True, blank=True)
    has_swimming_pool = models.IntegerField(null=True, blank=True)
    has_sauna = models.IntegerField(null=True, blank=True)
    has_jacuzzi = models.IntegerField(null=True, blank=True)
    has_tv_in_room = models.IntegerField(null=True, blank=True)
    has_air_conditioning = models.IntegerField(null=True, blank=True)
    has_wifi = models.IntegerField(null=True, blank=True)
    has_hot_tub = models.IntegerField(null=True, blank=True)
    has_lift = models.IntegerField(null=True, blank=True)
    suitable_for_children = models.IntegerField(null=True, blank=True)
    has_child_care = models.IntegerField(null=True, blank=True)
    has_bar = models.IntegerField(null=True, blank=True)
    has_sea_view = models.IntegerField(null=True, blank=True)
    close_to_resort = models.IntegerField(null=True, blank=True)
    close_to_lift = models.IntegerField(null=True, blank=True)
    ski_in_ski_out = models.IntegerField(null=True, blank=True)
    days_booked_before_travel = models.IntegerField(null=True, blank=True)
    holiday_duration = models.IntegerField(null=True, blank=True)
    travel_week = models.IntegerField(null=True, blank=True)
    booking_week = models.IntegerField(null=True, blank=True)
    apartment = models.IntegerField(null=True, blank=True)
    holiday_home = models.IntegerField(null=True, blank=True)
    hotel = models.IntegerField(null=True, blank=True)
    chalet = models.IntegerField(null=True, blank=True)
    bed_and_breakfast = models.IntegerField(null=True, blank=True)
    half_board = models.IntegerField(null=True, blank=True)
    full_board = models.IntegerField(null=True, blank=True)
    all_enclusive = models.IntegerField(null=True, blank=True)
    self_catering = models.IntegerField(null=True, blank=True)
    dep_DUB = models.IntegerField(null=True, blank=True)
    dep_BFS = models.IntegerField(null=True, blank=True)
    dep_BHD = models.IntegerField(null=True, blank=True)
    dep_ORK = models.IntegerField(null=True, blank=True)
    dep_LGW = models.IntegerField(null=True, blank=True)
    dep_MAN = models.IntegerField(null=True, blank=True)
    predicted_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return "{} Predicted Price: {}".format(self.hotel_code, self.predicted_price)

class ModelTraining(models.Model):
    user = models.CharField(max_length=256, null=True, blank=True)
    trained_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    accuracy_r2 = models.IntegerField( null=True, blank=True)

    def __str__(self):
        return "Accuracy R2: {}".format(self.accuracy_r2)
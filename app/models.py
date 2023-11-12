from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='trips_as_user')
    destination_lat = models.DecimalField(max_digits=9, decimal_places=6, default= 0.0)
    destination_lon = models.DecimalField(max_digits=9, decimal_places=6, default= 0.0)
    origin_lat = models.DecimalField(max_digits=9, decimal_places=6, default= 0.0)
    origin_lon = models.DecimalField(max_digits=9, decimal_places=6, default= 0.0)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips_as_driver', null=True)

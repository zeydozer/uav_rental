from django.db import models
from django.contrib.auth.models import User

class UAV(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight = models.FloatField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand} | {self.model}"
    
    def rent(self, renting_member, start_date, end_date):
        RentalService = rest_api.services.rental_service.RentalService
        rental = RentalService.rent_uav(self, renting_member, start_date, end_date)
        return rental

class Rental(models.Model):
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE)
    renting_member = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Rental by {self.renting_member.username} for {self.uav.model} from {self.start_date} to {self.end_date}"
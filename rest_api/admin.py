from django.contrib import admin
from .models import UAV, Rental

class UAVAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "weight", "category")

admin.site.register(UAV, UAVAdmin)

class RentalAdmin(admin.ModelAdmin):
    list_display = ("uav", "renting_member", "start_date", "end_date")

admin.site.register(Rental, RentalAdmin)
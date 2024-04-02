from django.contrib import admin
from .models import Cars, Cargo, Locations


# Register your models here.

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    pass


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    pass


@admin.register(Locations)
class LocationAdmin(admin.ModelAdmin):
    pass

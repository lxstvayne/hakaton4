from django.contrib import admin

from . import models


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Complex)
class ComplexAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Liter)
class LiterAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Floor)
class FloorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Commercial)
class CommercialAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass

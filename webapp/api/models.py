from django.db import models
from django_auto_one_to_one import AutoOneToOneModel

from authentication.models import User


class Coordinates(models.Model):
    longitude = models.DecimalField(max_digits=30, decimal_places=15)
    latitude = models.DecimalField(max_digits=30, decimal_places=15)


class City(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=300)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Complex(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='complexes')
    address = models.CharField(max_length=300)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Liter(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE, related_name='liters')
    number = models.IntegerField()

    def __str__(self):
        return f"{self.complex!s} {self.number}"


class Section(models.Model):
    liter = models.ForeignKey(Liter, on_delete=models.CASCADE, related_name='sections')
    number = models.IntegerField()

    def __str__(self):
        return f"{self.liter!s} {self.number}"


class Plan(models.Model):
    html = models.TextField()


class Path(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='paths')
    room_id = models.IntegerField()
    d = models.CharField(max_length=800)


class Floor(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='floors')
    number = models.IntegerField()
    plan = models.OneToOneField(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.section.liter.complex!s} {self.number}"


class Commercial(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class CommercialRecommendationsRatings(models.Model):
    commercial = models.ForeignKey(Commercial, on_delete=models.CASCADE, related_name='commercial_recommendations')
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE, related_name='ratings')
    welfare_score = models.FloatField()
    traffic_score = models.FloatField()
    competitors_score = models.FloatField()
    population_score = models.FloatField()
    sector = models.CharField(max_length=255, null=True)


class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    area = models.FloatField()
    plan = models.URLField()

    def __str__(self):
        return f"{self.floor.section.liter.complex!s} {self.id} {self.area} м2 - {self.commercial!s}"


class Client(AutoOneToOneModel(User)):
    pass


class ClientRoom(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='commercial_room')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_rooms')
    commercial_type = models.ForeignKey(Commercial, on_delete=models.CASCADE, related_name="rooms")
    status = models.CharField(max_length=150, choices=(("Продано", "Продано"), ("Арендуется", "Арендуется")))
    price_per_month = models.IntegerField(null=True, default=None)
    created_at = models.DateField()

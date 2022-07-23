from rest_framework import serializers

from . import models


class DistrictSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name')

    class Meta:
        model = models.District
        fields = ("name", "city")


class ComplexSerializer(serializers.ModelSerializer):
    district = serializers.CharField(source='district.name')

    class Meta:
        model = models.Complex
        fields = ("district", "address", "name")


class LiterSerializer(serializers.ModelSerializer):
    complex = ComplexSerializer()

    class Meta:
        model = models.Liter
        fields = ('complex', 'number')


class SectionSerializer(serializers.ModelSerializer):
    liter = LiterSerializer()

    class Meta:
        model = models.Section
        fields = ("liter", "number")


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = ("html",)


class FloorSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    plan = PlanSerializer()

    class Meta:
        model = models.Floor
        fields = ("section", "plan", "number")


class CommercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Commercial
        fields = ("name",)


class RoomSerializer(serializers.ModelSerializer):
    floor = serializers.IntegerField(source='floor.number')
    section = serializers.IntegerField(source='floor.section.number')
    liter = serializers.IntegerField(source='floor.section.liter.number')
    complex = serializers.CharField(source='floor.section.liter.complex.name')

    class Meta:
        model = models.Room
        fields = ("id", "name", "price", "floor", "area", "plan", "section", "liter", "complex")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id", "first_name", "last_name")


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Client
        fields = ("user",)


class ClientRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    client = ClientSerializer()

    class Meta:
        model = models.ClientRoom
        fields = ("room", "client", "commercial_type", "status", "price_per_month", "created_at")


class CommercialRecommendationsRatingsSerializer(serializers.ModelSerializer):
    complex = serializers.CharField(source="complex.name")
    commercial = serializers.CharField(source="commercial.name")

    class Meta:
        model = models.CommercialRecommendationsRatings
        fields = ("commercial", "welfare_score", "traffic_score", "competitors_score", "population_score",
                  "sector", "complex")

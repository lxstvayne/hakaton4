from django_filters import rest_framework as filters

from . import models


class RoomListFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    floor = filters.NumberFilter(field_name="floor__number")
    commercial = filters.CharFilter('commercial__name')
    min_area = filters.NumberFilter(field_name="area", lookup_expr='gte')
    max_area = filters.NumberFilter(field_name="area", lookup_expr='lte')
    complex = filters.CharFilter(field_name="floor__section__liter__complex__name")

    order_by = filters.OrderingFilter

    class Meta:
        model = models.Room
        fields = []


class CommercialRecommendationsRatingsFilter(filters.FilterSet):
    complex = filters.CharFilter('complex__name')

    class Meta:
        model = models.CommercialRecommendationsRatings
        fields = ["title"]

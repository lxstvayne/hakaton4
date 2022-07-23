from django.db.models import Sum, F
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView, GenericAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from . import models
from . import serializers
from .filters import RoomListFilter, CommercialRecommendationsRatingsFilter


class ListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 25


class ComplexListAPIView(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ComplexSerializer
    queryset = models.Complex.objects.all()


class DistrictListAPIView(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DistrictSerializer
    queryset = models.District.objects.all()


class RoomAPIView(GenericAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer

    def get(self, request, id):
        data = get_object_or_404(self.queryset, id=id)
        serialized_data = self.serializer_class(data)
        return Response(serialized_data.data)


class RoomListAPIView(ListAPIView):
    serializer_class = serializers.RoomSerializer
    pagination_class = ListPagination
    queryset = models.Room.objects.all().order_by('id')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RoomListFilter


class CommercialRecommendationsRatingsAPIView(ListAPIView):
    serializer_class = serializers.CommercialRecommendationsRatingsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommercialRecommendationsRatingsFilter
    queryset = models.CommercialRecommendationsRatings.objects.all()

    def get_queryset(self):
        q = self.queryset.annotate(
            rating=Sum(F("welfare_score") + F("traffic_score") + (5 - F("competitors_score")) + F("population_score")))

        q = q.filter(rating__gte=9).order_by('-rating')

        return q

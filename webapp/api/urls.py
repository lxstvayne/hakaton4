from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('complexes/', views.ComplexListAPIView.as_view()),
    path('districts/', views.DistrictListAPIView.as_view()),
    path('rooms/', views.RoomListAPIView.as_view()),
    path('rooms/<int:id>', views.RoomAPIView.as_view()),
    path('recommendations/', views.CommercialRecommendationsRatingsAPIView.as_view())
]

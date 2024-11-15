from django.urls import path
from locations import views

urlpatterns = [
    path('locations/', views.LocationList.as_view(), name='locations'),
    path('locations/<int:pk>/', views.LocationDetail.as_view(), name='location'),
    path('locations/countries/', views.country_list, name='country_list'),
    path(
        'locations/full-countries/',
        views.full_country_list,
        name='full_country_list'),
]

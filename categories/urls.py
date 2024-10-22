from django.urls import path
from categories import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category'),
]
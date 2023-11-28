from django.urls import path
from . import views

urlpatterns = [
    path('hydrogen-production/', views.hydrogen_production_view, name='hydrogen_production'),
    path('test/', views.generic_test_view, name='generic-test'),
]

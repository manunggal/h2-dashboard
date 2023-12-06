from django.urls import path
from . import views

urlpatterns = [
    path('', views.hydrogen_blog, name='hydrogen_blog'),
    path('hydrogen-production/', views.hydrogen_production_view, name='hydrogen_production'),
    path('test/', views.generic_test_view, name='generic-test'),
]

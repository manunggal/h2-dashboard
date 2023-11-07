from django.urls import path
from . import views

urlpatterns = [
    path('hydrogen-production/', views.hydrogen_production_view, name='hydrogen_production'),
]

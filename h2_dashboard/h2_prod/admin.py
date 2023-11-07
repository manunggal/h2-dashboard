from django.contrib import admin
from .models import ElectricityProductionBenchmark, CO2EmissionsBenchmark

@admin.register(ElectricityProductionBenchmark)
class ElectricityProductionBenchmarkAdmin(admin.ModelAdmin):
    list_display = ('year', 'total_production')
    search_fields = ('year',)

@admin.register(CO2EmissionsBenchmark)
class CO2EmissionsBenchmarkAdmin(admin.ModelAdmin):
    list_display = ('year', 'total_emissions')
    search_fields = ('year',)

from django.contrib import admin
from .models import ElectricityProductionBenchmark, CO2EmissionsBenchmark

@admin.register(ElectricityProductionBenchmark)
class ElectricityProductionBenchmarkAdmin(admin.ModelAdmin):
    list_display = ('year', 'value')
    search_fields = ('year',)

@admin.register(CO2EmissionsBenchmark)
class CO2EmissionsBenchmarkAdmin(admin.ModelAdmin):
    list_display = ('year', 'value')
    search_fields = ('year',)

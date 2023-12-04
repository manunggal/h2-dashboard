from django.contrib import admin
from .models import ElectricityProductionBenchmark, CO2eEmissionsBenchmark

@admin.register(ElectricityProductionBenchmark)
class ElectricityProductionBenchmarkAdmin(admin.ModelAdmin):
    list_display = ('year', 'value')
    search_fields = ('year',)

@admin.register(CO2eEmissionsBenchmark)
class CO2eEmissionsBenchmarkAdmin(admin.ModelAdmin):
    list_display = ('year', 'value')
    search_fields = ('year',)

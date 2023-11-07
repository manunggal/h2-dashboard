from django.db import models

class ElectricityProductionBenchmark(models.Model):
    # The 'year' field represents the year of the benchmark data.
    year = models.IntegerField(help_text="Year of the benchmark data")
    # The 'total_production' field is the total electricity production for the year
    # stored in gigawatt-hours (GWh).
    total_production = models.FloatField(help_text="Total electricity production in gigawatt-hours (GWh)")

    def __str__(self):
        # String representation of the ElectricityProductionBenchmark model
        return f"Electricity Production Benchmark for {self.year}"

class CO2EmissionsBenchmark(models.Model):
    # The 'year' field represents the year of the benchmark data.
    year = models.IntegerField(help_text="Year of the benchmark data")
    # The 'total_emissions' field is the total CO2 emissions for the year
    # stored in megatonnes (MtCO2).
    total_emissions = models.FloatField(help_text="Total CO2 emissions in megatonnes")

    def __str__(self):
        # String representation of the CO2EmissionsBenchmark model
        return f"CO2 Emissions Benchmark for {self.year}"

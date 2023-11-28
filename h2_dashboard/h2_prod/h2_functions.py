
from django.apps import apps

# dummy input data
# total_h2_production = 90
# electrolyzer_efficiency = 70
# percentage_renewable_electricity = 33
# co2_emission_per_kwh_fossil = 0.5
# co2_emission_per_kwh_renewable = 0.0


# constant
kwh_per_kg_h2 = 33.3  # kWh required per kg of H2 on a LHV basis, it's almost like a constant
default_total_h2_production = 120  # megatonnes per year
electrolyzer_rating = 20 # MW ref https://hydrogentechworld.com/worlds-largest-pem-electrolyzer-installed-in-canada


# current state of H2 production
def current_total_co2_emissions(total_h2_production):
    # Percentage of hydrogen production from each source
    percentage_gas = 0.48
    percentage_oil = 0.3
    percentage_coal = 0.18
    percentage_electro = 0.04

    # CO2 emissions (kg) from each source
    co2_per_kg_gas = 12  # kg CO2e per kg H2
    co2_per_kg_oil = 18  # kg CO2e per kg H2
    co2_per_kg_coal = 24  # kg CO2e per kg H2
    co2_per_kg_electro = 22  # kg CO2e per kg H2

    # Convert total hydrogen production from megatonnes to kilograms (1 megatonne = 1,000,000,000 kg)
    total_h2_prod_kg = float(total_h2_production) * 1e9

    # Calculating the CO2 emissions from each source
    co2_emissions_gas = total_h2_prod_kg * percentage_gas * co2_per_kg_gas
    co2_emissions_oil = total_h2_prod_kg * percentage_oil * co2_per_kg_oil
    co2_emissions_coal = total_h2_prod_kg * percentage_coal * co2_per_kg_coal
    co2_emissions_electro = total_h2_prod_kg * percentage_electro * co2_per_kg_electro

    # Summing up the CO2 emissions from all sources to get the total CO2 emissions from hydrogen production
    current_state_co2_emission = co2_emissions_gas + co2_emissions_oil + co2_emissions_coal + co2_emissions_electro
    return current_state_co2_emission * 1e-9  # Conversion to Mega tonnes

# current_state_co2_emission = current_total_co2_emissions(total_h2_production)

# calculations for the new state of H2 production, 
# how much CO2 emission is reduced, and how much electricity is required

def calculate_outputs(total_h2_production, 
                      electrolyzer_efficiency,
                      percentage_renewable_electricity, 
                      co2_emission_per_kwh_fossil,
                      current_state_co2_emission,
                      electrolyzer_rating):
    
    electricity_per_kg_h2 = kwh_per_kg_h2 / (electrolyzer_efficiency / 100)
    total_electricity_requirement = electricity_per_kg_h2 * total_h2_production * 1e9  # Conversion to kg

    fossil_electricity_percentage = 1 - (percentage_renewable_electricity / 100)
    co2_emission_fossil = total_electricity_requirement * fossil_electricity_percentage * co2_emission_per_kwh_fossil
    

    total_co2_emissions = co2_emission_fossil
    co2_emissions_reduction = current_state_co2_emission - (total_co2_emissions * 1e-9)  # Conversion to Mega tonnes for both

    required_electrolyzer_units = (total_electricity_requirement*1e-3)/(electrolyzer_rating * 8760) # electricity in kwh, electrolyzer rating in MW, 8760 hours in a year
    
    return total_electricity_requirement * 1e-9, total_co2_emissions * 1e-9, co2_emissions_reduction, total_h2_production, required_electrolyzer_units


def calculate_defaults():
    default_total_co2_emissions = current_total_co2_emissions(120)
    total_h2_prod_kg = 120 * 1e9
    default_total_electricity_requirement = total_h2_prod_kg * 0.04 * 22
    return (default_total_electricity_requirement * 1e-9, default_total_co2_emissions, 0)

# default_total_electricity_requirement, default_total_co2_emissions = calculate_defaults(default_total_h2_production)

# total_electricity_requirement, total_co2_emission, co2_emission_reduction = calculate_outputs(
#     total_h2_production, electrolyzer_efficiency, percentage_renewable_electricity, 
#     co2_emission_per_kwh_fossil, co2_emission_per_kwh_renewable, current_state_co2_emission)

# print(f'Total electricity required for clean hydrogen production: {total_electricity_requirement:.2f} tWh')
# print(f'Total CO2 emission: {total_co2_emission:.2f} Mega tonnes per year')
# print(f'CO2 emission reduction: {co2_emission_reduction:.2f} Mega tonnes per year')
# print(f'Previous CO2 emission: {current_state_co2_emission:.2f} Mega tonnes per year')



def get_benchmark_data():
    # List of benchmark models you have, e.g., ['ElectricityProductionBenchmark', 'CO2EmissionsBenchmark']
    benchmark_models = ['ElectricityProductionBenchmark', 'CO2EmissionsBenchmark']
    benchmark_data = {}

    # Loop through each benchmark model and get all the data
    for model_name in benchmark_models:
        model = apps.get_model('h2_prod', model_name)  # Adjust 'h2_prod' to your app name if different
        benchmarks = model.objects.all()

        # Loop through each benchmark object and store the data in a dictionary
        for benchmark in benchmarks:
            key = f"{model_name}-{benchmark.year}"
            if key not in benchmark_data:
                benchmark_data[key] = []
            benchmark_data[key].append((benchmark.value, benchmark.name))
    return benchmark_data

# to convert request.POST elements to float
def post_floater(post_data):
    for key, value in post_data.items():
        if key != 'csrfmiddlewaretoken':
            try:
                post_data[key] = float(value)
            except ValueError:
                # Handle the case where conversion fails
                print(f"Value conversion failed for key: {key}")
                post_data[key] = None  # or handle this differently as per your need

    # Logging the converted values and their types
    # for key, value in post_data.items():
    #     print(f"{key}: {value}, Type: {type(value)}")
    
    return post_data
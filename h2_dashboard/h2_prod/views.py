from django.shortcuts import render
# from django.contrib import messages
from .forms import HydrogenProductionForm
from .h2_functions import calculate_outputs, current_total_co2e_emissions, calculate_defaults, get_benchmark_data, electrolyzer_rating, post_floater, process_benchmark_data, plotting_calc_vs_benchmark, update_plot_calc_vs_benchmark
from .models import ElectricityProductionBenchmark, CO2eEmissionsBenchmark
from plotly.offline import plot
import plotly.graph_objects as go
from django.http import HttpResponse, JsonResponse
import json



def home(request):
    return render(request, 'home.html')

def hydrogen_blog(request):
    return render(request, 'h2_prod/hydrogen.html')

def hydrogen_production_view(request):
    #  debugging
    print("View function called")
    print("Request method:", request.method)

    # initial values
    initial_values = {
        'initial_h2_production': 90,  # MegaTonnes
        'initial_electrolyzer_efficiency': 70,  # Percent
        'initial_renewable_percentage': 30,  # Percent
        'initial_co2e_emission_per_kwh_fossil': 0.47,  # kg
        'initial_total_electricity_requirement': 4281,  # TWh
        'initial_required_electrolyzer_units': 24437,  # Units
        'initial_total_co2e_emissions': 1409,  # MegaTonnes
    }
    
    # step 1: fetch benchmark data
    benchmark_data = get_benchmark_data()

    # electricity_benchmark_data and co2e_benchmark_data
    electricity_benchmark_data = process_benchmark_data(benchmark_data, 'ElectricityProductionBenchmark')             
    co2e_benchmark_data = process_benchmark_data(benchmark_data, 'CO2eEmissionsBenchmark')

    # plot charts
    # electricity
    electricity_chart_html = plotting_calc_vs_benchmark(
        initial_values['initial_total_electricity_requirement'], 
        electricity_benchmark_data, 
        'Electricity Production', 
        'Total Electricity Requirement (TWh)')
    # co2e
    co2e_chart_html = plotting_calc_vs_benchmark(
        initial_values['initial_total_co2e_emissions'], 
        co2e_benchmark_data, 
        'CO2e Emissions', 
        'CO2e Emissions MegaTonnes')
    
    initial_values.update({'electricity_chart_html': electricity_chart_html, 'co2e_chart_html': co2e_chart_html})

    # context initialization
    context = {'form': HydrogenProductionForm()}
    context.update(initial_values)

    #  reset functionality, return all the values to initial_values
    if request.method == 'POST' and 'reset' in request.POST:
        print("Reset button clicked")
        # Reset the form with initial values
        context = {'form': HydrogenProductionForm(initial=initial_values)}
        context.update(initial_values)
        return render(request, 'h2_prod/hydrogen_production.html', context)

    # calculation and updating values when the sliders are moved
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print("POST request received")
        print("Post Data:", request.POST)

        # convert the POST strings data to float
        post_data = request.POST.copy()
        post_data = post_floater(post_data)

        # Production & electrolizer Efficiency
        total_h2_production = post_data.get('hiddenH2Production', None)
        electrolyzer_efficiency = post_data.get('hiddenElectrolyzerEff', None)
        # Grid renewable percentage & total CO2e emission
        co2e_emission_per_kwh_fossil = post_data.get('hiddenCO2eEmission', None)
        renewable_percentage = post_data.get('hiddenRenewablePct', None)

        # state of CO2e emissions
        current_state_co2e_emission = current_total_co2e_emissions(total_h2_production)

        # calculations for the new state of H2 production, 
        # how much CO2e emission is reduced, and how much electricity is required 
        total_electricity_requirement, total_co2e_emissions, co2e_emissions_reduction, total_h2_production, required_electrolyzer_units = calculate_outputs(
        total_h2_production, electrolyzer_efficiency, renewable_percentage, 
        co2e_emission_per_kwh_fossil, current_state_co2e_emission, electrolyzer_rating)

        # round the total_electricity_requirement and total_co2e_emissions
        rounded_total_electricity_requirement = round(total_electricity_requirement)
        rounded_total_co2e_emissions = round(total_co2e_emissions)
        rounded_total_h2_production = round(total_h2_production)
        rounded_required_electrolyzer_units = round(required_electrolyzer_units)

        # plot charts
        electricity_chart_html = plotting_calc_vs_benchmark(
        initial_values['initial_total_electricity_requirement'], 
        electricity_benchmark_data, 
        'Electricity Production', 
        'Total Electricity Requirement (TWh)')


        # electricity
        electricity_chart_data, electricity_chart_layout  = update_plot_calc_vs_benchmark(
            rounded_total_electricity_requirement, 
            electricity_benchmark_data, 
            'Electricity Production', 
            'Total Electricity Requirement (TWh)')
        # co2e
        co2e_chart_data, co2e_chart_layout = update_plot_calc_vs_benchmark(
            rounded_total_co2e_emissions, 
            co2e_benchmark_data, 
            'CO2e Emissions', 
            'CO2e Emissions MegaTonnes')
        
        # debugging
        print(electricity_chart_data)

        return JsonResponse({
            'total_electricity_requirement': rounded_total_electricity_requirement,
            'total_co2e_emissions': rounded_total_co2e_emissions,
            'co2e_emissions_reduction': co2e_emissions_reduction,
            'total_h2_production': rounded_total_h2_production,
            'required_electrolyzer_units': rounded_required_electrolyzer_units,
            'electricity_chart_data': electricity_chart_data,
            'electricity_chart_layout': electricity_chart_layout,
            'co2e_chart_data': co2e_chart_data,
            'co2e_chart_layout': co2e_chart_layout,
        })

    
    return render(request, 'h2_prod/hydrogen_production.html', context)


def generic_test_view(request):
    if request.method == 'POST':
        # Example of processing POST request
        received_data = request.POST.get('hiddenH2Production', '')
        print("Received data:", received_data)
        response_data = {'status': 'success', 'message': 'Data received'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    # If the request is not POST, you can return a simple HttpResponse
    # return HttpResponse("This is a response from GET request.")
    return render(request, 'h2_prod/test_page.html')


from django.shortcuts import render
# from django.contrib import messages
from .forms import HydrogenProductionForm
from .h2_functions import calculate_outputs, current_total_co2_emissions, calculate_defaults, get_benchmark_data, electrolyzer_rating, post_floater
from .models import ElectricityProductionBenchmark, CO2EmissionsBenchmark
from plotly.offline import plot
import plotly.graph_objects as go
from django.http import HttpResponse
import json



def home(request):
    return render(request, 'home.html')

def hydrogen_production_view(request):
    print("View function called")
    print("Request method:", request.method)
    # Initialize the context with a form instance
    context = {'form': HydrogenProductionForm()}

    if request.method == 'POST':
        print("POST request received")
        print("Post Data:", request.POST)

        post_data = request.POST.copy()
        post_data = post_floater(post_data)



        if 'reset' in request.POST:
            # If the user clicked the reset button, then reset the form 
            form = HydrogenProductionForm() # instantiate a new form which has default values
            default_output = calculate_defaults()
            context = {
                'form': form,
                'total_electricity_requirement': default_output[0],
                'total_co2_emissions': default_output[1],
                'co2_emissions_reduction': default_output[2],
            }
            return render(request, 'h2_prod/hydrogen_production.html', context)

        else:
            # If the user clicked the submit button, then process the data
            
            form = HydrogenProductionForm(post_data)
            if form.is_valid():
                # Get the data from the form, and then process the data in form.cleaned_data

                # CO2 emissions of electricity generation per source
                co2_emission_per_kwh_fossil = post_data.get('hiddenCO2Emission', None)
  
                # Production, Efficiency, etc.
                total_h2_production = post_data.get('hiddenH2Production', None)
                electrolyzer_efficiency = post_data.get('hiddenElectrolyzerEff', None)
                renewable_percentage = post_data.get('hiddenRenewablePct', None)

                # state of CO2 emissions
                current_state_co2_emission = current_total_co2_emissions(total_h2_production)

                # calculations for the new state of H2 production, 
                # how much CO2 emission is reduced, and how much electricity is required 
                total_electricity_requirement, total_co2_emissions, co2_emissions_reduction, total_h2_production, required_electrolyzer_units = calculate_outputs(
                total_h2_production, electrolyzer_efficiency, renewable_percentage, 
                co2_emission_per_kwh_fossil, current_state_co2_emission, electrolyzer_rating)

                # round the total_electricity_requirement and total_co2_emissions
                rounded_total_electricity_requirement = round(total_electricity_requirement)
                rounded_total_co2_emissions = round(total_co2_emissions)
                rounded_total_h2_production = round(total_h2_production)
                required_electrolyzer_units = round(required_electrolyzer_units)


                # Create the bar chart

                # step 1: fetch benchmark data
                benchmark_data = get_benchmark_data()

                # step 2: separate the benchmark data into two lists
                
                # electricity_benchmark_data
                electricity_benchmark_data = sorted(
                    [(int(key.split('-')[1]), benchmark_value, benchmark_name)
                    for key, values in benchmark_data.items() if 'ElectricityProductionBenchmark' in key
                    for benchmark_value, benchmark_name in values],
                    key=lambda x: x[0]
                )

                # co2_benchmark_data
                co2_benchmark_data = sorted(
                    [(int(key.split('-')[1]), benchmark_value, benchmark_name)
                    for key, values in benchmark_data.items() if 'CO2EmissionsBenchmark' in key
                    for benchmark_value, benchmark_name in values],
                    key=lambda x: x[0]
                )

                # benchmark_colors
                benchmark_colors = ['#d53e4f', '#f46d43', '#fdae61']
                reversed_colors = benchmark_colors[::-1]

                # step 3: Prepare data for the chart
                # Electricity data
                electricity_chart_data = [
                    # Add the benchmark data to the chart
                    *[
                    go.Bar(
                        x = [f'{name}'],
                        y = [value],
                        name = f'Benchmark {year}',
                        marker = dict(color=reversed_colors[i])
                    )
                    for i, (year, value, name) in enumerate(electricity_benchmark_data[:3])
                    ],

                    # Add the calculated value to the chart
                    go.Bar(
                        x = ['Your Calculation'],
                        y = [rounded_total_electricity_requirement],
                        name = 'Your Calculation',
                        marker = dict(color='#3288bd')
                    )
                ]

                # CO2 data
                co2_chart_data = [
                    # Add the benchmark data to the chart
                    *[
                    go.Bar(
                        x = [f'{name}'],
                        y = [value],
                        name = f'Benchmark {year}',
                        marker = dict(color=reversed_colors[i])
                    )
                    for i, (year, value, name) in enumerate(co2_benchmark_data[:3])
                    ],

                    # Add the current state of CO2 emissions to produce hydrogen
                    go.Bar(
                        x = ['Current State of CO2 Emissions to produce H2'],
                        y = [round(current_total_co2_emissions(120))],
                        name = 'Your Calculation',
                        marker = dict(color='#9e0142')
                    ),

                    # Add the calculated value to the chart
                    go.Bar(
                        x = ['Your Calculation'],
                        y = [rounded_total_co2_emissions],
                        name = 'Your Calculation',
                        marker = dict(color='#3288bd')
                    )
                ]


                # step 4: Generate the Plotly chart
                # Electricity chart
                electricity_layout = go.Layout(
                    title = {'text':'Electricity Production vs Benchmarks Comparison', 'x':0.5, 'xanchor':'center'},
                    xaxis = dict(title='Benchmark - Year'),
                    yaxis = dict(title='Total Electricity Requirement (TWh)'),
                    showlegend=False
                )

                electricity_fig = go.Figure(data=electricity_chart_data, layout=electricity_layout)

                # CO2 chart
                co2_layout = go.Layout(
                    title = {'text':'CO2 Emissions vs Benchmarks Comparison', 'x':0.5, 'xanchor':'center'},
                    xaxis = dict(title='Benchmark - Year'),
                    yaxis = dict(title='Total CO2 Emissions (MtCO2)'),
                    showlegend=False
                )
                
                co2_fig = go.Figure(data=co2_chart_data, layout=co2_layout)
                

                # step 5: Convert the Plotly chart to HTML
                electricity_chart_html = plot(electricity_fig, output_type='div', include_plotlyjs=False)
                co2_chart_html = plot(co2_fig, output_type='div', include_plotlyjs=False)
           
                # Pass results to the template
                # Construct the context with form and results
                context = {
                    'form': form,
                    'total_electricity_requirement': rounded_total_electricity_requirement,
                    'total_co2_emissions': total_co2_emissions,
                    'co2_emissions_reduction': co2_emissions_reduction,
                    'total_h2_production': rounded_total_h2_production,
                    'required_electrolyzer_units': required_electrolyzer_units,
                    'electricity_chart_html': electricity_chart_html,
                    'co2_chart_html': co2_chart_html,
                }
                print(f'total_electricity_requirement: {rounded_total_electricity_requirement}')
                print(rounded_total_co2_emissions)
                print(co2_benchmark_data)
                print(total_h2_production)

                # Render the template with context
                return render(request, 'h2_prod/hydrogen_production.html', context)

            # If the form is not valid, then render the form with errors
            else:
                print('form is not valid')
                print("Form errors:", form.errors)
                context = {'form': form}
                print(request.POST)
    
    # Render the template with context
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


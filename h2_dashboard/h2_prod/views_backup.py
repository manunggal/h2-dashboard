from django.shortcuts import render
# from django.contrib import messages
from .forms import HydrogenProductionForm
from .h2_functions import calculate_outputs, current_total_co2_emissions, calculate_defaults

def home(request):
    return render(request, 'home.html')

def hydrogen_production_view(request):
    # Initialize the context with a form instance
    context = {'form': HydrogenProductionForm()}

    if request.method == 'POST':

        if 'reset' in request.POST:
            # If the user clicked the reset button, then reset the form 
            form = HydrogenProductionForm() # instantiate a new form which has default values
            default_output = calculate_defaults()
            context = {
                'form': form,
                'default_total_electricity_requirement': 1,
                'default_total_co2_emissions': 2,
                'co2_emission_reduction': default_output[2],
            }
            return render(request, 'h2_prod/hydrogen_production.html', context)

        else:
            # If the user clicked the submit button, then process the data
            
            form = HydrogenProductionForm(request.POST)
            if form.is_valid():
                # Get the data from the form, and then process the data in form.cleaned_data
                # h2 emissions per source
                h2_from_natural_gas = form.cleaned_data['h2_from_natural_gas']
                h2_from_coal = form.cleaned_data['h2_from_coal']
                h2_from_oil = form.cleaned_data['h2_from_oil']
                h2_from_electrolysis = form.cleaned_data['h2_from_electrolysis']

                # CO2 emissions of electricity generation per source
                co2_emission_per_kwh_fossil = form.cleaned_data['co2_emission_per_kwh_fossil']
                co2_emission_per_kwh_renewable = form.cleaned_data['co2_emission_per_kwh_renewable']

                # Production, Efficiency, etc.
                total_h2_production = form.cleaned_data['total_h2_production']
                electrolyzer_efficiency = form.cleaned_data['electrolyzer_efficiency']
                renewable_percentage = form.cleaned_data['renewable_percentage']

                # state of CO2 emissions
                current_state_co2_emission = current_total_co2_emissions(total_h2_production)

                # calculations for the new state of H2 production, 
                # how much CO2 emission is reduced, and how much electricity is required 
                total_electricity_requirement, total_co2_emission, co2_emission_reduction = calculate_outputs(
                total_h2_production, electrolyzer_efficiency, renewable_percentage, 
                co2_emission_per_kwh_fossil, co2_emission_per_kwh_renewable, current_state_co2_emission)

                # Pass results to the template
                # Construct the context with form and results
                context = {
                    'form': form,
                    'total_electricity_requirement': total_electricity_requirement,
                    'total_co2_emission': total_co2_emission,
                    'co2_emission_reduction': co2_emission_reduction,
                    # Add other context variables as needed
                }
                
                # Render the template with context
                return render(request, 'h2_prod/hydrogen_production.html', context)

            # If the form is not valid, then render the form with errors
            else:
                context = {'form': form}

    # Render the template with context
    return render(request, 'h2_prod/hydrogen_production.html', context)

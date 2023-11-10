from django import forms

class HydrogenProductionForm(forms.Form):

    # Sliders for CO2 emissions per source
    # H2 derived from natural gas
    h2_from_natural_gas = forms.IntegerField(
        label='H2 derived from natural gas',
        min_value=10,
        max_value=14,
        initial=12,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )

    # H2 derived from coal
    h2_from_coal = forms.IntegerField(
        label='H2 derived from coal',
        min_value=10,
        max_value=14,
        initial=12,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )

    # H2 derived from oil
    h2_from_oil = forms.IntegerField(
        label='H2 derived from oil',
        min_value=10,
        max_value=14,
        initial=12,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )

    # H2 derived from electrolysis
    h2_from_electrolysis = forms.IntegerField(
        label='H2 derived from electrolysis',
        min_value=10,
        max_value=14,
        initial=12,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )



    # Sliders for Production, Efficiency, etc.
    # Total H2 production
    total_h2_production = forms.IntegerField(
        label='Total H2 Production (megatonnes per year)',
        min_value=0,
        max_value=200,
        initial=90,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '5'})
    )

    # Electrolyzer efficiency
    electrolyzer_efficiency = forms.IntegerField(
        label='Electrolyzer Efficiency (%)',
        min_value=0,
        max_value=100,
        initial=70,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )

    # Percentage of renewable energy used for electrolysis
    renewable_percentage = forms.IntegerField(
        label='Percentage of Renewable Energy Used for Electrolysis (%)',
        min_value=0,
        max_value=100,
        initial=30,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )

    # sliders for CO2 emissions for fossil fuels in electric generation
    co2_emission_per_kwh_fossil = forms.FloatField(
        label='CO2 Emission per kWh from Fossil Fuels',
        min_value=0.0,
        max_value=1.0,
        initial=0.39,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '0.01'})
    )

    co2_emission_per_kwh_renewable = forms.FloatField(
        label='CO2 Emission per kWh from Renewable Sources',
        min_value=0.0,
        max_value=1.0,
        initial=0.0,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '0.01'})
    )

    # Add similar fields for electrolyzer efficiency and percentage renewable

    # Note: You can customize this form to match exactly what you need, including proper validation.

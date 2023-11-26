from django import forms

class HydrogenProductionForm(forms.Form):

     # Sliders for Production, Efficiency, etc.
    # Total H2 production
    hiddenH2Production = forms.IntegerField(
        label='Total H2 Production (megatonnes per year)',
        min_value=0,
        max_value=200,
        initial=90,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '5'})
    )

    # Electrolyzer efficiency
    hiddenElectrolyzerEff = forms.IntegerField(
        label='Electrolyzer Efficiency (%)',
        min_value=0,
        max_value=100,
        initial=70,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )

    # Percentage of renewable energy used for electrolysis
    hiddenRenewablePct = forms.IntegerField(
        label='Percentage of Renewable Energy Used for Electrolysis (%)',
        min_value=0,
        max_value=100,
        initial=30,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )

    # sliders for CO2 emissions for fossil fuels in electric generation
    hiddenCO2Emission = forms.FloatField(
        label='CO2 Emission per kWh from Fossil Fuels',
        min_value=0.0,
        max_value=1.0,
        initial=0.47, # https://www.iea.org/reports/global-energy-co2-status-report-2019/emissions
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '0.01'})
    )



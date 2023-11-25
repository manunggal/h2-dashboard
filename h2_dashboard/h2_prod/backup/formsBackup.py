from django import forms

class HydrogenProductionForm(forms.Form):

    # Sliders for CO2 emissions per source (# kg CO2e per kg H2)
    # H2 derived from natural gas
    sliderNatGas = forms.IntegerField(
        label='H2 derived from natural gas',
        min_value=10,
        max_value=14,
        initial=12,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )

    # H2 derived from coal
    sliderCoal = forms.IntegerField(
        label='H2 derived from coal',
        min_value=22,
        max_value=26,
        initial=24,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )

    # H2 derived from oil
    sliderOil = forms.IntegerField(
        label='H2 derived from oil',
        min_value=16,
        max_value=20,
        initial=18,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )

    # H2 derived from electrolysis
    sliderElectrolysis = forms.IntegerField(
        label='H2 derived from electrolysis',
        min_value=20,
        max_value=24,
        initial=22,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )



    # # Sliders for Production, Efficiency, etc.
    # # Total H2 production
    # SliderH2Production = forms.IntegerField(
    #     label='Total H2 Production (megatonnes per year)',
    #     min_value=0,
    #     max_value=200,
    #     initial=90,
    #     widget=forms.NumberInput(attrs={'type': 'range', 'step': '5'})
    # )

    # # Electrolyzer efficiency
    # SliderElectrolyzerEff = forms.IntegerField(
    #     label='Electrolyzer Efficiency (%)',
    #     min_value=0,
    #     max_value=100,
    #     initial=70,
    #     widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    # )

    # # Percentage of renewable energy used for electrolysis
    # SliderRenewablePct = forms.IntegerField(
    #     label='Percentage of Renewable Energy Used for Electrolysis (%)',
    #     min_value=0,
    #     max_value=100,
    #     initial=30,
    #     widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    # )

    # # sliders for CO2 emissions for fossil fuels in electric generation
    # SliderCO2Emission = forms.FloatField(
    #     label='CO2 Emission per kWh from Fossil Fuels',
    #     min_value=0.0,
    #     max_value=1.0,
    #     initial=0.475, # https://www.iea.org/reports/global-energy-co2-status-report-2019/emissions
    #     widget=forms.NumberInput(attrs={'type': 'range', 'step': '0.01'})
    # )



from django import forms

class HydrogenProductionForm(forms.Form):
    # Sliders for CO2 emissions per source
    h2_from_natural_gas = forms.IntegerField(
        label='H2 derived from natural gas',
        min_value=10,
        max_value=14,
        initial=12,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '1'})
    )
    # Add similar fields for coal, oil, and electrolysis

    # Sliders for Production, Efficiency, etc.
    total_h2_production = forms.IntegerField(
        label='Total H2 Production (megatonnes per year)',
        min_value=0,
        max_value=200,
        initial=90,
        widget=forms.NumberInput(attrs={'type': 'range', 'step': '5'})
    )
    # Add similar fields for electrolyzer efficiency and percentage renewable

    # Note: You can customize this form to match exactly what you need, including proper validation.

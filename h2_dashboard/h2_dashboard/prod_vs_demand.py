import plotly.graph_objects as go

# Data for hydrogen production in 2021 (percentages)
production_data = {
    'Natural Gas': 47,
    'Coal': 27,
    'Oil': 22,
    'Electrolysis': 4
}

# Total global hydrogen production in 2021 in million tonnes (assumed value)
# Note: Actual value will be needed for accurate representation
total_production_mt = 100  # Replace with actual value

# Convert production percentages to million tonnes
production_mt = {source: (percent / 100) * total_production_mt for source, percent in production_data.items()}

# Demand data in million tonnes
demand_data = {
    'Refining': 39.82,
    'Chemicals': 48.40,
    'Iron and Steel': 5.16,
    'Other Industry': 0.91,
    'Other': 0.04
}

# Creating nodes for the Sankey diagram
labels = list(production_mt.keys()) + list(demand_data.keys())

# Creating source, target, and value arrays for the Sankey diagram
source = []
target = []
value = []

# Adding production to demand links
for i, production_source in enumerate(production_mt):
    for j, demand_sector in enumerate(demand_data, start=len(production_mt)):
        source.append(i)
        target.append(j)
        # Distribute production evenly across demand sectors
        value.append(production_mt[production_source] * (demand_data[demand_sector] / total_production_mt))

# Creating the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=source,
        target=target,
        value=value
    ))])

fig.update_layout(title_text="Global Hydrogen Flow in 2021", font_size=10)
fig.show()

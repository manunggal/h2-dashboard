import pandas as pd
import plotly.express as px

# Hydrogen production data
production_data = {
    "Source": ["Natural Gas", "Coal", "Other"],
    "Production": [52.5, 16.5, 1.0]
}

# Hydrogen consumption data
consumption_data = {
    "Nature of Consumption": ["Ammonia Production", "Oil Refining", "Methanol Production", "Other"],
    "Consumption": [37.8, 16.8, 7.4, 8.0]
}

# Convert data to DataFrames
production_df = pd.DataFrame(production_data)
consumption_df = pd.DataFrame(consumption_data)

# Merge production and consumption data
merged_df = pd.merge(production_df, consumption_df, on="Source")

# Create Sankey diagram using Plotly Express
fig = px.sankey(
    merged_df,
    linksource="Source",
    linktarget="Nature of Consumption",
    values="Production",
    color="Source",
    title="Hydrogen Production and Consumption Sankey Diagram"
)

# Show the Sankey diagram
fig.show()

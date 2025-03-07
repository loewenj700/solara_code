import solara
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv('happiness_years02.csv')

# Standardize column names (for consistency across datasets)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Extract years directly from column names (excluding 'country')
years = [col for col in df.columns if col != 'country']
selected_year = solara.reactive(years[0])

@solara.component
def Page():
    with solara.Column(style={"padding": "20px"}):
        solara.Markdown("## Select a year to view global happiness scores by country.")
        solara.Select(label="Year", values=years, value=selected_year)
    # Prepare data for the selected year
    year_data = df[['country', selected_year.value]].rename(columns={selected_year.value: 'happiness_score'})

    # Drop rows with missing values (in case some countries have no data for that year)
    year_data = year_data.dropna()

    # Create choropleth map
    fig_map = px.choropleth(
        year_data,
        locations='country',
        locationmode='country names',
        color='happiness_score',
        hover_name='country',
        color_continuous_scale='Blues',
        title=f'Global Happiness Scores - {selected_year.value}'
    )
    fig_map.update_geos(projection_type='equirectangular', showcoastlines=True)

    # Display the map
    solara.FigurePlotly(fig_map)

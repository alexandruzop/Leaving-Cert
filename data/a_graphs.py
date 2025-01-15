"""
-open cleaned datasets
-create interactive sites using dash & plotly
-output graphs as div elements to be uploaded to site
"""

# MODULES
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import folium
from folium import Choropleth
import json

                                                
                                                
                                            # YEARLY DATA INDEX


# Read data
file_path_index = "st_index.csv"
data = pd.read_csv(file_path_index)


# Defining lines
Dublin = 'Dublin Mean'  
National = 'National Mean'  
National_Excl_Dublin = 'National Excl Dublin Mean'  
Year = 'Year'    

#making table space
fig = go.Figure()

#making lines
fig.add_trace(go.Scatter(
    x=data[Year],
    y=data[Dublin],
    mode='lines',
    name=Dublin,
    #adding hover 
    hoverinfo='x+y'
))

 
fig.add_trace(go.Scatter(
    x=data[Year],
    y=data[National],
    mode='lines',
    name=National,
    hoverinfo='x+y'
))


fig.add_trace(go.Scatter(
    x=data[Year],
    y=data[National_Excl_Dublin],
    mode='lines',
    name=National_Excl_Dublin,
    hoverinfo='x+y'
))

#creating layout
fig.update_layout(
    title='Housing Index Growth',
    title_x=0.5,
    xaxis_title='Date',
    yaxis_title='Index Value',

    #legend placement
    legend=dict(
        yanchor="top",
        y=0.95, 
        xanchor="center",
        x=0.5,  
        orientation="h",

        #legend styling
        font=dict(size=10),  
        bgcolor='rgba(255, 255, 255, 0.7)',  
        bordercolor='black',  
        borderwidth=1        
    )
)


#output to html
output_index = "a.annual_index.html"
fig.write_html(output_index)






                                    #YEARLY RENT


file_path_rent = 'st_rent.csv'
data = pd.read_csv(file_path_rent)

# Defining data columns
Dublin = 'Dublin Mean Rent'  
Rest_Of_Country = 'Rest of Country Mean Rent'  
Year = 'Year'    

# Creating the figure
fig = go.Figure()

# Adding an area trace for Dublin Mean Rent
fig.add_trace(go.Scatter(
    x=data[Year],
    y=data[Dublin],
    mode='lines',
    name=Dublin,
    fill='tozeroy',  # Fills the area under the line to the x-axis
    line=dict(color='#FF6F61'),  # Line color
    fillcolor='rgba(255, 111, 97, 0.5)',  # Semi-transparent fill color
    hoverinfo='x+y'
))

# Adding an area trace for Rest of Country Mean Rent
fig.add_trace(go.Scatter(
    x=data[Year],
    y=data[Rest_Of_Country],
    mode='lines',
    name=Rest_Of_Country,
    fill='tonexty',  # Fills the area between this trace and the previous one
    line=dict(color='#6BAED6'),  # Line color
    fillcolor='rgba(107, 174, 214, 0.5)',  # Semi-transparent fill color
    hoverinfo='x+y'
))

# Updating layout
fig.update_layout(
    title='Average Yearly Rent (€)',
    title_x=0.5,
    xaxis_title='Year',
    yaxis_title='Rent Price',

    # Legend placement
    legend=dict(
        yanchor="top",
        y=0.95, 
        xanchor="center",
        x=0.5,  
        orientation="h",

        # Legend styling
        font=dict(size=10),  
        bgcolor='rgba(255, 255, 255, 0.7)',  
        bordercolor='black',  
        borderwidth=1        
    )
)

# Output to HTML
# Uses Plotly library to create Python graph and output to an HTML file that is read as a div on your interface
output_index_rent = "a.annual_rent.html"
fig.write_html(output_index_rent)



                            #HOMELESS HEATMAP


#reading geojson & csv
geojson_path = 'ireland-with-counties_.geojson'
data_path = 'st_homeless_heatmap.csv'

#load geojson with module
with open(geojson_path, 'r') as file:
    geojson_content = json.load(file)

#load data from csv
homeless_data = pd.read_csv(data_path)

#define regions (manually done as not part of geojson)
#values found from wikipedia article
regions = {
    "Dublin": ["Dublin", "Dublin City", "South Dublin", "Fingal", "Dún Laoghaire-Rathdown"],
    "Mid-East": ["Kildare", "Kildare County", "Meath", "Meath County", "Louth", "Louth County", "Wicklow", "Wicklow County"],
    "Midlands": ["Laois", "Laois County", "Offaly", "Offaly County", "Westmeath", "Westmeath County", "Longford", "Longford County", "Roscommon", "Roscommon County"],
    "Mid-West": ["Limerick", "Limerick City", "Limerick County", "Clare", "Clare County", "Tipperary", "North Tipperary", "South Tipperary", "Galway", "Galway City", "Galway County"],
    "North-West": ["Cavan", "Cavan County", "Donegal", "Donegal County", "Leitrim", "Leitrim County", "Monaghan", "Monaghan County", "Sligo", "Sligo County", "Mayo", "Mayo County"],
    "South-East": ["Kilkenny", "Kilkenny County", "Wexford", "Wexford County", "Waterford", "Waterford City", "Waterford County", "Carlow", "Carlow County", "Tipperary", "North Tipperary", "South Tipperary"],
    "South-West": ["Cork", "Cork City", "Cork County", "Kerry", "Kerry County"],
}

#normalize name
def normalize_name(name):
    return name.replace(" City", "").replace(" County", "").replace("DÃºn", "Dún").strip()

#adding region feature to geojson file
#iterates through each feature in geojson file
for feature in geojson_content['features']:
    #normalize name
    county_name = normalize_name(feature['properties']['name'])
    #iterates through each county in regions
    for region, counties in regions.items():
        #normalize county names
        normalized_counties = [normalize_name(c) for c in counties]
        #if county name in normalized counties
        if county_name in normalized_counties:
            #add region to properties
            feature['properties']['Region'] = region
            #break loop if county found
            break
    #if county not found
    else:
        #add unknown to properties
        feature['properties']['Region'] = "Unknown"

#check unmatched counties
unmatched_counties = [feature['properties']['name'] for feature in geojson_content['features'] if feature['properties']['Region'] == "Unknown"]

#make dictionary of region & homeless data
region_homeless = homeless_data.set_index('Region')['Total'].to_dict()

#map geojson & data
for feature in geojson_content['features']:
    #get region name from properties
    region_name = feature['properties'].get('Region', 'Unknown')
    #add homeless data to properties
    feature['properties']['Homeless'] = region_homeless.get(region_name, 'Data not available')

#make folium map focused on ireland with coordinates
region_map = folium.Map(location=[53.1424, -7.6921], zoom_start=7)

#define colour interval 
threshold_scale = [0, 50, 100, 200, 400, 600, 800, 1000, 8000]

#add choropleth layer to map
folium.Choropleth(
    #add geojson & data
    geo_data=geojson_content,
    data=homeless_data,
    #match region with data
    columns=['Region', 'Total'],
    #styling
    key_on='feature.properties.Region', 
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Homeless Population by Region',
    #apply defined scale
    threshold_scale=threshold_scale,
    #hover
    highlight=True  
).add_to(region_map)

#add tooltip to map to display region & data
folium.GeoJson(
    geojson_content,
    style_function=lambda feature: {
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['Region', 'Homeless'],
        aliases=['Region:', 'Homeless Population:'],
        localize=True,
        sticky=True,
    )
).add_to(region_map)



# Save the map to an HTML file
region_map.save('a_heatmap.html')


                            #HOMELESS PIE CHART

# Read CSV
file_path = "st_homeless_piechart.csv"
homeless_data = pd.read_csv(file_path)

# Filter columns
homeless_pie_data = homeless_data[['Age Interval', 'Total']].dropna()

#defining colours
#palette gotten from Adobe colour
pie_colors = {
    "18-24": "#2F00FA",
    "25-44": "#D300FA",
    "45-64": "#FA00AC",
    "65+": "#8100FA"
}

#pie chart
fig = px.pie(
    homeless_pie_data,
    names='Age Interval',
    values='Total',
    title='Homeless People per Age Interval',
    # Styling
    color='Age Interval',  
    color_discrete_map=pie_colors
)


# Layout customization
fig.update_layout(
    title_font_size=20,
    title_x=0.5,  # Center title
    showlegend=True,
    legend=dict(
        font=dict(size=10),
        orientation="h",
        xanchor="center",
        x=0.5,
        y=-0.1
    )
)

#add shading & shadows
fig.update_traces(
    #slices pulled out
    pull=[0.05] * len(homeless_pie_data),  
    marker=dict(
        #border
        line=dict(color='black', width=1),  
            
    )
)

# Output to HTML
output_file = "a_piechart.html"
fig.write_html(output_file)

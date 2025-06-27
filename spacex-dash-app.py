# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
site = list(spacex_df['Launch Site'].unique())
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options = [{'label': 'All Sites', 'value': 'ALL'},
                                {'label':site[0], 'value': site[0]},
                                {'label':site[1], 'value': site[1]},
                                {'label':site[2], 'value': site[2]},
                                {'label':site[3], 'value': site[3]},
                                ],
                                value = 'ALL',
                                placeholder = 'Select Site',
                                searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min = 0, max = 10000,
                                step = 1000,
                                value = [min_payload, max_payload] 
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Pie Chart for Success At All Sites')
        return fig
    else:
        selected_df = filtered_df[filtered_df['Launch Site']== entered_site]
        fig = px.pie(selected_df,  
        names='class', 
        title='Pie Chart for Success At Site {}'.format(entered_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
[Input(component_id = 'site-dropdown', component_property = 'value'),
Input(component_id = 'payload-slider', component_property = 'value')])

def get_scatter_plot(entered_site, value):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        selected_df = filtered_df[(value[0]<=filtered_df['Payload Mass (kg)']) & 
        (filtered_df['Payload Mass (kg)']<=value[1])]
        print(selected_df.head())
        fig = px.scatter(selected_df,
        x = 'Payload Mass (kg)',
        y = 'class',
        color = 'Booster Version Category',
        title = 'Correlation between Payload and Success for All Sites')
        return fig
    else:
        site_df = filtered_df[filtered_df['Launch Site']==entered_site]
        selected_df = site_df[(value[0]<=site_df['Payload Mass (kg)']) &
        (site_df['Payload Mass (kg)']<=value[1])]
        print(selected_df.head())
        fig = px.scatter(selected_df,
        x = 'Payload Mass (kg)',
        y = 'class',
        color = 'Booster Version Category',
        title = 'Correlation between Payload and Success for {} Site'. format(entered_site))
        return fig
# Run the app
if __name__ == '__main__':
    app.run()

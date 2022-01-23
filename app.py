#migrated
###### Import the needed libraries
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


###### Read in the data
cchange = pd.read_csv('resources/combinedwrldbnkdata.csv')

###### Intiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'World Bank Economic and Climate Change Indicators - 2014 - 2020'
githublink = 'https://git.generalassemb.ly/mdsheppard/global-dev'
sourceurl = 'https://data.worldbank.org/topic/climate-change?view=chart'

###### Define the Layout
app.layout = html.Div([html.Div([html.H1("World Bank Economic and Climate Change Indicators")],
                                style={'textAlign': "center", "padding-bottom": "30"}),
                       html.Div([html.Span("Choose a metric:   ", className="six columns",
                                           style={"text-align": "right", "width": "40%", "padding-top": 5}),
                                 dcc.Dropdown(id="value-selected", value='Electricity_2018',
                                              options=[{'label': "Access to electricity (% of population) - 2018", 'value': 'Electricity_2018'},
                                                       {'label': "Mortality rate, under-5 (per 1,000  live births) - 2018", 'value': 'Mortality_2018'}
                                                       {'label': "GDP per capita (current $USD) - 2020", 'value': 'gdppc_2020'}
                                                       {'label': "Electricity Consumption (kWh per capita) - 2014", 'value': 'Electr_Cons_2014'}
                                                       {'label': "CO2 emissions (metric tons per capita) - 2018", 'value': 'CO2percap_2018'}],
                                              style={"display": "block", "margin-left": "auto", "margin-right": "auto",
                                                     "width": "100%"},
                                              className="six columns")], className="row"),
                       dcc.Graph(id="my-graph"),
                       html.A('Code on Github', href=githublink),
                       html.Br(),
                       html.A('Data Source', href=sourceurl),
                       ], className="container")

###### Define the callback and functions

@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("value-selected", "value")]
)
def update_figure(selected):
    dff = cchange.groupby(['Country Code', 'Country Name']).mean().reset_index()
    def title(text):
        if text == "Electricity_2018":
            return "% of the population with access to electricity"
        elif text == "Mortality_2018":
            return "Child mortality (<5) levels, # per 1,000 births"
        elif text == "gdppc_2020":
            return "GDP per capita"
        elif text == "Electr_Cons_2014":
            return "Electricity Consumption (kWh per capita)"
        else:
            return "Metric tons of emissions per capita"
    trace = go.Choropleth(locations=dff['Country Code'],z=dff[selected],text=dff['Country Name'],autocolorscale=False,
                          colorscale="viridis",marker={'line': {'color': 'rgb(180,180,180)','width': 0.9}},
                          colorbar={"thickness": 30,"len": 0.7,"x": 1.1,"y": 0.5,
                                    'title': {"text": title(selected), "side": "bottom"}})
    return {"data": [trace],
            "layout": go.Layout(title=title(selected),height=800,geo={'showframe': False,
                                                                      'showlakes': True,
                                                                      'showocean': True,
                                                                      'showcoastlines': True,
                                                                      'projection': {'type': "orthographic"}})}


###### Execute the app
if __name__ == '__main__':
    app.run_server(debug=True)

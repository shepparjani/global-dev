###### Import the needed libraries
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


###### Read in the data
hiv = pd.read_csv('resources/hiv_statistics_combined.csv')


###### Intiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Global HIV Statistics for 2018'
githublink = 'https://github.com/austinlasseter/hiv-statistics#global-hiv-statistics-for-2018'
sourceurl = 'http://apps.who.int/gho/data/node.main.618?lang=en'

###### Define the Layout
app.layout = html.Div([html.Div([html.H1("Global HIV Statistics for 2018")],
                                style={'textAlign': "center", "padding-bottom": "30"}),
                       html.Div([html.Span("Choose a metric:   ", className="six columns",
                                           style={"text-align": "right", "width": "40%", "padding-top": 5}),
                                 dcc.Dropdown(id="value-selected", value='d_total',
                                              options=[{'label': "Number of Deaths Due to HIV/AIDS", 'value': 'd_total'},
                                                       {'label': "Number of People Living with HIV", 'value': 'l_total'},
                                                       {'label': "Number of New HIV Infections", 'value': 'n_total'}],
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
    dff = hiv.groupby(['iso_alpha3', 'country_name']).mean().reset_index()
    def title(text):
        if text == "d_total":
            return "Number of Deaths Due to HIV/AIDS"
        elif text == "l_total":
            return "Number of People Living with HIV"
        else:
            return "Number of New HIV Infections"
    trace = go.Choropleth(locations=dff['iso_alpha3'],z=dff[selected],text=dff['country_name'],autocolorscale=False,
                          colorscale="plasma",marker={'line': {'color': 'rgb(180,180,180)','width': 0.9}},
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

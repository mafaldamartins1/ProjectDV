# Import packages
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dataset import df
import plotly.express as px

################################### INTERACTIVE COMPONENTS ###################################

# Slider for the year choice
range_slider = dcc.RangeSlider(
    id = 'range_slider',
    min = df['Execution Year'].min(),
    max = df['Execution Year'].max(),
    marks = {str(i): '{}'.format(str(i)) for i in
           [1977, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023]},
    value = [df['Execution Year'].min(), df['Execution Year'].max()],
    tooltip={"placement": "bottom", "always_visible": True},
    step = 1
)

# Dropdown for sex
sex_dropdown = dcc.Dropdown(
    id = 'sex_dropdown',
    options = df['Sex'].unique(),
    multi = True,
    clearable = True,
    searchable=False,
    placeholder= "Select a sex"
)

# Dropdown for race
race_dropdown = dcc.Dropdown(
    id = 'race_dropdown',
    options = df['Race'].unique(),
    multi = True,
    clearable = True,
    searchable= False,
    placeholder= "Select a race"
)

# Checkbox item to select volunteers
volunteer_checkbox = dcc.Checklist(
    id = 'volunteer_checkbox',
    options = [{'label': 'Execution Volunteer', 'value': 'yes'}],
    value=[]
)

# Checkbox item to select foreign nationals
foreign_checkbox  = dcc.Checklist(
    id = 'foreign_checkbox',
    options = [{'label': 'Foreign National', 'value': 'Yes'}],
    value=[]
)

################################### APP ###################################

app = dash.Dash(__name__)

server = app.server

#################### APP LAYOUT ####################

app.layout = html.Div([
    html.Div([
        html.H1('Execution in US')
    ], id='Title row', className='title_box'),
    html.Br(),
    html.Br(),
    html.Div([
        sex_dropdown,
    ],),
    html.Div([
        html.Div([
            volunteer_checkbox
        ]),
        html.Br(),
        html.Div([
            foreign_checkbox
        ])
    ]),

    html.Div([
        range_slider
    ]),
    html.Br(),
    html.Br(),

    html.Div([
        html.Div([
            html.Div([
                html.Label(id = 'map_title'),
            ]),
            html.Div([
                race_dropdown,
            ]),
            dcc.Graph(id='usa_map'),
        ])
    ])

])

################################### CALLBACKS ###################################

@app.callback(
    [
        Output('map_title', 'children'),
        Output('usa_map', 'figure')
    ],
    [
        Input('range_slider', 'value'),
        Input('sex_dropdown', 'value'),
        Input('race_dropdown', 'value'),
        Input('volunteer_checkbox', 'value'),
        Input('foreign_checkbox', 'value')
    ]
)
### VISUALIZATION 1- USA MAP
def plot_map(range_slider, sex_dropdown, race_dropdown, volunteer_checkbox, foreign_checkbox):
    filtered_df = df[(df['Execution Year'] >= range_slider[0]) & (df['Execution Year'] <= range_slider[1])]

    if sex_dropdown:
        filtered_df = filtered_df[filtered_df['Sex'].isin(sex_dropdown)]

    if race_dropdown:
        filtered_df = filtered_df[filtered_df['Race'].isin(race_dropdown)]

    if 'yes' in volunteer_checkbox:
        filtered_df = filtered_df[filtered_df['Execution Volunteer'] == 'yes']

    if 'Yes' in foreign_checkbox:
        filtered_df = filtered_df[filtered_df['Foreign National'] == 'Yes']

    executions_by_state = filtered_df.groupby('State')['State'].count().reset_index(name='Executions')

    map_title = f'Total number of executions by state'

    fig = px.choropleth(data_frame=executions_by_state,
                        locations='State',
                        locationmode="USA-states",
                        scope="usa",
                        height=600,
                        color='Executions',
                        color_continuous_scale='reds',
                        range_color=(0, executions_by_state['Executions'].max()),
                        labels={'Executions': 'Number of Executions'})

    return fig, map_title


################################### END OF THE APP ###################################

if __name__ == '__main__':
    app.run_server(debug=True)
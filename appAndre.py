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

counts = df.groupby(['Execution Date', 'Race']).size().reset_index(name='Count')


################################### APP ###################################

app = dash.Dash(__name__)

server = app.server

#################### APP LAYOUT ####################

app.layout = html.Div([
    html.Div([
            html.Img(
                src='/assets/logo.png',
                style={
                    'height': '50px',
                    'display': 'inline-block',
                    'margin-right': '15px',
                    'vertical-align': 'top'
                }
            ),
            html.H1(
                'Executions in US',
                style={
                    'display': 'inline-block',
                    'vertical-align': 'top',
                    'margin': '0',
                    'text-align': 'center',
                    'width': '100%'
                }
            )
        ],
        id='Title row',
        className='title_box',
        style={'display': 'flex'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Div([
                sex_dropdown,
            ], style={'text-align': 'center','width': '300px'}),
            html.Div([
                volunteer_checkbox,
                foreign_checkbox,
            ], style={'margin-top': '20px'}),
        ], style={'display': 'flex', 'align-items': 'center'}),
        html.Br(),
        html.Div([
            range_slider,
        ], style={'width': '700px'}),
    ], style={'margin': 'auto', 'max-width': '800px', 'display': 'flex', 'flex-direction': 'column',
              'align-items': 'center'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Label(id='map_title'),
        ], style={'text-align': 'center', 'padding-bottom': '10px', 'font-weight': 'bold', 'font-size': '20px', 'width': '350px', 'margin-left': '300px'}),
            html.Div([
                race_dropdown
            ], style={'text-align': 'center', 'width': '350px', 'margin-left': '300px'}),
            dcc.Graph(id='usa_map'),
        ], style={'display': 'inline-block', 'width': '70%', 'text-align': 'center'}),
        html.Div([
            html.Div([
                html.Label(id='pie_title'),
            ], style={'text-align': 'center', 'padding-bottom': '7px', 'font-weight':'bold', 'font-size': '20px'}),
            html.Div([
                dcc.Graph(id='nested_pie_chart')
            ])
        ], style={'display': 'inline-block', 'width': '30%'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Label(id='matrix_title'),
        ], style={'text-align': 'center', 'padding-bottom': '10px', 'font-weight': 'bold', 'font-size': '20px',
                  'width': '350px', 'margin-left': '300px'}),
        html.Div([
            dcc.Graph(id='matrix'),
        ], style={'display': 'inline-block', 'width': '50%', 'text-align': 'center'}),
        html.Div([
            html.Div([
                html.Label(id='linechart_title'),
            ], style={'text-align': 'center', 'padding-bottom': '7px', 'font-weight': 'bold', 'font-size': '20px'}),
            html.Div([
                dcc.Graph(id='linechart')
            ]),
            html.Div([
                html.Label(id='scatter_fig_title'),], style={'text-align': 'center', 'padding-bottom': '5px', 'font-weight': 'bold', 'font-size': '20px'}),
            html.Div([
                dcc.Graph(id='scatter_fig')
            ])
        ], style={'display': 'inline-block', 'width': '50%', 'margin-top': '50px'}),
    ])
])

sex_dropdown.style = {'margin-top': '20px', 'margin-left': '-15px'}

################################### CALLBACKS ###################################

@app.callback(
    [
        Output('map_title', 'children'),
        Output('usa_map', 'figure'),
        Output('pie_title', 'children'),
        Output('nested_pie_chart', 'figure'),
        Output('linechart_title','children'),
        Output('linechart', 'figure'),
        Output('matrix_title', 'children'),
        Output('matrix', 'figure'),
        Output('scatter_fig', 'figure')
    ],
    [
        Input('range_slider', 'value'),
        Input('sex_dropdown', 'value'),
        Input('race_dropdown', 'value'),
        Input('volunteer_checkbox', 'value'),
        Input('foreign_checkbox', 'value')
    ]
)

def plot(range_slider, sex_dropdown, race_dropdown, volunteer_checkbox, foreign_checkbox):
    filtered_df = df[(df['Execution Year'] >= range_slider[0]) & (df['Execution Year'] <= range_slider[1])]

    if sex_dropdown:
        filtered_df = filtered_df[filtered_df['Sex'].isin(sex_dropdown)]

    if 'yes' in volunteer_checkbox:
        filtered_df = filtered_df[filtered_df['Execution Volunteer'] == 'yes']

    if 'Yes' in foreign_checkbox:
        filtered_df = filtered_df[filtered_df['Foreign National'] == 'Yes']

    ### VISUALIZATION 1- USA MAP
    if race_dropdown:
        filtered_df_map = filtered_df[filtered_df['Race'].isin(race_dropdown)]
        executions_by_state = filtered_df_map.groupby('State Code')['State Code'].count().reset_index(name='Executions')
        executions_by_state['State'] = filtered_df_map['State']
    else:
        executions_by_state = filtered_df.groupby('State Code')['State Code'].count().reset_index(name='Executions')
        executions_by_state['State'] = filtered_df['State']

    map_title = f'Total number of executions by state'

    fig1 = px.choropleth(data_frame=executions_by_state,
                        locations='State Code',
                        locationmode="USA-states",
                        scope="usa",
                        height=600,
                        color='Executions',
                        color_continuous_scale='reds',
                        range_color=(0, executions_by_state['Executions'].max()),
                        labels={'Executions': 'Number of Executions'},
                        hover_data={'State':True, 'Executions':True})

    ### VISUALIZATION 2- NESTED PIE CHART
    pie_title = f'Number of executions by sex and race'

    filtered_df_grouped = filtered_df.groupby(['Sex', 'Race']).size().reset_index(name='Executions')

    fig2 = px.sunburst(data_frame=filtered_df_grouped,
                       path=['Sex', 'Race'],
                       values='Executions',
                       color='Race')

    ### VISUALIZATION 3 - LINE CHART
    linechart_title = f'Executions per Race over time'

    executions_by_race_by_year = filtered_df.groupby(['Race', 'Execution Year']).size().reset_index(name='Executions')

    linechart = px.line(executions_by_race_by_year, x="Execution Year", y='Executions', color='Race', height=400)

    ### VISUALIZATION 4 - MATRIX

    matrix_title = f'Matriz de etnia mata que etnia'

    victims_by_race = filtered_df.groupby('Race').size().reset_index(name='Executions')
    victims_by_race = victims_by_race[victims_by_race['Executions'] > 0]    # filter out races with 0 executions

    victims_columns = ['Number of White Victims', 'Number of Black Victims', 'Number of Latino Victims',
                       'Number of Asian Victims', 'Number of Native American Victims', 'Number of Other Race Victims']

    race_victims = ['White', 'Black', 'Latinx', 'Asian', 'Native American', 'Other Race']

    victims_data = filtered_df.groupby('Race')[victims_columns].sum().reset_index(drop=True)

    max_victims = victims_data.sum().max()

    fig4 = px.imshow(victims_data,
                     labels=dict(x="Victim's Race", y="Race of the Executed"),
                     x=race_victims,
                     y=victims_by_race['Race'],
                     color_continuous_scale='blues')

    #df_corr_etn = filtered_df['Race', 'Number of White Victims', 'Number of Black Victims', 'Number of Latino Victims', 'Number of Asian Victims', 'Number of Native American Victims', 'Number of Other Race Victims']
    #df_corr_etn.corrwith(df_corr_etn['Race'])
    #df_corr_etn.iplot(kind="heatmap",
     #                 colorscale="Blues",
     #                 title="Matriz de etnia mata que etnia",
     #                 dimensions=(500, 500))

    scatter_fig = px.scatter(filtered_df, x="Execution Date", y="Region", title="Execution Date vs Region")
    scatter_fig.update_layout(
        xaxis_title="Execution Date",
        yaxis_title="Region",
        hovermode="closest"
    )

    return map_title, fig1, pie_title, fig2, linechart_title, linechart, matrix_title, fig4, scatter_fig

################################### END OF THE APP ###################################

if __name__ == '__main__':
    app.run_server(debug=True)
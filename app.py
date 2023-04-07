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
colors = {
    'background': '#1E1E1E',
    'text': '#FFFFFF',
    'primary': '#FFA500',
    'secondary': '#00BFFF'
}
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
    multi = False,
    clearable = True,
    searchable= False,
    #style={'color': '#1E1E1E', 'background-color': '#1E1E1E'},
    placeholder="Select a sex"
)

# Dropdown for race
race_dropdown = dcc.Dropdown(
    id = 'race_dropdown',
    options = df['Race'].unique(),
    multi = False,
    clearable = True,
    searchable= False,
    placeholder= "Select a race",
    style={'color': '#1E1E1E', 'background-color': '#FFFFFF'}
)

# Checkbox item to select volunteers
volunteer_checkbox = dcc.Checklist(
    id = 'volunteer_checkbox',
    options = [{'label': ' Execution Volunteer', 'value': 'yes'}],
    value=[]
)

# Checkbox item to select foreign nationals
foreign_checkbox  = dcc.Checklist(
    id = 'foreign_checkbox',
    options = [{'label': ' Foreign National', 'value': 'Yes'}],
    value=[]
)

counts = df.groupby(['Execution Date', 'Race']).size().reset_index(name='Count')


################################### APP ###################################

app = dash.Dash(__name__ )

server = app.server

#################### APP LAYOUT ####################

app.layout = html.Div(style={'backgroundColor': colors['background']},
                      children=[
    html.Div([
            html.Img(
                src='/assets/logo.png',
                style={
                    'height': '70px',
                    'display': 'inline-block',
                    'margin-right': '15px',
                    'vertical-align': 'top'
                }
            ),
        html.H1(
                'Executions in USA',
                style={
                    'display': 'inline-block',
                    'vertical-align': 'top',
                    'margin-top': '20px',
                    'text-align': 'center',
                    'width': '100%'
                }
            )
        ],
        id='Title row',
        className='title_box',
        style={'display': 'flex'}),
    html.Br(),
    html.Div([
        html.H6('TEXTO INTRODUTORIO BLABLABLA INTRODUÇAO DO REPORT AHAHAHHAH')],
    style={'width': '100%', 'text-align': 'center'}),
    html.Br(),
    html.Div([
        html.Div([
            html.Div([
                sex_dropdown,
            ], style={'text-align': 'center','width': '200px','color': '#1E1E1E', 'background-color': '#1E1E1E'}),
            html.Div([
                volunteer_checkbox
            ], style={'margin-top': '30px','width': '200px' }),
            html.Div([
                foreign_checkbox
            ], style={'margin-top': '30px', 'width': '200px'}),
        ], style={'display': 'flex', 'align-items': 'center'}),
        html.Br(),
        html.Div([
            range_slider,
        ], style={'width': '1000px'}),
    ], style={'margin': 'auto', 'max-width': '1500px', 'display': 'flex', 'flex-direction': 'column',
              'align-items': 'center'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Label(id='map_title'),
        ], style={'text-align': 'center', 'padding-bottom': '10px', 'font-weight': 'bold', 'font-size': '20px', 'width': '350px', 'margin-left': '500px'}),
            html.Div([
                race_dropdown
            ], style={'text-align': 'center', 'width': '350px', 'margin-left': '500px', 'color': '#1E1E1E', 'background-color': '#1E1E1E'}),
        html.Div([
            dcc.Graph(id='usa_map'),
        ], style={'width': '100%'}),
    ], style={'display': 'inline-block', 'width': '100%', 'text-align': 'center'}),
    html.Div([
        html.Div([        html.H2('Between 1977 and 2023, 1561 prisioners were executed in the USA')    ], style={'width': '30%', 'text-align': 'center'}),
        html.Div([
            dcc.Graph(id='nested_pie_chart')    ], style={'width': '30%'}),
        html.Div([        html.H2('55.6% of the executed were white and 98.5% of them were male')    ], style={'width': '30%', 'text-align': 'center'}),
    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'width': '100%'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Graph(id='linechart')
        ], style={'display': 'inline-block', 'width': '48%'}),
        html.Div([
             dcc.Graph(id='scatter_fig')
         ], style={'display': 'inline-block', 'width': '48%'}),
    ], style={'display': 'inline-block', 'width': '100%', 'text-align': 'center'}),
html.Div([
        html.Div([
            dcc.Graph(id='matrix'),
        ], style={'display': 'inline-block', 'width': '48%', 'text-align': 'center'}),
        html.Div([
                dcc.Graph(id='figH')
        ], style={'display': 'inline-block', 'width': '48%', 'margin-top': '50px'}),
    ], style={'display': 'inline-block', 'width': '100%', 'text-align': 'center'}),
])

sex_dropdown.style = {'margin-top': '20px', 'margin-left': '-15px'}

################################### CALLBACKS ###################################

@app.callback(
    [
        Output('map_title', 'children'),
        Output('usa_map', 'figure'),
        Output('nested_pie_chart', 'figure'),
        Output('linechart', 'figure'),
        Output('matrix', 'figure'),
        Output('scatter_fig', 'figure'),
        Output('figH', 'figure')
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
        filtered_df_map = filtered_df[filtered_df['Race']==race_dropdown]
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
                        color_continuous_scale= px.colors.sequential.Pinkyl,
                        range_color=(0, executions_by_state['Executions'].max()),
                        labels={'Executions': 'Number of Executions'},
                        hover_data={'State':True, 'Executions':True}
                         )

    fig1.update_layout(
        coloraxis_colorbar=dict(
            title=dict(
                text='<b>Number of<br>Executions</b>',
                font=dict(color='white')
            ),
            tickfont=dict(color='white'),
        ),
        paper_bgcolor='rgb(30,30,30)',
        plot_bgcolor='rgb(30,30,30)',
        geo=dict(bgcolor='rgb(30,30,30)'),
        font=dict(color='black'),
        title=dict(font=dict(color='white'))
    )

    ### VISUALIZATION 2- NESTED PIE CHART

    filtered_df_grouped = filtered_df.groupby(['Sex', 'Race']).size().reset_index(name='Executions')

    fig2 = px.sunburst(data_frame=filtered_df_grouped,
                       path=['Sex', 'Race'],
                       values='Executions',
                       color='Race',
                       title='Number of executions by sex and race'
                       )
    fig2.update_layout(
        title=dict(text="<b>Number of executions by sex and race</b>", font=dict(color='white'), x=0.5, y=0.95),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    ### VISUALIZATION 3 - LINE CHART

    executions_by_race_by_year = filtered_df.groupby(['Race', 'Execution Year']).size().reset_index(name='Executions')

    linechart = px.line(executions_by_race_by_year, title="Executions per Race over time", x="Execution Year", y='Executions', color='Race', height=400)

    linechart.update_layout(
        title=dict(text="<b>Executions per Race over time</b>", font=dict(color='white'), x=0.5, y=0.95),
        xaxis=dict(title=dict(text='<b>Execution Year</b>', font=dict(color='white')),
                   tickfont=dict(color='white')),
        yaxis=dict(title=dict(text='<b>Executions</b>', font=dict(color='white')),
                   tickfont=dict(color='white')),
        legend=dict(title=dict(text='<b>Race</b>', font=dict(color='white')),
                    font=dict(color='white')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    ### VISUALIZATION 4 - MATRIX

    victims_by_race = filtered_df.groupby('Race').size().reset_index(name='Executions')
    victims_by_race = victims_by_race[victims_by_race['Executions'] > 0]    # filter out races with 0 executions

    victims_columns = ['Number of White Victims', 'Number of Black Victims', 'Number of Latino Victims',
                       'Number of Asian Victims', 'Number of Native American Victims', 'Number of Other Race Victims']

    race_victims = ['White', 'Black', 'Latinx', 'Asian', 'Native American', 'Other Race']

    victims_data = filtered_df.groupby('Race')[victims_columns].sum().reset_index(drop=True)

    fig4 = px.imshow(victims_data,
                     labels=dict(x="Victim's Race", y="Race of the Executed", title="Executioners' Race vs Victims' Race"),
                     x=race_victims,
                     y=victims_by_race['Race'],
                     color_continuous_scale='reds')

    fig4.update_layout(
        xaxis=dict(title=dict(text="<b>Victim's Race</b>", font=dict(color='white')),
                   tickfont=dict(color='white')),
        yaxis=dict(title=dict(text='<b>Race of the Executed</b>', font=dict(color='white')),
                   tickfont=dict(color='white')),
        coloraxis=dict(colorbar=dict(title=dict(text='<b>Number of Executions</b>', font=dict(color='white')),
                                     tickfont=dict(color='white'))),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=dict(text="<b>Executioners' Race vs Victims' Race</b>", font=dict(color='white'), x=0.5, y=0.95)
    )

    # Create a new column for the total number of victims per execution
    filtered_df['Total Victims'] = filtered_df['Number of White Victims'] + filtered_df['Number of Black Victims'] + filtered_df[
        'Number of Latino Victims'] + filtered_df['Number of Asian Victims'] + filtered_df['Number of Native American Victims'] + filtered_df[
                              'Number of Other Race Victims']

    # Create a scatter plot with the total number of victims determining the size of the scatter points
    scatter_fig = px.scatter(filtered_df, x="Execution Date", y="Region", size='Total Victims', title="Execution Date vs Region")

    # Set the axis and hover labels
    scatter_fig.update_layout(
        xaxis_title="Execution Date",
        yaxis_title="Region",
        hovermode="closest",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title=dict(text="<b>Execution Date</b>", font=dict(color='white')),
                   tickfont=dict(color='white')),
        yaxis=dict(title=dict(text="<b>Region</b>", font=dict(color='white')),
                   tickfont=dict(color='white')),
        title=dict(text="<b>Execution Date vs Region</b>", font=dict(color='white'),x=0.5, y=0.95)
    )

    filtered_df['ID'] = filtered_df.index
    pivot_df = pd.pivot_table(filtered_df, values='ID', index=['Race'], columns=['Region'], aggfunc='count').sort_values("South", ascending=False)
    figH = px.bar(pivot_df, x=pivot_df.index, y=["South", "West", "Midwest", "Northeast"], title='Number of Executed by Race and Region' )

    figH.update_layout(
        title=dict(text="<b>Number of Executed by Race and Region</b>", font=dict(color='white'), x=0.5, y=0.95),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title=dict(text="<b>Race</b>", font=dict(color='white')),
                   tickfont=dict(color='white')),
        yaxis=dict(title=dict(text="<b>Number of Executed</b>", font=dict(color='white')),
                   tickfont=dict(color='white')),
        legend=dict(
            title=dict(text="<b>Region</b>", font=dict(color='white')),
            font=dict(color='white')
        )
    )
    return map_title, fig1, fig2, linechart, fig4, scatter_fig, figH

################################### END OF THE APP ###################################

if __name__ == '__main__':
    app.run_server(debug=True)

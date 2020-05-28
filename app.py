import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Dataset Processing

path = 'https://raw.githubusercontent.com/IP2014336/DVCLASS/master/'
df = pd.read_csv(path + 'THERanking.csv', sep=';', engine='python')

country_options = [
    dict(label=country, value=country)
    for country in df['Country'].unique()]

University_options = [
    dict(label=University, value=University)
    for University in df['University'].unique()]

Year_options = [
    dict(label=Year, value=Year)
    for Year in df['Year'].unique()]

# Year	Rank	University	Country	National_Rank	Number_students	Numbstudentsper_Staff
# International_Students	Pct_Female	PCT_Male	ScoreResult	Teaching	Research	Citations
# Industry_Income	International_Outlook

# Building our Graphs
df_2020 = df.loc[df['Year'] == 2020][['Country', 'Rank', 'ScoreResult', 'National_Rank', 'University']]
df_2020_NR1 = df.loc[df['National_Rank'] == 1][['Country', 'Rank', 'ScoreResult', 'University']]
TopColl = df_2020.loc[df_2020['Rank'] == 1]
data_2020_choropleth = dict(type='choropleth',
                            locations=df_2020_NR1['Country'],
                            locationmode='country names',
                            z=df_2020_NR1['ScoreResult'],
                            text=df_2020_NR1['Country'] + '<br>' + df_2020_NR1['University'] + '<br>' +
                                 'World Rank: ' + df_2020_NR1['Rank'].apply(str),
                            colorscale='viridis',
                            reversescale=True
                            )

layout_2020_choropleth = dict(geo=dict(scope='world',  # default
                                       projection=dict(type='orthographic'
                                                       ),
                                       landcolor='black',
                                       lakecolor='white',
                                       showocean=True,  # default = False
                                       oceancolor='azure'
                                       ),
                              title=dict(text='University Rank 2020 (top scored in country)',
                                         x=.5  # Title relative position according to the xaxis, range (0,1)
                                         )
                              )

fig_2020_choropleth = go.Figure(data=data_2020_choropleth, layout=layout_2020_choropleth)
fig_2020_choropleth.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))

corr1 = px.scatter(df,
                   x=df['Number_students'],
                   y=df['ScoreResult'],
                   color=df['Year'],
                   hover_data=['University'],
                   title='Score vs Nr Students'
                   )
corr2 = px.scatter(df,
                   x=df['Pct_Female'],
                   y=df['ScoreResult'],
                   color=df['Year'],
                   hover_data=['University'],
                   title='Score vs Nr Students'
                   )
corr3 = px.scatter(df,
                   x=df['Numbstudentsper_Staff'],
                   y=df['ScoreResult'],
                   color=df['Year'],
                   hover_data=['University'],
                   title='Score vs Nr Students per staff'
                   )
corr4 = px.scatter(df,
                   x=df['International_Students'],
                   y=df['ScoreResult'],
                   color=df['Year'],
                   hover_data=['University'],
                   title='Score vs Nr Students International Students'
                   )
# menus
dropdown_country = dcc.Dropdown(
    id='country_drop',
    options=country_options,
    value='Portugal',
    multi=False
)
dropdown_univ = dcc.Dropdown(
    id='university_drop',
    options=University_options,
    value='NOVA University of Lisbon',
    multi=False
)
# RadioRank = dcc.RadioItems(
#        id='RankingType',
#        options=Ranking_options,
#        value='World University Ranking'
#    )
# RadioLeague = dcc.RadioItems(
#        id='league_drop',
#        options=League_options,
#        labelStyle={'display': 'block'}
#    )
SliderYear = dcc.RangeSlider(
    id='year_slider',
    min=2016,
    max=2020,
    value=[2016, 2020],
    marks={'2016': '2016',
           '2017': '2017',
           '2018': '2018',
           '2019': '2019',
           '2020': '2020'},
    step=1
)

# The app itself

app = dash.Dash(__name__)
server = app.server

colors = {
    'background': '#b6cfe0',
    'text': '#ffffff'
}
colorstit = {
    'background': '#b6cfe0',
    'text': '#808080'
}
app.layout = html.Div(style={'backgroundColor': colors['background'], }, children=[
    html.H2(
        children='University Rankings',
        style={
            'textAlign': 'center',
            'color': colorstit['text']
        }),
    html.Br(),
    html.Div([
        html.Div([
            dcc.Graph(
                id='clorop',
                figure=fig_2020_choropleth
            ),
            dcc.Textarea(
                id='card Top',
                value='\n\n\n\n\n\n\n\n\n\nTop University 2020\n\n\n\n California Institute of Technology\n United States ',
                style={'width': '50%', 'height': 400, 'textAlign': 'center'},
            )
        ], style={'display': 'flex'})
    ]),
    html.Div([
        html.Div([html.H3(children='Choose Country(s)',
                          style={'textAlign': 'center'}
                          ),
                  dropdown_country,
                  html.Button(id='clearButton', n_clicks=0, children='Clear Countries')]),
        html.Div([
            html.Div([
                html.H3(children='Choose time frame',
                        style={'textAlign': 'center'}
                        ),
                SliderYear,
            ], style={'width': '20%', 'borders': '1.5', 'margin': '10', 'color': colors['text']}),

            html.Div([
                html.Div([dcc.Graph(id='graph_example')])
            ], style={'width': '70%', 'textAlign': 'center'})
        ])
    ]),
    html.Div([
        html.H3(children='Choose a university',
                style={'textAlign': 'center'}
                ),
        html.Div([dropdown_univ]),
        html.Div([
            dcc.Graph(id='uni_evol')
        ])
    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id='c1',
                figure=corr1
            )]),
        html.Div([
            dcc.Graph(
                id='c2',
                figure=corr2
            )])
    ], style={'display': 'flex'}),
    html.Div([
        html.Div([
            dcc.Graph(
                id='c3',
                figure=corr3
            )]),
        html.Div([
            dcc.Graph(
                id='c4',
                figure=corr4
            )])
        ], style={'display': 'flex'})
])


@app.callback(
    [Output('graph_example', 'figure'),
     Output('uni_evol', 'figure')],
    [Input('country_drop', 'value'),
     Input('year_slider', 'value'),
     Input('university_drop', 'value')]
)
def update_graph(country, year, university):
    by_year_df = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]

    full_filtered_df = by_year_df.loc[by_year_df['Country'] == country]

    fig = px.scatter(full_filtered_df,
                     x=full_filtered_df['Year'],
                     y=full_filtered_df['Rank'],
                     color=full_filtered_df['University'],
                     symbol=full_filtered_df['Country'],
                     hover_data=['University'],
                     title='Ranks for Universities from ' + '<b>' + country + '</b><br>between ' +
                           '<b>' + str(year[0]) + '</b> and ' + '<b>' + str(year[1])
                     )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font': {
            'color': colors['text']
        }
    })
    fig.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    df_univ = df.loc[df['University'] == university]
    figun = px.scatter(df_univ,
                       x=df_univ['Year'],
                       y=df_univ['Rank'],
                       symbol=df_univ['Country'],
                       hover_data=['University'],
                       title=university + ' evolution 2016-2020'
                       )
    figun.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font': {
            'color': colors['text']
        }
    })
    figun.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig, figun


if __name__ == '__main__':
    app.run_server(debug=True)

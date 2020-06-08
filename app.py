import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO

response = requests.get('https://raw.githubusercontent.com/IP2014336/DVCLASS/master/still-life-851328_1920.jpg')
img = Image.open(BytesIO(response.content))

# Dataset Processing

path = 'https://raw.githubusercontent.com/IP2014336/DVCLASS/master/'
df = pd.read_csv(path + 'THERanking.csv', sep=',', engine='python')
# still-life-851328_1920.jpg

#img = Image.open(r"C:\Users\inesp\Downloads\still-life-851328_1920.jpg")

colors = {
    'background': '#d9d9d9',
    'text': '#ffffff'
}
colorstit = {
    'background': '#b6cfe0',
    'text': '#737373'
}
country_options = [
    dict(label=country, value=country)
    for country in df['Country'].unique()]

University_options = [
    dict(label=University, value=University)
    for University in df['University'].unique()]

Year_options = [
    dict(label=Year, value=Year)
    for Year in df['Year'].unique()]

Measures = ['Nº Students', '% International Students', 'Nº Students per Staff', '% females',
            'Teaching', 'Research', 'Citations', 'Industry Outlook', 'International Overlook']
Measures_options = [dict(label=measure, value=measure) for measure in Measures]

YesNo = ['Yes', 'No']
YesNo_options = [dict(label=simnao, value=simnao) for simnao in YesNo]

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
RadioYear = dcc.RadioItems(
    id='RadioYears',
    options=Year_options,
    value=2020
)
RadioYesNo = dcc.RadioItems(
    id='RadioYears',
    options=YesNo_options,
    value=2020
)

RadioMeasures = dcc.RadioItems(
    id='RadioMeasures',
    options=Measures_options,
    value='Research'
)
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

app = dash.Dash(__name__)
#server = app.server

app.layout = html.Div([
    # Overall Title
    html.H1(children='University Rankings', style={'textAlign': 'center', 'color': colorstit['text']}),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Introduction', value='tab-1'),
        dcc.Tab(label='Global', value='tab-2'),
        dcc.Tab(label='Countries', value='tab-3'),
        dcc.Tab(label='Universities', value='tab-4'),
        dcc.Tab(label='Indicators', value='tab-5'),
        dcc.Tab(label='Leave you feedback', value='tab-6')
    ]),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div([html.Img(src=img, width="850", height="600")]),
            html.Div([
                html.H1('"Learning never exhausts"', style={'textAlign': 'right'}),
                html.H1(' the mind"', style={'textAlign': 'right'}),
                html.H4('Leonardo da Vinci   ',
                        style={'font-weight': 'normal',
                               'font-size': '15px', 'font-style': 'italic',
                               'textAlign': 'right'}),
                html.Br(),
                html.H4(
                    children=" # Browse through the tabs to discover the top Universities in the word or in your country"),
                html.H4(children=" # Check the evolution of each University through the years"),
                html.H4(children=" # Understand the relationship between the ranking and other indicators")
            ])
        ], style={'display': 'flex'})
    elif tab == 'tab-2':  # GLOBAL
        return html.Div([
            html.Div([html.H3(children='Choose Year:',
                              style={'textAlign': 'center', 'padding': '0px', 'marginTop': 0}), RadioYear],
                     style={'display': 'flex', 'textAlign': 'center', 'padding': '5px', 'height': '20px',
                            'border': 'thin solid #888888', 'backgroundColor': '#e6e6e6'}),
            html.Div([
                html.Div([dcc.Graph(id='globe')],
                         style={'marginTop': 5, 'padding': '5px', 'backgroundColor': colors['background'],
                                'border': 'thin solid #888888', 'box-shadow': '2px 2px #888888', 'width': '38.5%',
                                'height': '380px'}),
                html.Div(html.Br(), style={'width': '1%', 'opacity': '0%', 'height': '390px'}),
                html.Div([dcc.Graph(id='top10country')],
                         style={'marginTop': 5, 'box-shadow': '2px 2px #888888', 'width': '60%',
                                'border': 'thin solid #888888', 'height': '390px'})
            ], style={'display': 'flex', 'textAlign': 'center', 'height': '390px'}),
            html.Div(html.Br(), style={'opacity': '0%', 'height': '10px'}),
            html.Div([
                html.Div([
                    html.Div(html.Br(), style={'width': '5%'}),
                    html.Div([dcc.Graph(id='top10uni')], style={'width': '90%', 'textAlign': 'center'})
                ], style={'display': 'flex', 'textAlign': 'center'})
            ], style={'backgroundColor': colors['background'], 'padding': '5px', 'border': 'thin solid #888888',
                      'box-shadow': '5px 5px #888888'}),
        ]),
    elif tab == 'tab-3':  # COUNTRIES
        return html.Div([
            html.Div([html.H3(children='Choose Country:', style={'marginTop': '1px', 'marginBottom': '1px'}),
                      dropdown_country],
                     style={'backgroundColor': colors['background'], 'padding': '1px'}),
            html.H3(children='TOP 3 National Universities in 2020',
                    style={'textAlign': 'center', 'font-size': '18px', 'padding': '4px',
                           'marginTop': '6px', 'marginBottom': '2px'}),
            html.Div([
                html.Div([dbc.Card(id='first_card', outline=True)]),
                html.Div([dbc.Card(id='second_card', outline=True)]),
                html.Div([dbc.Card(id='third_card', outline=True)])
            ], style={'display': 'flex', 'padding': '5px', 'border': 'thin solid #888888',
                      'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']}),
            html.Div([html.H3(children='Choose time frame:'),
                      html.Div([SliderYear], style={'padding-left': '30%', 'padding-right': '30%'})],
                     style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                            'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']}),
            html.Div([html.Div([dcc.Graph(id='country')])],
                     style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                            'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']})
        ])
    elif tab == 'tab-4':  # Universities
        return html.Div([
            html.Div([html.H3(children='Choose a university:'), dropdown_univ],
                     style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                            'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']}),
            html.Div([
                html.Div([dcc.Graph(id='uni_evol')], style={'width': '32%', 'margin': '0'}),
                html.Div([
                    html.Div([
                        html.Div([dcc.Graph(id='measure1')]),
                        html.Div([dcc.Graph(id='measure2')]),
                        html.Div([dcc.Graph(id='measure3')]),
                        html.Div([dcc.Graph(id='measure4')])
                    ], style={'display': 'flex'}),
                    html.Div([
                        html.Div([dcc.Graph(id='measure5')]),
                        html.Div([dcc.Graph(id='measure6')]),
                        html.Div([dcc.Graph(id='measure7')]),
                        html.Div([dcc.Graph(id='measure8')])
                    ], style={'display': 'flex'})
                ], style={'width': '68%'})
            ], style={'display': 'flex', 'padding': '5px', 'border': 'thin solid #888888',
                      'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']})
        ])
    elif tab == 'tab-5':  # Indicators
        return html.Div([
            html.Div([
                html.Div([dcc.Graph(id='c1', figure=corr1)],
                         style={'width': '50%', 'padding': '5px',
                                'border': 'thin solid #888888', 'box-shadow': '5px 5px #888888'}),
                html.Div([dcc.Graph(id='c2', figure=corr2)],
                         style={'width': '50%', 'padding': '5px',
                                'border': 'thin solid #888888', 'box-shadow': '5px 5px #888888'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([dcc.Graph(id='c3', figure=corr3)],
                         style={'width': '50%', 'padding': '5px',
                                'border': 'thin solid #888888', 'box-shadow': '5px 5px #888888'}),
                html.Div([dcc.Graph(id='c4', figure=corr4)],
                         style={'width': '50%', 'padding': '5px',
                                'border': 'thin solid #888888', 'box-shadow': '5px 5px #888888'})
            ], style={'display': 'flex'})
        ])
    elif tab == 'tab-6':
        return html.Div([
            html.H3('Tab content 6')
        ])


# Graficos para GLOBAL START
@app.callback(
    [Output('top10uni', 'figure'),
     Output('top10country', 'figure'),
     Output('globe', 'figure')],
    [Input('RadioYears', 'value')]
)
def update_graph(year2):
    # Top Universidades
    df_year2 = df.loc[df['Year'] == year2]
    df_topu = df_year2.loc[df_year2['Rank'] <= 10].sort_values(by='ScoreResult', ascending=False)
    figtopu = px.bar(data_frame=df_topu,
                     x=df_topu['ScoreResult'],
                     y=df_topu['University'],
                     color=df_topu['Country'],
                     text=df_topu['Rank'],
                     color_discrete_sequence=px.colors.sequential.Viridis_r,
                     orientation='h',
                     opacity=0.8,
                     barmode='relative',
                     height=390,
                     title='<b>TOP 10 Universities world wide in ' + str(year2))
    figtopu.update_layout(margin=dict(l=20, r=20, t=40, b=20), titlefont=dict(size=15),
                          title={'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    figtopu.update_layout({'paper_bgcolor': 'rgba(255, 255, 255, 0)'})

    # Paises com mais univ no top 200
    df_topc = df_year2.loc[df_year2['Rank'] <= 200][['Country', 'Rank', 'University']]
    countrylist = df_topc['Country'].value_counts()[:10].sort_values(ascending=False).index
    df_topc3 = df_topc[df_topc['Country'].isin(countrylist)]
    figtopc = px.bar(data_frame=df_topc3,
                     x=df_topc3['Rank'],
                     y=df_topc3['Country'],
                     color=df_topc3['Country'],
                     hover_name=df_topc3['University'],
                     color_discrete_sequence=px.colors.sequential.Viridis_r,
                     orientation='h',
                     opacity=0.9,
                     barmode='relative',
                     height=390,
                     title='<b>TOP 10 Countries with most universities on TOP 200 in ' + str(year2))
    figtopc.update_layout(margin=dict(l=20, r=20, t=40, b=20), titlefont=dict(size=15),
                          title={'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    # Globo
    df_NR1 = df_year2.loc[df_year2['National_Rank'] == 1][['Country', 'Rank', 'ScoreResult', 'University']]

    data_choropleth = dict(type='choropleth',
                           locations=df_NR1['Country'],
                           locationmode='country names',
                           z=df_NR1['ScoreResult'],
                           text=df_NR1['Country'] + '<br>' + df_NR1['University'] + '<br>' +
                                'World Rank: ' + df_NR1['Rank'].apply(str),
                           colorscale='viridis',
                           reversescale=True
                           )

    layout_choropleth = dict(geo=dict(scope='world',  # default
                                      projection=dict(type='orthographic'),
                                      landcolor='black',
                                      lakecolor='white',
                                      showocean=True,  # default = False
                                      oceancolor='azure'
                                      ),
                             title=dict(text='<b>University Rank ' + str(year2) + '</b><br>'
                                             + '<i>top scored in country',
                                        x=.47  # Title relative position according to the xaxis, range (0,1)
                                        ),
                             height=350
                             )

    fig_choropleth = go.Figure(data=data_choropleth, layout=layout_choropleth)
    fig_choropleth.update_layout(margin=dict(l=5, r=5, t=50, b=10), titlefont=dict(size=15))
    fig_choropleth.update_layout({
        'plot_bgcolor': 'rgba(95, 158, 160, 0)',
        'paper_bgcolor': 'rgba(95, 158, 160, 0)'
    })
    # World Graph END
    # Graficos para GLOBAL END
    return figtopu, figtopc, fig_choropleth


# Graficos para COUNTRIES START
@app.callback(
    [Output('first_card', 'children'),
     Output('second_card', 'children'),
     Output('third_card', 'children'),
     Output('country', 'figure')],
    [Input('country_drop', 'value'),
     Input('year_slider', 'value')]  # V2
)
def update_graph(country, year):  # V2
    df_cards = df.loc[(df['Year'] == 2020) & (df['Country'] == country) & (df['National_Rank'] <= 3)]
    df_1cards = df_cards.loc[(df_cards['National_Rank'] == 1)]
    first_card = dbc.Card([
        html.Br(), html.Br(), html.Br(), html.Br(),
        dbc.CardHeader("Nº 1 National Rank", style={'color': colors['text']}),
        dbc.CardBody(
            [
                html.H3(df_1cards['University'], className="card-title", style={'color': 'rgb(133, 224, 133)'}),
                html.H5("World Rank: " + df_1cards['Rank'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Nº of Students: " + df_1cards['Number_students'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Nº of Students per staff: " + df_1cards['Numbstudentsper_Staff'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("% International Students: " + df_1cards['International_Students'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("% Females : " + df_1cards['Pct_Female'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Teaching: " + df_1cards['Teaching'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Research: " + df_1cards['Research'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Citations: " + df_1cards['Citations'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Industry Income: " + df_1cards['Industry_Income'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("International Outlook: " + df_1cards['International_Outlook'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']})
            ]),
    ], style={"width": "25rem", 'line-height': '2px', 'textAlign': 'center', "border": "2px black solid",
              'backgroundColor': 'rgba(0, 0, 0, 1)'})
    df_2cards = df_cards.loc[df['National_Rank'] == 2]
    second_card = dbc.Card([
        html.Br(), html.Br(), html.Br(), html.Br(),
        dbc.CardHeader("Nº 2 National Rank", style={'color': colors['text']}),
        dbc.CardBody(
            [
                html.H3(df_2cards['University'], className="card-title", style={'color': 'rgb(133, 224, 133)'}),
                html.H5("World Rank: " + df_2cards['Rank'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Nº of Students: " + df_2cards['Number_students'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Nº of Students per staff: " + df_2cards['Numbstudentsper_Staff'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("% International Students: " + df_2cards['International_Students'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("% Females : " + df_2cards['Pct_Female'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Teaching: " + df_2cards['Teaching'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Research: " + df_2cards['Research'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Citations: " + df_2cards['Citations'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Industry Income: " + df_2cards['Industry_Income'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("International Outlook: " + df_2cards['International_Outlook'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']})
            ]),
    ], style={"width": "25rem", 'line-height': '2px', 'textAlign': 'center', "border": "2px black solid",
              'backgroundColor': 'rgba(0, 0, 0, 0.6)'})

    df_3cards = df_cards.loc[df['National_Rank'] == 3]
    third_card = dbc.Card([
        html.Br(), html.Br(), html.Br(), html.Br(),
        dbc.CardHeader("Nº 3 National Rank", style={'opacity': '100%', 'color': colors['text']}),
        dbc.CardBody(
            [
                html.H3(df_3cards['University'], className="card-title", style={'color': 'rgb(133, 224, 133)'}),
                html.H5("World Rank: " + df_3cards['Rank'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Nº of Students: " + df_3cards['Number_students'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Nº of Students per staff: " + df_3cards['Numbstudentsper_Staff'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("% International Students: " + df_3cards['International_Students'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("% Females : " + df_3cards['Pct_Female'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Teaching: " + df_3cards['Teaching'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Research: " + df_3cards['Research'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Citations: " + df_3cards['Citations'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("Industry Income: " + df_3cards['Industry_Income'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                html.H5("International Outlook: " + df_3cards['International_Outlook'].apply(str),
                        style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']})
            ]),
    ], style={"width": "25rem", 'line-height': '2px', 'textAlign': 'center', "border": "2px black solid",
              'backgroundColor': 'rgba(0, 0, 0, 0.4)'})

    by_year_df = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]
    full_filtered_df = by_year_df.loc[by_year_df['Country'] == country]
    fig = px.scatter(full_filtered_df,
                     x=full_filtered_df['Year'],
                     y=full_filtered_df['Rank'],
                     color=full_filtered_df['University'],
                     symbol=full_filtered_df['Country'],
                     hover_data=['University', 'National_Rank'],
                     title='Ranks for Universities from ' + '<b>' + country + '</b> between ' +
                           '<b>' + str(year[0]) + '</b> and ' + '<b>' + str(year[1])
                     )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0.2)',
        'paper_bgcolor': 'rgba(95, 158, 160, 0.5)'
    })
    fig.update_layout(xaxis_type='category')
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.update_layout(legend=dict(x=1, y=1))

    return first_card, second_card, third_card, fig


# Gráficos para Countries END

# Gráficos para Universities START
@app.callback(
    [Output('uni_evol', 'figure'),
     Output('measure1', 'figure'),
     Output('measure2', 'figure'),
     Output('measure3', 'figure'),
     Output('measure4', 'figure'),
     Output('measure5', 'figure'),
     Output('measure6', 'figure'),
     Output('measure7', 'figure'),
     Output('measure8', 'figure')],
    [Input('university_drop', 'value')]
)
def update_graph(university):
    df_univ = df.loc[df['University'] == university]
    figun = px.scatter(df_univ,
                       x=df_univ['Year'],
                       y=df_univ['Rank'],
                       title='World Rank evolution 2016-2020'
                       )
    figun.update_layout({
        'plot_bgcolor': 'rgba(255, 255, 255, 0.1)',
        'paper_bgcolor': 'rgba(95, 158, 160, 0)',
        #   'font': {
        #       'color': colors['text']
        #   }
    })
    figun.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        margin=dict(l=5, r=5, t=60, b=20)
    )
    figun.update_traces(marker=dict(size=20,
                                    line=dict(width=1,
                                              color='DarkSlateGrey')),
                        selector=dict(mode='markers'))
    dfm1 = df_univ[['Year', 'Number_students']]
    measure1 = px.bar(data_frame=dfm1, x=dfm1['Year'], y=dfm1['Number_students'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=210, color_discrete_sequence=["DarkCyan"],
                      title={'text': 'Nº of Students', 'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'})
    measure1.update_layout(margin=dict(l=10, r=10, t=30, b=5), paper_bgcolor="rgba(95, 158, 160, 0)",
                           font=dict(size=10))
    measure1['layout']['yaxis']['title']['text'] = ''
    measure1['layout']['xaxis']['title']['text'] = ''
    measure1.update_xaxes(showgrid=False, zeroline=False)
    measure1.update_yaxes(showgrid=False, zeroline=False)

    dfm2 = df_univ[['Year', 'Numbstudentsper_Staff']]
    measure2 = px.bar(data_frame=dfm2, x=dfm2['Year'], y=dfm2['Numbstudentsper_Staff'], orientation='v',
                      opacity=0.9, barmode='relative', height=218, width=210, color_discrete_sequence=["CadetBlue"],
                      title={'text': 'Nº of Students per staff', 'y': 0.95, 'x': 0.6, 'xanchor': 'center',
                             'yanchor': 'top'})
    measure2.update_layout(margin=dict(l=10, r=10, t=30, b=5), paper_bgcolor="rgba(95, 158, 160, 0)",
                           font=dict(size=10))
    measure2['layout']['yaxis']['title']['text'] = ''
    measure2['layout']['xaxis']['title']['text'] = ''
    measure2.update_xaxes(showgrid=False, zeroline=False)
    measure2.update_yaxes(showgrid=False, zeroline=False)

    dfm3 = df_univ[['Year', 'Teaching']]
    measure3 = px.bar(data_frame=dfm3, x=dfm3['Year'], y=dfm3['Teaching'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=210, color_discrete_sequence=["DarkSeaGreen"],
                      title={'text': 'Teaching', 'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'})
    measure3.update_layout(margin=dict(l=10, r=10, t=30, b=5), paper_bgcolor="rgba(95, 158, 160, 0)",
                           font=dict(size=10))
    measure3['layout']['yaxis']['title']['text'] = ''
    measure3['layout']['xaxis']['title']['text'] = ''
    measure3.update_xaxes(showgrid=False, zeroline=False)
    measure3.update_yaxes(showgrid=False, zeroline=False)

    dfm4 = df_univ[['Year', 'Research']]
    measure4 = px.bar(data_frame=dfm4, x=dfm4['Year'], y=dfm4['Research'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=210, color_discrete_sequence=["ForestGreen"],
                      title={'text': 'Research', 'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'})
    measure4.update_layout(margin=dict(l=10, r=10, t=30, b=5), paper_bgcolor="rgba(95, 158, 160, 0)",
                           font=dict(size=10))
    measure4['layout']['yaxis']['title']['text'] = ''
    measure4['layout']['xaxis']['title']['text'] = ''
    measure4.update_xaxes(showgrid=False, zeroline=False)
    measure4.update_yaxes(showgrid=False, zeroline=False)

    dfm5 = df_univ[['Year', 'Citations']]
    measure5 = px.bar(data_frame=dfm5, x=dfm5['Year'], y=dfm5['Citations'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=210, color_discrete_sequence=["DarkOliveGreen"],
                      title={'text': 'Citations', 'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'})
    measure5.update_layout(margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(95, 158, 160, 0)",
                           font=dict(size=10))
    measure5['layout']['yaxis']['title']['text'] = ''
    measure5.update_xaxes(showgrid=False, zeroline=False)
    measure5.update_yaxes(showgrid=False, zeroline=False)

    dfm6 = df_univ[['Year', 'Industry_Income']]
    measure6 = px.bar(data_frame=dfm6, x=dfm6['Year'], y=dfm6['Industry_Income'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=210, color_discrete_sequence=["DarkSlateGrey"],
                      title={'text': 'Industry Outcome', 'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'})
    measure6.update_layout(margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(95, 158, 160, 0)",
                           font=dict(size=10))
    measure6['layout']['yaxis']['title']['text'] = ''
    measure6.update_xaxes(showgrid=False, zeroline=False)
    measure6.update_yaxes(showgrid=False, zeroline=False)

    dfm7 = df_univ[['Year', 'International_Outlook']]
    measure7 = px.bar(data_frame=dfm7, x=dfm7['Year'], y=dfm7['International_Outlook'], orientation='v',
                      opacity=0.9,
                      barmode='relative', height=218, width=210, color_discrete_sequence=["Gray"],
                      title={'text': 'International Outlook', 'y': 0.95, 'x': 0.6, 'xanchor': 'center',
                             'yanchor': 'top'})
    measure7.update_layout(margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(95, 158, 160, 0)",
                           font=dict(size=10))
    measure7['layout']['yaxis']['title']['text'] = ''
    measure7.update_xaxes(showgrid=False, zeroline=False)
    measure7.update_yaxes(showgrid=False, zeroline=False)

    dfm8 = df_univ[['Year', 'Pct_Female']]
    measure8 = px.bar(data_frame=dfm8, x=dfm8['Year'], y=dfm8['Pct_Female'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=210, color_discrete_sequence=["DarkKhaki"],
                      title={'text': '% Females & Males', 'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'})
    measure8.update_layout(margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(95, 158, 160, 0)",
                           font=dict(size=10))
    measure8['layout']['yaxis']['title']['text'] = ''
    measure8.update_xaxes(showgrid=False, zeroline=False)
    measure8.update_yaxes(showgrid=False, zeroline=False)
    return figun, measure1, measure2, measure3, measure4, measure5, measure6, measure7, measure8


# Gráficos para Universities END

# Gráficos para Indicators START

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
                   title='Score vs %Females'
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

if __name__ == '__main__':
    app.run_server(debug=True)

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

#######################################
# Inicio do Indice
# 1 > Recupera Imagem homepage
# 2 > Recupera dados
# 3 > Define cores genéricas
# 4 > Definição das opções para os menus interativos
# 5 > Definição dos menus interativos
# 6 > Inicio do layout da app
#   6.1 > Título geral da página, por cima das Tabs
#   6.2 > Tabs do menu
# 7 > Callback das tabs
#   7.1 > Tab Inicial
#     7.1.1 > Call Imagem
#     7.1.2 > Quote
#     7.1.3 > Objetivos da app
#   7.2 > Tab Global
#     7.2.1 > Menu de anos
#     7.2.2 > Call Gráfico Globo
#     7.2.3 > Call Gráfico Paises com mais universidades no top200
#     7.2.4 > Call Gráfico Top 10 universidades
#   7.3 > Tab de Países
#     7.3.1 > Menu de país
#     7.3.2 > Call Cards do top 3 nacional
#     7.3.3 > Call de gráfico das universidades do país
#     7.3.4 > Menu de intervalo de datas
#   7.4 > Tab de Universidades
#     7.4.1 > Menu de universidade
#     7.4.2 > Call de scatter plot de evolução do score da universidade
#     7.4.3 > Call de 11 gráficos de barras de indicadores da universidade
#   7.5 > Tab de Indicadores (estática)
#     7.5.1 > Call de 4 scatter plots de indicadores vs score
#   7.6 > Tab de feedback (exemplificativo, não recolhe efetivamente o feedback...)
#     7.6.1 > Título
#     7.6.2 > Perguntas
#     7.6.3 > Caixa de comentario
#     7.6.4 > Call Botão de submissao
# 8 > app.callback para Tab Global
#   8.1 > Define gráfico das 10 melhores Universidades
#   8.2 > Define gráfico dos Paises com mais univ no top 200
#   8.3 > Define gráfico de Globo
# 9 > app.callback para Tab Paises
#   9.1 > Define Card 1
#   9.2 > Define Card 2
#   9.3 > Define Card 3
#   9.4 > Define Gráfico das Universidades do País
# 10 > app.callback para Tab Universidade
#   10.1 > Define gráfico da evolução do rank da universidade
#   10.2 > Define gráfico da evolução do nº de estudandes
#   10.3 > Define gráfico da evolução do nº de estudandes por funcionario
#   10.4 > Define gráfico da evolução do Teaching
#   10.5 > Define gráfico da evolução do Research
#   10.6 > Define gráfico da evolução do Citations
#   10.7 > Define gráfico da evolução do Industry_Income
#   10.8 > Define gráfico da evolução do International_Outlook
#   10.9 > Define gráfico da evolução do Pct_Female
#   10.10 > Define gráfico da % estudantes internacionais
# 11 > Define 4 scatter plots de indicadores vs score
#   11.1 > Constroi 1º gráfico
#   11.2 > Anotaçoes ao 1º gráfico
# 12 > Define botão de submissão
# Fim do Indice
#######################################

# 1 > Recupera Imagem homepage
response = requests.get('https://raw.githubusercontent.com/IP2014336/DVCLASS/master/still-life-851328_1920.jpg')
img = Image.open(BytesIO(response.content))

# 2 > Recupera dados
path = 'https://raw.githubusercontent.com/IP2014336/DVCLASS/master/'
df = pd.read_csv(path + 'THERanking.csv', sep=';', engine='python')

# 3 > Define cores genéricas
colors = {
    'background': '#d9d9d9',
    'text': '#ffffff'
}
colorstit = {
    'background': '#b6cfe0',
    'text': '#737373'
}

# 4 > Definição das opções para os menus interativos
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
grades = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
grades_options = [dict(label=grade, value=grade) for grade in grades]
uniquests = ['Oxford', 'Harvard ', 'Yale', 'Nova University of Lisbon', 'Dont know']
quest_options = [dict(label=uniquest, value=uniquest) for uniquest in uniquests]

# 5 > Definição dos menus interativos
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
    id='RadioYesNo',
    options=YesNo_options
)
RadioGrade = dcc.RadioItems(
    id='RadioGrade',
    options=grades_options
)
RadioQuest = dcc.RadioItems(
    id='RadioGrade',
    options=quest_options
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

# suppress_callback_exceptions=True para não dar erros com os callbacks das distintas tabs
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server #Descomentar no github

# 6 > Inicio do layout da app
app.layout = html.Div([
    # 6.1 > Título geral da página, por cima das Tabs
    html.H1(children='University Rankings',
            style={'textAlign': 'center', 'color': colorstit['text'], 'marginTop': '20px', 'marginBottom': '10px'}),
    # 6.2 > Tabs do menu
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Introduction', value='tab-1'),
        dcc.Tab(label='Global', value='tab-2'),
        dcc.Tab(label='Countries', value='tab-3'),
        dcc.Tab(label='Universities', value='tab-4'),
        dcc.Tab(label='Indicators', value='tab-5'),
        dcc.Tab(label='Leave your feedback', value='tab-6')
    ]),
    html.Div(id='tabs-content')
])


# 7 > Callback das tabs
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':  # 7.1 > Tab Inicial
        return html.Div([
            # 7.1.1 > Call Imagem
            html.Div([html.Img(src=img, width="832", height="600")]),
            html.Div([
                # 7.1.2 > Quote
                html.H1('"Learning never exhausts', style={'textAlign': 'right'}),
                html.H1(' the mind"', style={'textAlign': 'right'}),
                html.H4('Leonardo da Vinci   ',
                        style={'font-weight': 'normal',
                               'font-size': '15px', 'font-style': 'italic',
                               'textAlign': 'right'}),
                html.Br(),
                # 7.1.3 > Objetivos da app
                html.H4(children=" # Browse through the tabs to discover the top "
                                 "Universities in the word or in your country"),
                html.H4(children=" # Check the evolution of each University through the years"),
                html.H4(children=" # Understand the relationship between the ranking and other indicators")
            ])
        ], style={'display': 'flex'})
    elif tab == 'tab-2':
        # 7.2 > Tab Global
        return html.Div([
            # 7.2.1 > Menu de anos
            html.Div([html.H3(children='Choose a Year:', style={'marginTop': '0', 'marginBottom': '0'}),
                      RadioYear], style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                                             'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']}),
            html.Div([html.Br()], style={'height': '5px'}),
            html.Div([
                # 7.2.2 > Call Gráfico Globo
                html.Div([dcc.Graph(id='globe')],
                         style={'marginTop': 5, 'padding': '5px', 'backgroundColor': colors['background'],
                                'border': 'thin solid #888888', 'box-shadow': '2px 2px #888888', 'width': '44%',
                                'height': '380px'}),
                html.Div(html.Br(), style={'width': '1%', 'opacity': '0%', 'height': '390px'}),
                # 7.2.3 > Call Gráfico Paises com mais universidades no top200
                html.Div([dcc.Graph(id='top10country')],
                         style={'marginTop': 5, 'box-shadow': '2px 2px #888888', 'width': '55%',
                                'border': 'thin solid #888888', 'height': '390px'})
            ], style={'display': 'flex', 'textAlign': 'center', 'height': '390px'}),
            html.Div(html.Br(), style={'opacity': '0%', 'height': '10px'}),
            html.Div([
                html.Div([
                    html.Div(html.Br(), style={'width': '5%'}),
                    # 7.2.4 > Call Gráfico Top 10 universidades
                    html.Div([dcc.Graph(id='top10uni')], style={'width': '90%', 'textAlign': 'center'})
                ], style={'display': 'flex', 'textAlign': 'center'})
            ], style={'backgroundColor': colors['background'], 'padding': '5px', 'border': 'thin solid #888888',
                      'box-shadow': '5px 5px #888888'}),
        ]),
    elif tab == 'tab-3':  # 7.3 > Tab de Países
        return html.Div([
            # 7.3.1 > Menu de país
            html.Div([html.H3(children='Choose a Country:', style={'marginTop': '0', 'marginBottom': '0'}),
                      dropdown_country], style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                                             'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']}),
            html.Div([html.Br()], style={'height': '5px'}),
            html.Div([
                # 7.3.2 > Call Cards do top 3 nacional
                html.H3(children='TOP 3 National Universities in 2020',
                        style={'textAlign': 'center', 'font-size': '18px', 'padding': '4px',
                               'marginTop': '6px', 'marginBottom': '2px'}),
                html.Div([
                    html.Div([dbc.Card(id='first_card', outline=True)]),
                    html.Div([dbc.Card(id='second_card', outline=True)]),
                    html.Div([dbc.Card(id='third_card', outline=True)])
                ], style={'display': 'flex'})
            ], style={'padding': '5px', 'border': 'thin solid #888888',
                      'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']}),
            html.Div([html.Br()], style={'height': '7px'}),
            # 7.3.3 > Call de gráfico das universidades do país
            html.Div([html.Div([dcc.Graph(id='country')])],
                     style={'textAlign': 'center', 'padding': '2px', 'border': 'thin solid #888888', 'marginTop': '0px',
                            'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']}),
            # 7.3.4 > Menu de intervalo de datas
            html.Div([html.H3(children='Update time frame:', style={'marginTop': '0px', 'marginBottom': '0px'}),
                      html.Div([SliderYear], style={'padding-left': '30%', 'padding-right': '30%'})],
                     style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                            'box-shadow': '5px 5px #888888', 'backgroundColor': 'white'}),
        ])
    elif tab == 'tab-4':  # 7.4 > Tab de Universidades
        return html.Div([
            # 7.4.1 > Menu de universidade
            html.Div([html.H3(children='Choose a university:', style={'marginTop': '0', 'marginBottom': '0'}),
                      dropdown_univ], style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                                             'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']}),
            html.Div([html.Br()], style={'height': '5px'}),
            html.Div([
                html.Div([
                    # 7.4.2 > Call de scatter plot de evolução do score da universidade
                    html.Div([dcc.Graph(id='uni_evol')])
                ], style={'width': '40%', 'marginTop': '0', 'marginBottom': '20'}),
                html.Div([
                    html.Div([
                        # 7.4.3 > Call de 11 gráficos de barras de indicadores da universidade
                        html.Div([dcc.Graph(id='measure1')], style={'width': '35%', 'height': '190px'}),
                        html.Div([dcc.Graph(id='measure2')], style={'width': '35%', 'height': '190px'}),
                        html.Div([dcc.Graph(id='measure3')], style={'width': '35%', 'height': '190px'}),
                    ], style={'display': 'flex'}),
                    html.Div([
                        html.Div([dcc.Graph(id='measure4')], style={'width': '35%', 'height': '190px'}),
                        html.Div([dcc.Graph(id='measure5')], style={'width': '35%', 'height': '150px'}),
                        html.Div([dcc.Graph(id='measure6')], style={'width': '35%', 'height': '150px'}),
                    ], style={'display': 'flex'}),
                    html.Div([
                        html.Div([dcc.Graph(id='measure7')], style={'width': '35%', 'height': '150px'}),
                        html.Div([dcc.Graph(id='measure8')], style={'width': '35%', 'height': '150px'}),
                        html.Div([dcc.Graph(id='measure9')], style={'width': '35%', 'height': '150px'})
                    ], style={'display': 'flex'})
                ], style={'width': '60%'})
            ], style={'display': 'flex', 'padding': '5px', 'border': 'thin solid #888888', 'height': '600px',
                      'box-shadow': '5px 5px #888888', 'backgroundColor': colors['background']})
        ])
    elif tab == 'tab-5':  # 7.5 > Tab de Indicadores (estática)
        return html.Div([
            html.Div([html.Br()], style={'height': '7px'}),
            html.Div([
                # 7.5.1 > Call de 4 scatter plots de indicadores vs score
                html.Div([dcc.Graph(id='c1', figure=corr1)],
                         style={'width': '24.5%', 'padding': '0px', 'height': '460px',
                                'border': 'thin solid #888888', 'box-shadow': '5px 5px #888888'}),
                html.Div([html.Br()], style={'width': '0.5%'}),
                html.Div([dcc.Graph(id='c2', figure=corr2)],
                         style={'width': '24.5%', 'padding': '0px', 'height': '460px',
                                'border': 'thin solid #888888', 'box-shadow': '5px 5px #888888'}),
                html.Div([html.Br()], style={'width': '0.5%'}),
                html.Div([dcc.Graph(id='c3', figure=corr3)],
                         style={'width': '24.5%', 'padding': '0px', 'height': '460px',
                                'border': 'thin solid #888888', 'box-shadow': '5px 5px #888888'}),
                html.Div([html.Br()], style={'width': '0.5%'}),
                html.Div([dcc.Graph(id='c4', figure=corr4)],
                         style={'width': '24.5%', 'padding': '0px', 'height': '460px',
                                'border': 'thin solid #888888', 'box-shadow': '5px 5px #888888'})
             ], style={'display': 'flex'})
        ])
    elif tab == 'tab-6':  # 7.6 > Tab de feedback (exemplificativo, não recolhe efetivamente o feedback...)
        return html.Div([
            # 7.6.1 > Título
            html.H1('Help us improve!', style={'color': '#669999', 'text-shadow': '2px 0px black'}),
            # 7.6.2 > Perguntas
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("The visualizations are intuitive and easy to use")], style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
                html.Div([RadioGrade], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("The visualizations loaded quickly")], style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
                html.Div([RadioGrade], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("This is an important subject to me")], style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
                html.Div([RadioGrade], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("I was able to gather relevant information")],
                         style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
                html.Div([RadioGrade], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("The application has all the options I expected")],
                         style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
                html.Div([RadioGrade], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("I am satisfied with the overall application")],
                         style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
                html.Div([RadioGrade], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%'}),
                html.Div([html.P("Do you now know which is the world best University in 2020?")],
                         style={'width': '35%'}),
                html.Div([html.Br()], style={'width': '3%'}),
                html.Div([RadioQuest], style={'marginBottom': '0px', 'marginTop': '15px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%'}),
                html.Div([html.P("Feel free to leave any comment")], style={'width': '35%'}),
                html.Div([html.Br()], style={'width': '3%'}),
                # 7.6.3 > Caixa de comentario
                html.Div([
                    dcc.Textarea(
                        value='write here',
                        style={'width': 550, 'height': 50, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                    )])
            ], style={'display': 'flex'}),
            html.Div([html.Br()], style={'height': '15px'}),
            html.Div([
                # 7.6.4 > Botão de submissao
                html.Div([html.Br()], style={'width': '36%'}),
                html.Div([html.Button(' Submit ', id='submitbutton', n_clicks=0, style={})]),
                html.Div([html.Br()], style={'width': '1%'}),
                html.Div(id='container-button-basic',
                         style={'font-style': 'italic', 'font-size': '12px', 'marginTop': '5px'})
            ], style={'display': 'flex'})
        ])


# 8 > app.callback para GLOBAL
@app.callback(
    [Output('top10uni', 'figure'),
     Output('top10country', 'figure'),
     Output('globe', 'figure')],
    [Input('RadioYears', 'value')]
)
def update_graph(year2):
    # 8.1 > Define gráfico das 10 melhores Universidades
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
    figtopu.update_layout(yaxis_categoryorder='total ascending')
    #   8.2 > Define gráfico dos Paises com mais univ no top 200
    df_topc = df_year2.loc[df_year2['Rank'] <= 200][['Country', 'Rank', 'University', 'ScoreResult']]
    countrylist = df_topc['Country'].value_counts()[:10].sort_values(ascending=False).index
    df_topc3 = df_topc[df_topc['Country'].isin(countrylist)]
    df_topc3.loc[:, 'count'] = df_topc3.groupby('Country')['Country'].transform('count')
    df_topc3 = df_topc3.sort_values(by=['count', 'Rank'], ascending=False)
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
    figtopc.update_layout(margin=dict(l=20, r=20, t=40, b=20), titlefont=dict(size=15), showlegend=False,
                          xaxis=dict(title='<i><b>Stacked Ranks', showgrid=False, zeroline=False, showticklabels=False),
                          title={'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    # 8.3 > Define gráfico de Globo
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
    # Graficos para GLOBAL END
    return figtopu, figtopc, fig_choropleth


# 9 > app.callback para Tab Países
@app.callback(
    [Output('first_card', 'children'),
     Output('second_card', 'children'),
     Output('third_card', 'children'),
     Output('country', 'figure')],
    [Input('country_drop', 'value'),
     Input('year_slider', 'value')]
)
def update_graph(country, year):
    df_cards = df.loc[(df['Year'] == 2020) & (df['Country'] == country) & (df['National_Rank'] <= 3)]
    # 9.1 > Define Card 1
    df_1cards = df_cards.loc[(df_cards['National_Rank'] == 1)]
    first_card = dbc.Card([
        html.Br(), html.Br(), html.Br(), html.Br(),
        dbc.CardHeader("Nº 1 National Rank", style={'color': colors['text']}),
        dbc.CardBody(
            [
                html.H3(df_1cards['University'], className="card-title",
                        style={'color': '#75a3a3', 'text-shadow': '1px 0px grey'}),
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
    # 9.2 > Define Card 2
    df_2cards = df_cards.loc[df['National_Rank'] == 2]
    second_card = dbc.Card([
        html.Br(), html.Br(), html.Br(), html.Br(),
        dbc.CardHeader("Nº 2 National Rank", style={'color': colors['text']}),
        dbc.CardBody(
            [
                html.H3(df_2cards['University'], className="card-title",
                        style={'color': '#75a3a3', 'text-shadow': '1px 0px grey'}),
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
    # 9.3 > Define Card 3
    df_3cards = df_cards.loc[df['National_Rank'] == 3]
    third_card = dbc.Card([
        html.Br(), html.Br(), html.Br(), html.Br(),
        dbc.CardHeader("Nº 3 National Rank", style={'opacity': '100%', 'color': colors['text']}),
        dbc.CardBody(
            [
                html.H3(df_3cards['University'], className="card-title",
                        style={'color': '#3d5c5c', 'text-shadow': '1px 0px grey'}),
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
    # 9.4 > Define Gráfico das Universidades do País
    by_year_df = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]
    full_filtered_df = by_year_df.loc[by_year_df['Country'] == country]
    fig = px.scatter(full_filtered_df,
                     x=full_filtered_df['Year'],
                     y=full_filtered_df['Rank'],
                     color=full_filtered_df['University'],
                     symbol=full_filtered_df['Country'],
                     hover_data=['University', 'National_Rank'],
                     height=400,
                     title='Ranks for Universities from ' + '<b>' + country + '</b> between ' +
                           '<b>' + str(year[0]) + '</b> and ' + '<b>' + str(year[1])
                     )
    fig.update_layout({
        'plot_bgcolor': 'rgba(95, 158, 160, 0.1)',
        'paper_bgcolor': 'rgba(95, 158, 160, 0)'
    })
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(xaxis_type='category', title={'y': 0.97, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top',
                                                    'font_color': 'black'},
                      legend=dict(x=1, y=1), titlefont=dict(size=15), margin=dict(l=300, r=5, t=40, b=5),
                      plot_bgcolor='rgba(255, 255, 255, 0.1)', paper_bgcolor='rgba(95, 158, 160, 0)')
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color='grey'), opacity=0.7),
                      selector=dict(mode='markers'))

    return first_card, second_card, third_card, fig
# Gráficos para Countries END


# 10 > app.callback para Tab Universidade
@app.callback(
    [Output('uni_evol', 'figure'),
     Output('measure1', 'figure'),
     Output('measure2', 'figure'),
     Output('measure3', 'figure'),
     Output('measure4', 'figure'),
     Output('measure5', 'figure'),
     Output('measure6', 'figure'),
     Output('measure7', 'figure'),
     Output('measure8', 'figure'),
     Output('measure9', 'figure')],
    [Input('university_drop', 'value')]
)
def update_graph(university):
    df_univ = df.loc[df['University'] == university]
    # 10.1 > Define gráfico da evolução do rank da universidade
    figun = px.scatter(df_univ, x=df_univ['Year'], y=df_univ['ScoreResult'], width=500, height=500,
                       title='<b>World Rank: Score Results <br> </b> <i> evolution 2016-2020')
    figun.update_layout(plot_bgcolor='rgba(255, 255, 255, 0.1)', paper_bgcolor='rgba(95, 158, 160, 0)',
                        titlefont=dict(size=15),
                        title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    figun.data[0].update(mode='markers+lines')
    figun.update_traces(marker=dict(size=25, color='#004080', line=dict(width=2, color='white'), opacity=0.8))

    for ano in df['Year'].unique():
        if not df_univ.loc[df_univ['Year'] == ano].empty:
            figun.add_annotation(x=ano, y=df_univ.loc[df_univ['Year'] == ano]['ScoreResult'].values[0], font=dict(size=10),
                                 text='Rank: <b>' + str(df_univ.loc[df_univ['Year'] == ano]['Rank'].values[0])
                                 , xref="x", yref="y", showarrow=True, arrowhead=7, ax=0, ay=-20,)

    # 10.2 > Define gráfico da evolução do nº de estudandes
    measure1 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Number_students'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=230, color_discrete_sequence=["DarkCyan"],
                      title='<b>Nº of Students')
    measure1.update_layout(margin=dict(l=5, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)",
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False),
                           xaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.3 > Define gráfico da evolução do nº de estudandes por funcionario
    measure2 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Numbstudentsper_Staff'], orientation='v',
                      opacity=0.9, barmode='relative', height=218, width=230, color_discrete_sequence=["CadetBlue"],
                      title='<b>Nº of Students per staff')
    measure2.update_layout(margin=dict(l=10, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)",
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False),
                           xaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.4 > Define gráfico da evolução do Teaching
    measure3 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Teaching'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=230, color_discrete_sequence=["DarkSeaGreen"],
                      title='<b>Teaching')
    measure3.update_layout(margin=dict(l=10, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)",
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False),
                           xaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.5 > Define gráfico da evolução do Research
    measure4 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Research'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=230, color_discrete_sequence=["ForestGreen"],
                      title='<b>Research')
    measure4.update_layout(margin=dict(l=10, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)",
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False),
                           xaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.6 > Define gráfico da evolução do Citations
    measure5 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Citations'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=230, color_discrete_sequence=["DarkOliveGreen"],
                      title='<b>Citations')
    measure5.update_layout(margin=dict(l=5, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)", xaxis=dict(title_text="", showgrid=False, zeroline=False),
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.7 > Define gráfico da evolução do Industry_Income
    measure6 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Industry_Income'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=230, color_discrete_sequence=["DarkSlateGrey"],
                      title='<b>Industry Outcome')
    measure6.update_layout(margin=dict(l=10, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)", xaxis=dict(title_text="", showgrid=False, zeroline=False),
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.8 > Define gráfico da evolução do International_Outlook
    measure7 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['International_Outlook'],
                      opacity=0.9, orientation='v',
                      barmode='relative', height=218, width=230, color_discrete_sequence=["Gray"],
                      title='<b>International Outlook')
    measure7.update_layout(margin=dict(l=10, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)", xaxis=dict(showgrid=False, zeroline=False),
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.9 > Define gráfico da evolução do Pct_Female
    measure8 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Pct_Female'], orientation='v', opacity=0.9,
                      barmode='stack', height=218, width=230, color_discrete_sequence=["magenta"],
                      title='<b>% Females & Males')
    aux = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['PCT_Male'])
    measure8.add_trace(aux.data[0])
    measure8.update_layout(margin=dict(l=10, r=10, t=23, b=0), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)", xaxis=dict(showgrid=False, zeroline=False),
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.10 > Define gráfico da % estudantes internacionais
    measure9 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['International_Students'], orientation='v',
                       opacity=0.9, barmode='stack', height=218, width=230, color_discrete_sequence=["#c2c2a3"],
                       title='<b>% International Students')
    measure9.update_layout(margin=dict(l=10, r=10, t=23, b=0), font=dict(size=10), titlefont=dict(size=10),
                            paper_bgcolor="rgba(95, 158, 160, 0)", xaxis=dict(showgrid=False, zeroline=False),
                            title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                            yaxis=dict(title_text="", showgrid=False, zeroline=False))

    return figun, measure1, measure2, measure3, measure4, measure5, measure6, measure7, measure8, measure9
# Gráficos para Universities END


# 11 > Define 4 scatter plots de indicadores vs score
# 11.1 > Constroi 1º gráfico
corr1 = px.scatter(df,
                   x=df['Number_students'],
                   y=df['ScoreResult'],
                   color=df['Year'].apply(str),
                   hover_data=['University'],
                   title='<b>Score Results </b><br>    vs   <br><b>Nº Students',
                   height=460, width=290,
                   color_discrete_sequence=px.colors.sequential.Viridis_r,
                   opacity=0.8
                   )
corr1.update_layout(margin=dict(l=0, r=0, t=60, b=10, pad=0),
                    title={'y': 0.97, 'x': 0.55, 'xanchor': 'center', 'yanchor': 'top'},
                    yaxis=dict(showgrid=False, zeroline=False, titlefont=dict(size=12)),
                    xaxis=dict(title_text="Nº Students", showgrid=False, zeroline=False, titlefont=dict(size=12)),
                    titlefont=dict(size=13), showlegend=True,
                    legend_orientation="h", legend_title_text='')
# 11.2 > Anotaçoes ao 1º gráfico
ax = 0
ay = -50
for ano in df['Year'].unique():
    df_ano = df.loc[df['Year'] == ano]
    minx = df_ano.loc[df_ano['Rank'] == 1]['Number_students'].values[0]
    miny = df_ano.loc[df_ano['Rank'] == 1]['ScoreResult'].values[0]
    corr1.add_annotation(x=minx, y=miny, text="1º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=ax, ay=ay, font=dict(size=7))
    ax = ax + 20
    ay = ay + 12
    rankmax = df_ano['Rank'].max()
    maxx = df_ano.loc[df_ano['Rank'] == rankmax]['Number_students'].values[0]
    maxy = df_ano.loc[df_ano['Rank'] == rankmax]['ScoreResult'].values[0]
    corr1.add_annotation(x=maxx, y=maxy, text=str(rankmax) + "º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=30, ay=0, font=dict(size=7))

corr2 = px.scatter(df,
                   x=df['Pct_Female'],
                   y=df['ScoreResult'],
                   color=df['Year'].apply(str),
                   hover_data=['University'],
                   title='<b>Score Results </b><br>    vs   <br><b>%Females',
                   height=460, width=290,
                   color_discrete_sequence=px.colors.sequential.Viridis_r,
                   opacity=0.8
                   )
corr2.update_layout(margin=dict(l=0, r=0, t=60, b=0, pad=0),
                    title={'y': 0.97, 'x': 0.56, 'xanchor': 'center', 'yanchor': 'top'},
                    yaxis=dict(showgrid=False, zeroline=False),
                    xaxis=dict(title_text="%Female", showgrid=False, zeroline=False, titlefont=dict(size=12)),
                    titlefont=dict(size=13), showlegend=True,
                    legend_orientation="h", legend_title_text='')
ax = 0
ay = -50
for ano in df['Year'].unique():
    df_ano = df.loc[df['Year'] == ano]
    minx = df_ano.loc[df_ano['Rank'] == 1]['Pct_Female'].values[0]
    miny = df_ano.loc[df_ano['Rank'] == 1]['ScoreResult'].values[0]
    corr2.add_annotation(x=minx, y=miny, text="1º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=ax, ay=ay, font=dict(size=7))
    ax = ax + 20
    ay = ay + 12
    rankmax = df_ano['Rank'].max()
    maxx = df_ano.loc[df_ano['Rank'] == rankmax]['Pct_Female'].values[0]
    maxy = df_ano.loc[df_ano['Rank'] == rankmax]['ScoreResult'].values[0]
    corr2.add_annotation(x=maxx, y=maxy, text=str(rankmax) + "º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=30, ay=0, font=dict(size=7))

corr3 = px.scatter(df,
                   x=df['Numbstudentsper_Staff'],
                   y=df['ScoreResult'],
                   color=df['Year'].apply(str),
                   hover_data=['University'],
                   title='<b>Score Results </b><br>    vs   <br><b>Nº Students per staff',
                   height=460, width=290,
                   color_discrete_sequence=px.colors.sequential.Viridis_r,
                   opacity=0.8
                   )
corr3.update_layout(margin=dict(l=0, r=0, t=60, b=0, pad=0),
                    yaxis=dict(showgrid=False, zeroline=False),
                    xaxis=dict(title_text="Nº Students per staff", showgrid=False,
                               zeroline=False, titlefont=dict(size=12)),
                    titlefont=dict(size=13), showlegend=True,
                    title={'y': 0.97, 'x': 0.56, 'xanchor': 'center', 'yanchor': 'top'},
                    legend_orientation="h", legend_title_text='')
ax = 0
ay = -50
for ano in df['Year'].unique():
    df_ano = df.loc[df['Year'] == ano]
    minx = df_ano.loc[df_ano['Rank'] == 1]['Numbstudentsper_Staff'].values[0]
    miny = df_ano.loc[df_ano['Rank'] == 1]['ScoreResult'].values[0]
    corr3.add_annotation(x=minx, y=miny, text="1º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=ax, ay=ay, font=dict(size=7))
    ax = ax + 20
    ay = ay + 12
    rankmax = df_ano['Rank'].max()
    maxx = df_ano.loc[df_ano['Rank'] == rankmax]['Numbstudentsper_Staff'].values[0]
    maxy = df_ano.loc[df_ano['Rank'] == rankmax]['ScoreResult'].values[0]
    corr3.add_annotation(x=maxx, y=maxy, text=str(rankmax) + "º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=30, ay=0, font=dict(size=7))

corr4 = px.scatter(df,
                   x=df['International_Students'],
                   y=df['ScoreResult'],
                   color=df['Year'].apply(str),
                   hover_data=['University'],
                   title='<b>Score Results </b><br>    vs   <br><b>% Students International Students',
                   height=460, width=290,
                   color_discrete_sequence=px.colors.sequential.Viridis_r,
                   opacity=0.8
                   )
corr4.update_layout(margin=dict(l=0, r=0, t=60, b=0, pad=0),
                    yaxis=dict(showgrid=False, zeroline=False),
                    xaxis=dict(title_text="% International Students", showgrid=False, zeroline=False, titlefont=dict(size=12)),
                    titlefont=dict(size=13), showlegend=True,
                    title={'y': 0.97, 'x': 0.55, 'xanchor': 'center', 'yanchor': 'top'},
                    legend_orientation="h", legend_title_text='')
ax = 0
ay = -50
for ano in df['Year'].unique():
    df_ano = df.loc[df['Year'] == ano]
    minx = df_ano.loc[df_ano['Rank'] == 1]['International_Students'].values[0]
    miny = df_ano.loc[df_ano['Rank'] == 1]['ScoreResult'].values[0]
    corr4.add_annotation(x=minx, y=miny, text="1º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=ax, ay=ay, font=dict(size=7))
    ax = ax + 20
    ay = ay + 12
    rankmax = df_ano['Rank'].max()
    maxx = df_ano.loc[df_ano['Rank'] == rankmax]['International_Students'].values[0]
    maxy = df_ano.loc[df_ano['Rank'] == rankmax]['ScoreResult'].values[0]
    corr4.add_annotation(x=maxx, y=maxy, text=str(rankmax) + "º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=30, ay=0, font=dict(size=7))


# 12 > Define botão de submissão
@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submitbutton', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks > 0:
        return 'Feedback submitted. Thank you!'



if __name__ == '__main__':
    app.run_server(debug=True)

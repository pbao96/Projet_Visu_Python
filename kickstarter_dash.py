# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
#import iso3166
import plotly.plotly as py
import plotly.figure_factory as ff
import plotly.graph_objs as go
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#ksprojects=pd.read_csv("ks-projects-201801.csv",encoding = 'utf8')
ksprojects=pd.read_csv("https://perso.esiee.fr/~hamamic/cgi-bin/R/kickstarter/ks-projects-201801.csv",encoding = 'utf8')
df = ksprojects
df = df.fillna(0)

df.drop(['usd pledged'],axis=1,inplace=True)

df['deadline'] = pd.to_datetime(df['deadline'])
df['launched'] = pd.to_datetime(df['launched'])

df = df.query("state != 'live' & state != 'undefined' & country != 'N,0\"' ")
df = df.query('20090101000000 < launched < 20180101000000')

df = df.assign(funding_percentage = (df.usd_pledged_real/df.usd_goal_real)*100)
df = df.assign(avrg_per_bckers = df.usd_pledged_real/df.backers)
df = df.assign(days_to_complete = df.deadline-df.launched)
df = df.assign(year = df.launched.dt.year)

df.days_to_complete = df.days_to_complete.dt.days

df.replace([np.inf, -np.inf], np.nan)
df = df.fillna(0)

df1 = df[(df.year == 2017) & (df.country == 'FR')].agg({'days_to_complete': ['size', 'std', 'min','mean', 'max', 'sum'], 
                                                  'backers': ['size', 'std', 'min','mean', 'max', 'sum'],
                                                  'usd_pledged_real': ['size', 'std', 'min','mean', 'max', 'sum'],
                                                  'usd_goal_real': ['size', 'std', 'min','mean', 'max', 'sum'],
                                                  'funding_percentage': ['size', 'std', 'min','mean', 'max', 'sum'],
                                                  'avrg_per_bckers': ['size', 'std', 'min','mean', 'max', 'sum']
                                                 })

       
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div([
            html.H1(
                'Projet Python: Kickstarter Data Analysis',
                style={'font-family': 'Helvetica', "margin-top": "25", "margin-bottom": "0"})
    ]),
            
    html.U(html.H2('Général')),
    
    html.Div([
        html.Div([
            html.H3('Nombre de projets par année'),
            dcc.Graph(id='g1', figure={'data': [go.Scatter(y=df.groupby('year').size().tolist(),x=sorted(df.year.unique()))]  })
        ], className="six columns"),

        html.Div([
            html.H3('Nombre de projets par année et par états de projet'),
            dcc.Graph(id='g2', figure={'data':[go.Scatter(x = sorted(df.year.unique()),y = [(df[(df.year == i) & (df.state==j)]['backers'].sum()) for i in sorted(df.year.unique())], name = j) for j in df.state.unique()]+[go.Scatter(x = sorted(df.year.unique()),y = [(df[df.year == i]['backers'].sum()) for i in sorted(df.year.unique())],name = 'sum')]})
        ], className="six columns"),
    ], className="row"),

    html.Div([
            html.H3('Nombre de jours d\'accomplissement par année'),
            dcc.Graph(id='g3', figure={'data': [go.Box(y = df[df.year == i]['days_to_complete'].tolist(),name=str(i),boxpoints= False) for i in sorted(df.year.unique())]  })
    ]),

    html.U(html.H2('Détails')),
    
    html.Div([
        html.Div([
            dcc.Slider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                value=df['year'].min(),
                marks={str(year): str(year) for year in df['year'].unique()})
        ], className="six columns"),

        html.Div([
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': str(i), 'value': i} for i in df.country.unique()],
                value = 'US')
        ], className="six columns"),
    ], className="row"),

            
    html.Div([
            html.H3('Résumé statistique'),
            dcc.Graph(id='g4')
    ]),

    html.Div([
            html.H3('Nombre de projet par état'),
            dcc.Graph(id='g5')
    ]),

    html.Div([
            html.H3("Nombre de projets par catégories avec le pourcentage des différents états de projet"),
            dcc.Graph(id='g6')
    ])

])


@app.callback(
    dash.dependencies.Output('g4', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
     dash.dependencies.Input('country-dropdown', 'value')])

def update_table(selected_year,selected_country):
 
    return {
        'data': ff.create_table( df[(df.year == selected_year) & (df.country == selected_country)].agg({'days_to_complete': ['size', 'std', 'min','mean', 'max', 'sum'], 
                                                  'backers': ['size', 'std', 'min','mean', 'max', 'sum'],
                                                  'usd_pledged_real': ['size', 'std', 'min','mean', 'max', 'sum'],
                                                  'usd_goal_real': ['size', 'std', 'min','mean', 'max', 'sum'],
                                                  'funding_percentage': ['size', 'std', 'min','mean', 'max', 'sum'],
                                                  'avrg_per_bckers': ['size', 'std', 'min','mean', 'max', 'sum']
                                                 }),index=True)
    }
        
@app.callback(
    dash.dependencies.Output('g5', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
     dash.dependencies.Input('country-dropdown', 'value')])       
    
def update_histo(selected_year,selected_country):
 
    return {
            'data':[go.Histogram(histfunc = "count",x = list(df[(df.year == selected_year) & (df.country == selected_country)].state))]
        
            
    }
    
@app.callback(
    dash.dependencies.Output('g6', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
     dash.dependencies.Input('country-dropdown', 'value')])       
    
def update_bar(selected_year,selected_country):
 
    return {
            'data':go.Figure(
                        data=[go.Bar(
                                x=df[(df.year == selected_year) & (df.country == selected_country) & (df.state == i)].main_category.value_counts().keys(),
                                y=df[(df.year == selected_year) & (df.country == selected_country) & (df.state == i)].main_category.value_counts(),
                                name=str(i) 
                                ) for i in df.state.unique()], 
                        layout = go.Layout(barmode='stack'))
            
        
            
    }    
     
if __name__ == '__main__':
    app.run_server(debug=True)
    
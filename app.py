import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import requests
import pandas as pd
import json
from fbprophet import Prophet
from fbprophet.plot import get_forecast_component_plotly_props
from fbprophet.plot import get_seasonality_plotly_props
import numpy as np

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)

#server = app.server

app.layout = html.Div([
    html.Div([
        html.H2('Dashboard Covid-19 - Unifesspa'),
        html.Img(src='/assets/LCC.png')
    ], className='banner'),

    dcc.Tabs([
        dcc.Tab(label='Casos confirmados e Óbitos', children=[
            html.Div([
                html.Div([
                    html.H3('Escolha o município'),
                    dcc.Dropdown(
                        id='dropdown_mun',
                        options=[
                            {'label': 'Marabá', 'value': 'Marabá'},
                            {'label': 'Xinguara', 'value': 'Xinguara'},
                            {'label': 'Rondon do Pará', 'value': 'Rondon do Pará'},
                            {'label': 'Santana do Araguaia', 'value': 'Santana do Araguaia'},
                            {'label': 'São Félix do Xingu', 'value': 'São Félix do Xingu'}
                        ],
                        value='Marabá',
                        multi=False,
                        clearable=False,
                        style={'width': '80%', 'font-size': '14px'}
                    )
                ], className='offset-by-one column, three columns')
            ], className='row'),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='mun_conf'
                    )
                ], className='six columns'),
                html.Div([
                    dcc.Graph(
                        id='mun_death',
                    )
                ], className='six columns')
            ], className='row'),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='mun_conf2'
                    )
                ], className='six columns'),
                html.Div([
                    dcc.Graph(
                        id='mun_death2',
                    )
                ], className='six columns')
            ], className='row')
        ]),
        dcc.Tab(label='Previsão confirmados - Marabá', children=[
            html.Div([
                html.Div([
                    html.H3('Escolha o período'),
                    dcc.Dropdown(
                        id='dropdown_prev_conf',
                        options=[
                            {'label': '1 semana', 'value': 7},
                            {'label': '2 semanas', 'value': 14}
                        ],
                        value=7,
                        multi=False,
                        clearable=False,
                        style={'width': '80%', 'font-size': '14px'}
                    )
                ], className='offset-by-one column, three columns')
            ], className='row'),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='mun_prev_conf'
                    )
                ], className='offset-by-one column, ten columns')
            ], className='row'),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='mun_trend_conf'
                    )
                ], className='offset-by-one column, five columns'),
                html.Div([
                    dcc.Graph(
                        id='mun_saz_conf',
                    )
                ], className='five columns')
            ], className='row'),
        ]),
        dcc.Tab(label='Previsão óbitos - Marabá', children=[
            html.Div([
                html.Div([
                    html.H3('Escolha o período'),
                    dcc.Dropdown(
                        id='dropdown_prev_death',
                        options=[
                            {'label': '1 semana', 'value': 7},
                            {'label': '2 semanas', 'value': 14}
                        ],
                        value=7,
                        multi=False,
                        clearable=False,
                        style={'width': '80%', 'font-size': '14px'}
                    )
                ], className='offset-by-one column, three columns')
            ], className='row'),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='mun_prev_death'
                    )
                ], className='offset-by-one column, ten columns')
            ], className='row'),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='mun_trend_death'
                    )
                ], className='offset-by-one column, five columns'),
                html.Div([
                    dcc.Graph(
                        id='mun_saz_death',
                    )
                ], className='five columns')
            ], className='row'),
        ]),
    ], style={'font-size': '14px'})
])

#--------------------------------------------------------------------------
@app.callback(
    [Output(component_id='mun_conf', component_property='figure'),
    Output(component_id='mun_death', component_property='figure'),
    Output(component_id='mun_conf2', component_property='figure'),
    Output(component_id='mun_death2', component_property='figure')],
    [Input(component_id='dropdown_mun', component_property='value')]
)

def update_graph(dropdown_mun):
    url = 'https://brasil.io/api/dataset/covid19/caso/data/?city=' + dropdown_mun + '&format=json'
    url_data = requests.get(url).content
    json_data = json.loads(url_data)
    df = pd.read_json(json.dumps(json_data['results']))
    df_conf_new = df.sort_values(by='date').confirmed.diff()
    df_death_new = df.sort_values(by='date').deaths.diff()
    df_conf_new = df_conf_new.iloc[::-1]
    df_death_new = df_death_new.iloc[::-1]
    #
    trace_conf = go.Scatter(x=list(df.date),
                            y=list(df.confirmed),
                            name='Confirmed',
                            line=dict(color='#42ecf5'))
    trace_death = go.Scatter(x=list(df.date),
                             y=list(df.deaths),
                             name='Deaths',
                             line=dict(color='#cf2525'))
    trace_conf_new = go.Scatter(x=list(df.date),
                            y=list(df_conf_new),
                            name='Confirmed_new',
                            line=dict(color='#42ecf5'))
    trace_death_new = go.Scatter(x=list(df.date),
                             y=list(df_death_new),
                             name='Deaths_new',
                             line=dict(color='#cf2525'))
    figure_conf = {
        'data': [trace_conf],
        'layout': dict(
            title='Confirmados',
            showlegend= False,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=7,
                             label='1 semana',
                             step='day',
                             stepmode='backward'),
                        dict(count=1,
                             label='1 mês',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6 meses',
                             step='month',
                             stepmode='backward'),
                        # dict(count=1,
                        #      label='1y',
                        #      step='year',
                        #      stepmode='backward'),
                        dict(label='Todos', step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )
    }

    figure_death = {
        'data': [trace_death],
        'layout': dict(
            title='Mortes',
            showlegend= False,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=7,
                             label='1 semana',
                             step='day',
                             stepmode='backward'),
                        dict(count=1,
                             label='1 mês',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6 meses',
                             step='month',
                             stepmode='backward'),
                        # dict(count=1,
                        #      label='1y',
                        #      step='year',
                        #      stepmode='backward'),
                        dict(label='Todos', step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )
    }

    figure_conf_new = {
        'data': [trace_conf_new],
        'layout': dict(
            title='Novos confirmados',
            showlegend= False,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=7,
                             label='1 semana',
                             step='day',
                             stepmode='backward'),
                        dict(count=1,
                             label='1 mês',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6 meses',
                             step='month',
                             stepmode='backward'),
                        # dict(count=1,
                        #      label='1y',
                        #      step='year',
                        #      stepmode='backward'),
                        dict(label='Todos', step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )
    }

    figure_death_new = {
        'data': [trace_death_new],
        'layout': dict(
            title='Novas mortes',
            showlegend= False,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=7,
                             label='1 semana',
                             step='day',
                             stepmode='backward'),
                        dict(count=1,
                             label='1 mês',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6 meses',
                             step='month',
                             stepmode='backward'),
                        # dict(count=1,
                        #      label='1y',
                        #      step='year',
                        #      stepmode='backward'),
                        dict(label='Todos', step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )
    }

    return figure_conf, figure_death, figure_conf_new, figure_death_new

@app.callback(
    [Output(component_id='mun_prev_conf', component_property='figure'),
     Output(component_id='mun_trend_conf', component_property='figure'),
     Output(component_id='mun_saz_conf', component_property='figure')],
    [Input(component_id='dropdown_prev_conf', component_property='value')]
)

def update_graph_prev_conf(dropdown_prev_conf):
    url = 'https://brasil.io/api/dataset/covid19/caso/data/?city=' + 'Marabá' + '&format=json'
    url_data = requests.get(url).content
    json_data = json.loads(url_data)
    df = pd.read_json(json.dumps(json_data['results']))
    df_new = df.sort_values(by='date')
    df_conf = pd.concat([df_new.date, df_new.confirmed], axis=1)
    df_conf.columns = ['ds', 'y']
    df_conf['ds'] = pd.to_datetime(df_conf['ds'])
    s_cap = df[:dropdown_prev_conf+1].confirmed
    if dropdown_prev_conf == 7:
        cap = s_cap[0] + s_cap[0] - s_cap[dropdown_prev_conf]
    else:
        cap = s_cap[0] + 1.4*(s_cap[0] - s_cap[dropdown_prev_conf])

    df_conf['cap'] = cap
    m = Prophet(interval_width=0.95, growth='logistic', weekly_seasonality=True)
    m.fit(df_conf)
    future = m.make_future_dataframe(periods=dropdown_prev_conf)
    future['cap'] = cap
    fcst = m.predict(future)
    #
    prediction_color = '#0072B2'
    error_color = 'rgba(0, 114, 178, 0.2)'  # '#0072B2' with 0.2 opacity
    actual_color = 'black'
    cap_color = 'black'
    trend_color = '#B23B00'
    line_width = 2
    marker_size = 4

    data = []
    ylabel = 'Confirmados'
    xlabel = 'Tempo'
    # Add lower bound
    data.append(go.Scatter(
        x=fcst['ds'],
        y=fcst['yhat_lower'],
        mode='lines',
        line=dict(width=0),
        hoverinfo='skip',
        showlegend=False
    ))
    # Add upper bound
    data.append(go.Scatter(
        name='Incerteza',
        x=fcst['ds'],
        y=fcst['yhat_upper'],
        mode='lines',
        line=dict(width=0),
        fillcolor=error_color,
        fill='tonexty',
        hoverinfo='skip',
        # showlegend=False
    ))
    # Add prediction
    data.append(go.Scatter(
        name='Predito',
        x=fcst['ds'],
        y=np.round(fcst['yhat']),
        mode='lines',
        line=dict(color=prediction_color, width=line_width),
        # fillcolor=error_color,
        # fill='tonexty'
    ))
    # Add actual
    data.append(go.Scatter(
        name='Real',
        x=m.history['ds'],
        y=m.history['y'],
        marker=dict(color=actual_color, size=marker_size),
        mode='markers'
    ))
    #figsize = (900, 800)
    layout = dict(
        title='Previsão confirmados',
        showlegend=False,
        #width=figsize[0],
        height=700,
        yaxis=dict(
            title=ylabel
        ),
        xaxis=dict(
            title=xlabel,
            type='date',
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                         label='1 semana',
                         step='day',
                         stepmode='backward'),
                    dict(count=1,
                         label='1 mês',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6 meses',
                         step='month',
                         stepmode='backward'),
                    # dict(count=1,
                    #      label='1ano',
                    #      step='year',
                    #      stepmode='backward'),
                    dict(label='Todos', step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        ),
    )
    figure_prev_conf = go.Figure(data=data, layout=layout)
    figure_prev_conf.update_layout(showlegend=True)

    # props = get_forecast_component_plotly_props(m, fcst, 'trend', uncertainty=True, plot_cap=False)
    #
    # layout = go.Layout(
    #     # width=figsize[0],
    #     height=700,
    #     showlegend=False,
    #     xaxis=props['xaxis'],
    #     yaxis=dict(title='Tendência')
    # )

    data = []
    ylabel = 'Tendência'
    # Add lower bound
    data.append(go.Scatter(
        x=fcst['ds'],
        y=fcst['trend_lower'],
        mode='lines',
        line=dict(width=0),
        #fillcolor=error_color,
        #fill='tonexty',
        hoverinfo='skip',
        showlegend=False
    ))
    # Add upper bound
    data.append(go.Scatter(
        name='Incerteza',
        x=fcst['ds'],
        y=fcst['trend_upper'],
        mode='lines',
        line=dict(width=0),
        fillcolor=error_color,
        fill='tonexty',
        hoverinfo='skip',
        showlegend=False
    ))
    # Add prediction
    data.append(go.Scatter(
        name='Tendência',
        x=fcst['ds'],
        y=np.round(fcst['trend']),
        mode='lines',
        line=dict(color=prediction_color, width=line_width),
        # fillcolor=error_color,
        # fill='tonexty'
    ))
    #figsize = (900, 800)
    layout = dict(
        showlegend=False,
        #width=figsize[0],
        height=700,
        yaxis=dict(
            title=ylabel
        )
    )

    fig_trend_conf = go.Figure(data=data, layout=layout)

    #print(props['traces'])

    for seasonality in m.seasonalities:
        props = get_seasonality_plotly_props(m, seasonality)
    props['xaxis'].pop('tickformat')
    props['xaxis'].pop('type')
    layout = go.Layout(
        #width=figsize[0],
        height=700,
        showlegend=False,
        xaxis=props['xaxis'],
        yaxis=dict(title='Sazonalidade')
    )

    props['traces'][0]['x'] = np.array(['Domingo', 'Segunda', 'Terça', 'Quarta',
                                        'Quinta', 'Sexta', 'Sábado'])
    fig_saz_conf = go.Figure(data=props['traces'], layout=layout)

    return figure_prev_conf, fig_trend_conf, fig_saz_conf


@app.callback(
    [Output(component_id='mun_prev_death', component_property='figure'),
     Output(component_id='mun_trend_death', component_property='figure'),
     Output(component_id='mun_saz_death', component_property='figure')],
    [Input(component_id='dropdown_prev_death', component_property='value')]
)

def update_graph_prev_death(dropdown_prev_death):
    url = 'https://brasil.io/api/dataset/covid19/caso/data/?city=' + 'Marabá' + '&format=json'
    url_data = requests.get(url).content
    json_data = json.loads(url_data)
    df = pd.read_json(json.dumps(json_data['results']))
    df_new = df.sort_values(by='date')
    df_death = pd.concat([df_new.date, df_new.deaths], axis=1)
    df_death.columns = ['ds', 'y']
    df_death['ds'] = pd.to_datetime(df_death['ds'])
    s_cap = df[:dropdown_prev_death+1].deaths
    if dropdown_prev_death == 7:
        cap = s_cap[0] + s_cap[0] - s_cap[dropdown_prev_death]
    else:
        cap = s_cap[0] + 1.4*(s_cap[0] - s_cap[dropdown_prev_death])

    df_death['cap'] = cap
    m = Prophet(interval_width=0.95, growth='logistic', weekly_seasonality=True)
    m.fit(df_death)
    future = m.make_future_dataframe(periods=dropdown_prev_death)
    future['cap'] = cap
    fcst = m.predict(future)
    #
    prediction_color = '#0072B2'
    error_color = 'rgba(0, 114, 178, 0.2)'  # '#0072B2' with 0.2 opacity
    actual_color = 'black'
    cap_color = 'black'
    trend_color = '#B23B00'
    line_width = 2
    marker_size = 4

    data = []
    ylabel = 'Óbitos'
    xlabel = 'Tempo'
    # Add lower bound
    data.append(go.Scatter(
        x=fcst['ds'],
        y=fcst['yhat_lower'],
        mode='lines',
        line=dict(width=0),
        hoverinfo='skip',
        showlegend=False
    ))
    # Add upper bound
    data.append(go.Scatter(
        name='Incerteza',
        x=fcst['ds'],
        y=fcst['yhat_upper'],
        mode='lines',
        line=dict(width=0),
        fillcolor=error_color,
        fill='tonexty',
        hoverinfo='skip',
        # showlegend=False
    ))
    # Add prediction
    data.append(go.Scatter(
        name='Predito',
        x=fcst['ds'],
        y=np.round(fcst['yhat']),
        mode='lines',
        line=dict(color=prediction_color, width=line_width),
        # fillcolor=error_color,
        # fill='tonexty'
    ))
    # Add actual
    data.append(go.Scatter(
        name='Real',
        x=m.history['ds'],
        y=m.history['y'],
        marker=dict(color=actual_color, size=marker_size),
        mode='markers'
    ))
    #figsize = (900, 800)
    layout = dict(
        title='Previsão óbitos',
        showlegend=False,
        #width=figsize[0],
        height=700,
        yaxis=dict(
            title=ylabel
        ),
        xaxis=dict(
            title=xlabel,
            type='date',
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                         label='1 semana',
                         step='day',
                         stepmode='backward'),
                    dict(count=1,
                         label='1 mês',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6 meses',
                         step='month',
                         stepmode='backward'),
                    # dict(count=1,
                    #      label='1ano',
                    #      step='year',
                    #      stepmode='backward'),
                    dict(label='Todos', step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        ),
    )
    figure_prev_death = go.Figure(data=data, layout=layout)
    figure_prev_death.update_layout(showlegend=True)

    # props = get_forecast_component_plotly_props(m, fcst, 'trend', uncertainty=True, plot_cap=False)
    #
    # layout = go.Layout(
    #     # width=figsize[0],
    #     height=700,
    #     showlegend=False,
    #     xaxis=props['xaxis'],
    #     yaxis=dict(title='Tendência')
    # )

    data = []
    ylabel = 'Tendência'
    # Add lower bound
    data.append(go.Scatter(
        x=fcst['ds'],
        y=fcst['trend_lower'],
        mode='lines',
        line=dict(width=0),
        #fillcolor=error_color,
        #fill='tonexty',
        hoverinfo='skip',
        showlegend=False
    ))
    # Add upper bound
    data.append(go.Scatter(
        name='Incerteza',
        x=fcst['ds'],
        y=fcst['trend_upper'],
        mode='lines',
        line=dict(width=0),
        fillcolor=error_color,
        fill='tonexty',
        hoverinfo='skip',
        showlegend=False
    ))
    # Add prediction
    data.append(go.Scatter(
        name='Tendência',
        x=fcst['ds'],
        y=np.round(fcst['trend']),
        mode='lines',
        line=dict(color=prediction_color, width=line_width),
        # fillcolor=error_color,
        # fill='tonexty'
    ))
    #figsize = (900, 800)
    layout = dict(
        showlegend=False,
        #width=figsize[0],
        height=700,
        yaxis=dict(
            title=ylabel
        )
    )

    fig_trend_death = go.Figure(data=data, layout=layout)

    #print(props['traces'])

    for seasonality in m.seasonalities:
        props = get_seasonality_plotly_props(m, seasonality)
    props['xaxis'].pop('tickformat')
    props['xaxis'].pop('type')
    layout = go.Layout(
        #width=figsize[0],
        height=700,
        showlegend=False,
        xaxis=props['xaxis'],
        yaxis=dict(title='Sazonalidade')
    )

    props['traces'][0]['x'] = np.array(['Domingo', 'Segunda', 'Terça', 'Quarta',
                                        'Quinta', 'Sexta', 'Sábado'])
    fig_saz_death = go.Figure(data=props['traces'], layout=layout)

    return figure_prev_death, fig_trend_death, fig_saz_death


if __name__ == '__main__':
    app.run_server(debug=True)

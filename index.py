from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dash_bootstrap_templates import ThemeSwitchAIO
import dash

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally = True
server = app.server


# ===== layout ===== #
tab_card = {'height': '100%'}

main_config = {
    'hovermode': 'x unified',
    'legend': {
        'yanchor': 'top',
        'y': 0.9,
        'xanchor': 'left',
        'x': 0.1,
        'title': {'text': None},
        'font': {'color': 'white'},
        'bgcolor': 'rgba(0,0,0,0.5)'
    },
    'margin': {'l':10, 'r': 10, 't': 10, 'b': 10}
}

config_graph = {'displayModeBar': False, 'showTips': False}

template_theme_white = 'flatly'
template_theme_dark = 'darkly'

url_theme_white = dbc.themes.FLATLY
url_theme_dark = dbc.themes.DARKLY

# reading and cleaning database

df = pd.read_csv('./data/dataset_asimov.csv')
df_aux = df.copy() # df_cru
# formatting months texts into numbers

df.loc[df['Mês'] == 'Jan', 'Mês'] = 1
df.loc[ df['Mês'] == 'Fev', 'Mês'] = 2
df.loc[ df['Mês'] == 'Mar', 'Mês'] = 3
df.loc[ df['Mês'] == 'Abr', 'Mês'] = 4
df.loc[ df['Mês'] == 'Mai', 'Mês'] = 5
df.loc[ df['Mês'] == 'Jun', 'Mês'] = 6
df.loc[ df['Mês'] == 'Jul', 'Mês'] = 7
df.loc[ df['Mês'] == 'Ago', 'Mês'] = 8
df.loc[ df['Mês'] == 'Set', 'Mês'] = 9
df.loc[ df['Mês'] == 'Out', 'Mês'] = 10
df.loc[ df['Mês'] == 'Nov', 'Mês'] = 11
df.loc[ df['Mês'] == 'Dez', 'Mês'] = 12

# cleaning database

PAID_VALUE = 'Valor Pago'
PAYMENT_STATUS = 'Status de Pagamento'
df[PAID_VALUE] = df[PAID_VALUE].str.lstrip('R$ ')
df.loc[df[PAYMENT_STATUS] == 'Pago', PAYMENT_STATUS] = 1
df.loc[df[PAYMENT_STATUS] == 'Não pago', PAYMENT_STATUS] = 0

# fixing types into numbers
df['Chamadas Realizadas'] = df['Chamadas Realizadas'].astype(int)
df['Dia'] = df['Dia'].astype(int)
df['Mês'] = df['Mês'].astype(int)
df[PAID_VALUE] = df[PAID_VALUE].astype(int)
df[PAYMENT_STATUS] = df[PAYMENT_STATUS].astype(int)

# Build filter options:

# filter of months
options_month = [{'label': 'Ano Todo', 'value': 0}]
for i, j in zip(df_aux['Mês'].unique(), df['Mês'].unique()):
    options_month.append({'label': i, 'value': j})

options_month = sorted(options_month, key=lambda x: x['value'])

# filter of teams
options_team = [{'label': 'Todas as Equipes', 'value': 0}]
for i in df['Equipe'].unique():
    options_team.append({'label': i, 'value': i})


# ===== layout ===== #
app.layout = dbc.Container(
    children=[

        # Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([  
                                html.Legend("Sales Analytics")
                            ], sm=8),
                            dbc.Col([        
                                html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                            ], sm=4, align="center")
                        ]),
                        dbc.Row([
                            dbc.Col([
                                ThemeSwitchAIO(aio_id="theme", themes=[url_theme_white, url_theme_dark]),
                                html.Legend("Asimov Academy")
                            ])
                        ], style={'margin-top': '10px'}),
                        dbc.Row([
                            dbc.Button("Visite o Site", href="https://asimov.academy/", target="_blank")
                        ], style={'margin-top': '10px'})
                    ])
                ], style=tab_card)
            ], sm=4, lg=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col(
                                html.Legend('Top Consultores por Equipe')
                            )
                        ),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='graph1', className='dbc', config=config_graph)
                            ], sm=12, md=7),
                            dbc.Col([
                                dcc.Graph(id='graph2', className='dbc', config=config_graph)
                            ], sm=12, lg=5)
                        ])
                    ])
                ], style=tab_card)
            ], sm=12, lg=7),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col([
                                html.H5('Escolha o Mês'),
                                dbc.RadioItems(
                                    id="radio-month",
                                    options=options_month,
                                    value=0,
                                    inline=True,
                                    labelCheckedClassName="text-success",
                                    inputCheckedClassName="border border-success bg-success",
                                ),
                                html.Div(id='month-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                            ])
                        )
                    ])
                ], style=tab_card)
            ], sm=12, lg=3)
        ], className='g-2 my-auto', style={'margin-top': '7px'}),

        # Row 2
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph3', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph4', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ])
                ], className='g-2 my-auto', style={'margin-top': '7px'})
            ], sm=12, lg=5),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph5', className='dbc', config=config_graph)    
                            ])
                        ], style=tab_card)
                    ], sm=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph6', className='dbc', config=config_graph)    
                            ])
                        ], style=tab_card)
                    ], sm=6)
                ], className='g-2'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dcc.Graph(id='graph7', className='dbc', config=config_graph)
                        ], style=tab_card)
                    ])
                ], className='g-2 my-auto', style={'margin-top': '7px'})
            ], sm=12, lg=4),
            dbc.Col([
                dbc.Card([
                    dcc.Graph(id='graph8', className='dbc', config=config_graph)
                ], style=tab_card)
            ], sm=12, lg=3)
        ], className='g-2 my-auto', style={'margin-top': '7px'}),
        
        # Row 3
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Distribuição de Propaganda'),
                        dcc.Graph(id='graph9', className='dbc', config=config_graph)
                    ])
                ], style=tab_card)
            ], sm=12, lg=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Valores de Propaganda convertidos por mês"),
                        dcc.Graph(id='graph10', className='dbc', config=config_graph)
                    ])
                ], style=tab_card)
            ], sm=12, lg=5),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='graph11', className='dbc', config=config_graph)
                    ])
                ], style=tab_card)
            ], sm=12, lg=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Escolha a Equipe'),
                        dbc.RadioItems(
                            id="radio-team",
                            options=options_team,
                            value=0,
                            inline=True,
                            labelCheckedClassName="text-warning",
                            inputCheckedClassName="border border-warning bg-warning",
                        ),
                        html.Div(id='team-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                    ])
                ], style=tab_card)
            ], sm=12, lg=2),
        ], className='g-2 my-auto', style={'margin-top': '7px'})

    ], fluid=True, style={'height': '100vh'}
)


# ===== start ===== #
if __name__ == 'main':
    app.run_server(debug=True, port=8050)
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


app.layout = dbc.Container(
    children=[

    ], fluid=True, style={'height': '100vh'}
)


# ===== start ===== #
if __name__ == 'main':
    app.run_server(debug=True, port=8050)
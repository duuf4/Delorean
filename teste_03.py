import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2("Meu Programa"),
    html.Label("Cadastro de Alunos"),
    html.Div([
        'Nome: ',
        dbc.Input(id = 'entrada_01',
                  value='',
                  type='text'),
    
    html.P(),
    html.Div(id='saida_01')
    

    ])

])

@app.callback(Output('saida_01', 'children'),
              [Input('entrada_01', 'value')])

def mostra_nome(e):
    return f'Bem vindo(a) {e} !!!'


app.run()


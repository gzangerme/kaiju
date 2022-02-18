import pandas as pd
from dash import Dash, html, dcc, dash
import plotly.express as px
from dash.dependencies import Input, Output



# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("intro_bees.csv")

df = df.groupby(['KR', 'ANSI', 'Objetivo', 'MesRef'])[['Valor']].mean()
df.reset_index(inplace=True)
print(df[:5])

objectives = ["Objetivo 1", "Objetivo 2"]

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("OKRs Coord Oper Varejo 2022", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_impact",
                 options=[{"label": x, "value":x} for x in objectives],
                 value="Objetivos",
                 multi=False,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_okr_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_okr_map', component_property='figure')],
    [Input(component_id='slct_impact', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "O Objetivo escolhido foi: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Objetivo"] == option_slctd]
    dff = dff[(dff["KR"] == "KR1") | (dff["KR"] == "KR2")]

    fig = px.line(
        data_frame=dff,
        x='MesRef',
        y='Valor',
        color='KR',
        template='plotly_dark'
    )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
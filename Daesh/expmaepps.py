import datetime
import io
import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input , Output, State

df = pd.read_csv('AEMB.csv')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
app.layout = dash_table.DataTable(
    style_data={'whiteSpace': 'normal'},
    css=[{
    'selector': '.dash-cell div.dash-cell-value',
    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
}],
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict("rows"),
    style_table={
        'maxHeight': '500',
        'overflowY': 'scroll'
    },
    editable=True
)


if __name__ == '__main__':
    app.run_server(debug=True)

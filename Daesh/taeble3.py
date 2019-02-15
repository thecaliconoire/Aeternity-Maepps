import base64
import datetime
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
    'maxHeight': '300',
    'overflowY': 'scroll'
},
)

app.layout = html.Div([
    dcc.Upload(
        id='datatable-upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
        },
    ),
    dash_table.DataTable(id='datatable-upload-container'),
    dcc.Graph(id='datatable-upload-graph')
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


@app.callback(Output('datatable-upload-container', 'data'),
              [Input('datatable-upload', 'contents')],
              [State('datatable-upload', 'filename')])
def update_output(contents, filename):
    if contents is None:
        return [{}]
    df = parse_contents(contents, filename)
    return df.to_dict('rows')


@app.callback(Output('datatable-upload-graph', 'figure'),
              [Input('datatable-upload-container', 'data')])
def display_graph(rows):
    df = pd.DataFrame(rows)
    return {
        'data': [{
            'x': df[df.columns[0]],
            'y': df[df.columns[1]],
            'type': 'dash_table'
        }]
    }


if __name__ == '__main__':
    app.run_server(debug=True)

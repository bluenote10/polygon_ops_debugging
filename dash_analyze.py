import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import json
import pandas as pd

import analyze_debug_log

args = analyze_debug_log.parse_args()

json_lines = analyze_debug_log.read_file(args.debug_file)
analyze_debug_log.replace_ids(json_lines)
bb = analyze_debug_log.extract_bounding_box(json_lines)

json_lines = [line for line in json_lines if "processEvent" in line]

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='iteration-slider',
        min=0,
        max=len(json_lines),
        value=0,
        marks={str(i): str(i) for i in range(len(json_lines))},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('iteration-slider', 'value')])
def update_figure(index):
    """
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(dict(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))
    """
    traces = []
    event = json_lines[index]["processEvent"]
    print(event)

    p_from = event["self"]["point"]
    p_from_x = p_from["x"]
    p_from_y = p_from["y"]
    p_upto = event["other"]["point"]
    p_upto_x = p_upto["x"]
    p_upto_y = p_upto["y"]

    if event["self"]["type"] == "L":
        color = "#00FF00"
    else:
        color = "#FF0000"

    traces.append(dict(
        x=[p_from_x, p_upto_x],
        y=[p_from_y, p_upto_y],
        mode="lines",
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': color}
        },
        showlegend=False,
    ))
    traces.append(dict(
        x=[p_from_x],
        y=[p_from_y],
        mode='markers',
        opacity=0.8,
        marker={
            'color': color,
            'size': 5,
            'line': {'width': 0.5, 'color': "#000000"}
        },
        name=event["self"]["addr"],
        hoverinfo="text",
        hovertext=["{} ({}, {})".format(event["self"]["addr"], json.dumps(p_from_x), json.dumps(p_from_y))],
    ))
    traces.append(dict(
        x=[p_upto_x],
        y=[p_upto_y],
        mode='markers',
        opacity=0.8,
        marker={
            'color': "#DDDDDD",
            'size': 5,
            'line': {'width': 0.5, 'color': "#000000"}
        },
        name=event["other"]["addr"],
        hoverinfo="text",
        hovertext=["{} ({}, {})".format(event["other"]["addr"], json.dumps(p_upto_x), json.dumps(p_upto_y))],
    ))

    offset_x = (bb[1] - bb[0]) * 0.03
    offset_y = (bb[3] - bb[2]) * 0.03
    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'x', 'range': [bb[0] - offset_x, bb[1] + offset_x]},
            yaxis={'title': 'y', 'range': [bb[2] - offset_y, bb[3] + offset_y]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest',
            #transition={'duration': 500},
        )
    }


#def main():


if __name__ == '__main__':
    app.run_server(debug=True)
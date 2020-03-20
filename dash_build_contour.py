#!/usr/bin/env python

import collections
import json

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

data = """
Coordinate { x: -15.0, y: -15.0 }
jumping to pos 16
Coordinate { x: 285.0, y: -15.0 }
searched to pos 17
jumping to pos 14
Coordinate { x: 195.0, y: 93.0 }
searched to pos 15
jumping to pos 18
Coordinate { x: 300.0, y: 240.0 }
searched to pos 19
jumping to pos 3
Coordinate { x: 0.0, y: 240.0 }
searched to pos 2
jumping to pos 5
Coordinate { x: 91.15384615384616, y: 112.38461538461539 }
searched to pos 6
jumping to pos 10
Coordinate { x: 150.0, y: 30.0 }
searched to pos 11
jumping to pos 12
Coordinate { x: 195.0, y: 93.0 }
searched to pos 13
jumping to pos 9
Coordinate { x: 135.0, y: 165.0 }
searched to pos 8
jumping to pos 7
Coordinate { x: 91.15384615384616, y: 112.38461538461539 }
searched to pos 4
jumping to pos 1
Coordinate { x: -15.0, y: -15.0 }
"""

def prepare_data():
    points = [
        json.loads(line.strip("Coordinate").replace('x', '"x"').replace('y', '"y"'))
        for line in data.split("\n")
        if line.startswith("Coordinate")
    ]

    min_x = min([p["x"] for p in points])
    max_x = max([p["x"] for p in points])
    min_y = min([p["y"] for p in points])
    max_y = max([p["y"] for p in points])
    bb = min_x, max_x, min_y, max_y

    return points, bb


class Event(object):
    def __init__(self, event):
        self.event = event
        self.from_x = event["self"]["point"][0]
        self.from_y = event["self"]["point"][1]
        self.upto_x = event["other"]["point"][0]
        self.upto_y = event["other"]["point"][1]

        self.is_left = event["self"]["type"] == "L"

        if self.is_left:
            self.color = "#00FF00"
        else:
            self.color = "#FF0000"

        self.segment = [
            self.from_x,
            self.from_y,
            self.upto_x,
            self.upto_y,
        ]


def trace_line(segment, name=None, color=None):
    from_x, from_y, upto_x, upto_y = segment
    return dict(
        x=[from_x, upto_x],
        y=[from_y, upto_y],
        mode="lines",
        color=color,
        line=dict(
            color=color,
        ),
        opacity=0.8,
        showlegend=name is not None,
        name=name,
    )


def trace_markers(xs, ys, color, name, symbol="circle", size=5):
    hovertext = [
        "{} ({}, {})".format(name, json.dumps(x), json.dumps(y))
        for x, y in zip(xs, ys)
    ]
    return dict(
        x=xs,
        y=ys,
        mode='markers',
        opacity=0.8,
        marker={
            'symbol': symbol,
            'color': color,
            'size': size,
            'line': {'width': 0.5, 'color': "#000000"}
        },
        name=name,
        hoverinfo="text",
        hovertext=hovertext,
    )


class AppData(object):
    def __init__(self):
        self.points = None
        self.bb = None


def init_app():
    app = dash.Dash(
        __name__,
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
    )

    app_data = AppData()

    def reload_app():
        points, bb = prepare_data()
        app_data.points = points
        app_data.bb = bb
        return html.Div([
            dcc.Slider(
                id='iteration-slider',
                min=0,
                max=len(points) - 1,
                value=0,
                marks={str(i): str(i) for i in range(len(points))},
            ),
            dcc.Graph(
                id='graph-with-slider',
            ),
            dcc.Textarea(
                id='textarea',
                value='',
                readOnly=True,
                rows=20,
                style={
                    'width': '100%',
                    'height': '300px',
                    'font-family': 'monospace',
                }
            ),
        ])

    app.layout = reload_app

    @app.callback(
        Output('graph-with-slider', 'figure'),
        [Input('iteration-slider', 'value')],
    )
    def update_figure(index):
        traces = []

        point = app_data.points[index]

        traces.append(trace_markers([point["x"]], [point["y"]], "#000000", "point", size=7))

        bb = app_data.bb
        offset_x = (bb[1] - bb[0]) * 0.03
        offset_y = (bb[3] - bb[2]) * 0.03
        return {
            'data': traces,
            'layout': dict(
                xaxis={'title': 'x', 'range': [bb[0] - offset_x, bb[1] + offset_x]},
                yaxis={'title': 'y', 'range': [bb[2] - offset_y, bb[3] + offset_y]},
                margin={'l': 100, 'b': 50, 't': 50, 'r': 300},
                hovermode='closest',
                legend={'x': 1.1, 'y': 0.5},
                # transition={'duration': 500},
            )
        }

    """
    @app.callback(
        Output('textarea', 'value'),
        [Input('iteration-slider', 'value')],
    )
    def update_text(index):
        iteration = app_data.iterations_data[index]
        text = "\n".join([
            str(line)
            for line in iteration.lines
        ])
        return text
    """
    
    return app


def main():
    app = init_app()
    app.run_server(debug=True, dev_tools_ui=True)


if __name__ == '__main__':
    main()

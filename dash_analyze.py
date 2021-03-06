import collections
import json

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import analyze_debug_log


def prepare_data(args):
    json_lines = analyze_debug_log.read_file(args.debug_file)

    analyze_debug_log.replace_ids(json_lines)
    bb = analyze_debug_log.extract_bounding_box(json_lines)
    iterations_data = analyze_debug_log.group_by_iteration(json_lines)

    return iterations_data, bb


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
        self.iterations_data = None
        self.bb = None


def init_app(args):
    app = dash.Dash(
        __name__,
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
    )

    app_data = AppData()

    def reload_app():
        iterations_data, bb = prepare_data(args)
        app_data.iterations_data = iterations_data
        app_data.bb = bb
        return html.Div([
            dcc.Slider(
                id='iteration-slider',
                min=0,
                max=len(iterations_data) - 1,
                value=0,
                marks={str(i): str(i) for i in range(len(iterations_data))},
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

        for iteration in app_data.iterations_data:
            e = Event(iteration.process_event)
            traces.append(trace_line(e.segment, name=None, color="#eeeeee"))

        iteration = app_data.iterations_data[index]
        print(index, iteration)

        process_event = iteration.process_event
        se_next_event = iteration.se_next_event
        se_prev_event = iteration.se_prev_event
        se_post_next_event = iteration.se_post_next_event
        se_post_prev_event = iteration.se_post_prev_event
        intersections = iteration.intersections

        if se_next_event is not None:
            e = Event(se_next_event)
            traces.append(trace_line(e.segment, "next", color="#e3cc00"))
        if se_prev_event is not None:
            e = Event(se_prev_event)
            traces.append(trace_line(e.segment, "prev", color="#8f43e6"))
        if se_post_next_event is not None:
            e = Event(se_post_next_event)
            traces.append(trace_line(e.segment, "on-remove next", color="#e3cc00"))
        if se_post_prev_event is not None:
            e = Event(se_post_prev_event)
            traces.append(trace_line(e.segment, "on-remove prev", color="#8f43e6"))
        for i, intersection in enumerate(intersections):
            x = intersection[0]
            y = intersection[1]
            traces.append(trace_markers([x], [y], "#000000", "intersection {}".format(i + 1), symbol="x", size=7))

        e = Event(process_event)
        traces.append(trace_line(e.segment, "current", color="#1f77b4"))
        traces.append(trace_markers([e.from_x], [e.from_y], e.color, process_event["self"]["addr"]))
        traces.append(trace_markers([e.upto_x], [e.upto_y], "#DDDDDD", process_event["other"]["addr"]))

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

    return app


def main():
    args = analyze_debug_log.parse_args()
    app = init_app(args)
    app.run_server(debug=True, dev_tools_ui=True)


if __name__ == '__main__':
    main()

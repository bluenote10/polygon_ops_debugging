import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import json
import pandas as pd

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
        self.from_x = event["self"]["point"]["x"]
        self.from_y = event["self"]["point"]["y"]
        self.upto_x = event["other"]["point"]["x"]
        self.upto_y = event["other"]["point"]["y"]

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


def init_app(iterations_data, bb):
    app = dash.Dash(
        __name__,
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
    )

    app.layout = html.Div([
        dcc.Graph(
            id='graph-with-slider',
        ),
        dcc.Slider(
            id='iteration-slider',
            min=0,
            max=len(iterations_data),
            value=0,
            marks={str(i): str(i) for i in range(len(iterations_data))},
        )
    ])

    @app.callback(
        Output('graph-with-slider', 'figure'),
        [Input('iteration-slider', 'value')],
    )
    def update_figure(index):
        iteration = iterations_data[index]
        print(index, iteration)

        traces = []
        process_event = iteration["processEvent"]
        se_next_event = iteration.get("seNextEvent")
        se_prev_event = iteration.get("sePrevEvent")
        se_post_next_event = iteration.get("sePostNextEvent")
        se_post_prev_event = iteration.get("sePostPrevEvent")
        intersections = iteration.get("intersections", [])

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
            x = intersection["x"]
            y = intersection["y"]
            traces.append(trace_markers([x], [y], "#000000", "intersection {}".format(i + 1), symbol="x", size=7))

        e = Event(process_event)
        traces.append(trace_line(e.segment, "current", color="#1f77b4"))
        traces.append(trace_markers([e.from_x], [e.from_y], e.color, process_event["self"]["addr"]))
        traces.append(trace_markers([e.upto_x], [e.upto_y], "#DDDDDD", process_event["other"]["addr"]))

        """
        if "computeFields" in iteration:
            df = pd.DataFrame(iteration["computeFields"])
        else:
            df = pd.DataFrame()
        keys, values = zip(*iteration["computeFields"].items())
        table = dash_table.DataTable(
            id='table',
            columns=[{"keys": keys, "values": values}],
            data=df.to_dict('records'),
        )
        """
        title = "Right event" if iteration.get("computeFields") is None else str(iteration["computeFields"])

        offset_x = (bb[1] - bb[0]) * 0.03
        offset_y = (bb[3] - bb[2]) * 0.03
        return {
            'data': traces,
            'layout': dict(
                title=title,
                xaxis={'title': 'x', 'range': [bb[0] - offset_x, bb[1] + offset_x]},
                yaxis={'title': 'y', 'range': [bb[2] - offset_y, bb[3] + offset_y]},
                margin={'l': 100, 'b': 50, 't': 50, 'r': 300},
                hovermode='closest',
                legend={'x': 1.1, 'y': 0.5},
                # transition={'duration': 500},
            )
        }

    return app


def main():
    args = analyze_debug_log.parse_args()
    iterations_data, bb = prepare_data(args)
    app = init_app(iterations_data, bb)
    app.run_server(debug=True)


if __name__ == '__main__':
    main()

import logging
import threading
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
from typing import List


class Plot:
    def updateData(__numberGame: int, __score: int, __step: int) -> None:
        Plot.__resultsHistory[0].append(__numberGame)
        Plot.__resultsHistory[1].append(__score)
        Plot.__resultsHistory[2].append(__step)

    def startServerPlot() -> None:
        Plot.__resultsHistory: List[List[int], List[int], List[int]] = [[], [], []]
        Plot.__app: dash.Dash = dash.Dash(__name__)
        __log: logging = logging.getLogger('werkzeug')
        __log.disabled: bool = True

        Plot.__app.layout: html.Div = html.Div([
            dcc.Graph(
                id='live-graph',
                animate=True,
                figure={
                    'data': [
                        {'x': [], 'y': [], 'type': 'line', 'name': 'Score'},
                        {'x': [], 'y': [], 'type': 'line', 'name': 'Step'}
                    ],
                    'layout': {
                        'title': 'Result history',
                        'xaxis': {
                            'title': 'Number game'
                        },
                        'yaxis': {
                            'title': 'Score / Step'
                        }
                    }
                }),
            dcc.Interval(
                id='interval-component',
                interval=1000,
                n_intervals=0
            ),
        ])

        @Plot.__app.callback(Output('live-graph', 'figure'),
                           [Input('interval-component', 'n_intervals')])

        def __updateGraph(n: int):
            data = {'x': Plot.__resultsHistory[0], 'score': Plot.__resultsHistory[1], 'step': Plot.__resultsHistory[2]}
            figure = {'data': [
                {'x': data['x'], 'y': data['score'], 'type': 'line', 'name': 'Score'},
                {'x': data['x'], 'y': data['step'], 'type': 'line', 'name': 'Step'}
            ],
                'layout': {
                    'title': 'Result history',
                    'xaxis': {
                        'title': 'Number game'
                    },
                    'yaxis': {
                        'title': 'Score / Step'
                    }
                }}
            return figure

        Plot.__dashThread: threading.Thread = threading.Thread(target=Plot.__app.run_server)
        Plot.__dashThread.start()

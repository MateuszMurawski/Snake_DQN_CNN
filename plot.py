import logging
import threading
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
from typing import List


class Plot:
    def updateData(__numberGame: int, __score: int, __step: int) -> None:
        Plot.__resultsHistory[0].append(__numberGame)
        Plot.__resultsHistory[1].append(__score)
        Plot.__resultsHistory[2].append(__step)

    def __listToAverageList() -> List:
        if Plot.__interval == 1:
            Plot.__titlePlot = "Result history - All results"
            return Plot.__resultsHistory

        __resultsHistoryAverage: List[List[int], List[int], List[int]] = [[], [], []]
        __sumScore: int = 0
        __sumStep: int = 0

        for i in range(len(Plot.__resultsHistory[0])):
            if (i + 1) % Plot.__interval != 0:
                __sumScore = __sumScore + Plot.__resultsHistory[1][i]
                __sumStep = __sumStep + Plot.__resultsHistory[2][i]
            else:
                __sumScore = __sumScore + Plot.__resultsHistory[1][i]
                __sumStep = __sumStep + Plot.__resultsHistory[2][i]

                __resultsHistoryAverage[0].append((i // Plot.__interval) + 1)
                __resultsHistoryAverage[1].append(__sumScore / Plot.__interval)
                __resultsHistoryAverage[2].append(__sumStep / Plot.__interval)

                __sumScore = 0
                __sumStep = 0

        return __resultsHistoryAverage

    def __listToMedianList() -> List:
        if Plot.__interval == 1:
            Plot.__titlePlot = "Result history - All results"
            return Plot.__resultsHistory

        __resultsHistoryMedian: List[List[int], List[int], List[int]] = [[], [], []]
        __listScore: List[int] = []
        __listStep: List[int] = []

        for i in range(len(Plot.__resultsHistory[0])):
            if (i + 1) % Plot.__interval != 0:
                __listScore.append(Plot.__resultsHistory[1][i])
                __listStep.append(Plot.__resultsHistory[2][i])
            else:
                __listScore.append(Plot.__resultsHistory[1][i])
                __listStep.append(Plot.__resultsHistory[2][i])

                __listScore.sort()
                __listStep.sort()

                __resultsHistoryMedian[0].append((i // Plot.__interval) + 1)

                if Plot.__interval % 2 == 0:
                    __resultsHistoryMedian[1].append(
                        (__listScore[Plot.__interval // 2] + __listScore[(Plot.__interval // 2) - 1]) / 2)
                    __resultsHistoryMedian[2].append(
                        (__listStep[Plot.__interval // 2] + __listStep[(Plot.__interval // 2) - 1]) / 2)

                else:
                    __resultsHistoryMedian[1].append(__listScore[Plot.__interval // 2])
                    __resultsHistoryMedian[2].append(__listStep[Plot.__interval // 2])

                __listScore.clear()
                __listStep.clear()

        return __resultsHistoryMedian

    def __checkVale(value: int) -> int:
        if type(value) != int:
            return 1
        elif value <= 0:
            return 1

        return value

    def startServerPlot() -> None:
        Plot.__resultsHistory: List[List[int], List[int], List[int]] = [[], [], []]
        Plot.__mode: int = 0
        Plot.__interval: int = 1
        Plot.__titlePlot: str = "Result history - All results"

        Plot.__app: dash.Dash = dash.Dash(__name__)

        __log: logging = logging.getLogger('werkzeug')
        __log.disabled: bool = True

        Plot.__app.layout: html.Div = html.Div([
            html.Div(dcc.Input(id='input-on-submit', type='number')),
            html.Button('All results', id='submit-all', n_clicks=0),
            html.Button('Average', id='submit-average', n_clicks=0),
            html.Button('Median', id='submit-median', n_clicks=0),
            dcc.Graph(
                id='live-graph',
                animate=True,
                figure={
                    'data': [
                        {'x': [], 'y': [], 'type': 'line', 'name': 'Score'},
                        {'x': [], 'y': [], 'type': 'line', 'name': 'Step'}
                    ],
                    'layout': {
                        'title': Plot.__titlePlot,
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
                             [Input('interval-component', 'n_intervals'),
                              Input('submit-all', 'n_clicks'),
                              Input('submit-average', 'n_clicks'),
                              Input('submit-median', 'n_clicks'),
                              State('input-on-submit', 'value')])
        def __updateGraph(n: int, n_clicks1: int, n_clicks2: int, n_clicks3: int, value: int):
            if "submit-all" == dash.ctx.triggered_id:
                Plot.__mode = 0
            elif "submit-average" == dash.ctx.triggered_id:
                Plot.__mode = 1
                Plot.__interval = Plot.__checkVale(value)
            elif "submit-median" == dash.ctx.triggered_id:
                Plot.__mode = 2
                Plot.__interval = Plot.__checkVale(value)

            if (Plot.__mode == 0):
                Plot.__listToPlot = Plot.__resultsHistory
                Plot.__titlePlot = "Result history - All results"

            if (Plot.__mode == 1):
                Plot.__listToPlot = Plot.__listToAverageList()
                Plot.__titlePlot = "Result history - Average 1/" + str(Plot.__interval)

            if (Plot.__mode == 2):
                Plot.__listToPlot = Plot.__listToMedianList()
                Plot.__titlePlot = "Result history - Median 1/" + str(Plot.__interval)

            data = {'x': Plot.__listToPlot[0], 'score': Plot.__listToPlot[1], 'step': Plot.__listToPlot[2]}
            figure = {'data': [
                {'x': data['x'], 'y': data['score'], 'type': 'line', 'name': 'Score'},
                {'x': data['x'], 'y': data['step'], 'type': 'line', 'name': 'Step'}
            ],
                'layout': {
                    'title': Plot.__titlePlot,
                    'xaxis': {
                        'title': 'Number game'
                    },
                    'yaxis': {
                        'title': 'Score / Step'
                    }
                }}
            return figure

        Plot.__dashThread: threading.Thread = threading.Thread(target=Plot.__app.run_server, args=("0.0.0.0",))
        Plot.__dashThread.start()

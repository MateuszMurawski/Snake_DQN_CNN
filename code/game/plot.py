from logging import getLogger
from threading import Thread
from dash import Dash, dcc, html, ctx
from dash.dependencies import Output, Input, State
from typing import List


class Plot:
    """
    A class representing a server that displays a graph of game results on a web page.
    """

    @staticmethod
    def startServerPlot() -> None:
        """
        Initializes and starts a Dash server to display a live graph of game results.
        The function creates a Dash app with a live graph that shows the score and step history of the games played.
        The user can choose to display all results, the average of every n results, or the median of every n results,
        where n is a user-defined value. The graph updates every 5 seconds. The default site address is: 127.0.0.1:8050

        Returns:
            None
        """

        Plot.__resultsHistory: List = [[], [], []]
        Plot.__mode: int = 0
        Plot.__interval: int = 1
        Plot.__titlePlot: str = "Result history - All results"

        Plot.__app: Dash = Dash(__name__)
        Plot.__app.title: str = "Snake game - result history"

        getLogger('werkzeug').disabled = True

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
                interval=5000,
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
            if "submit-all" == ctx.triggered_id:
                Plot.__mode = 0

            elif "submit-average" == ctx.triggered_id:
                Plot.__mode = 1
                Plot.__interval = Plot.__checkVale(value)

            elif "submit-median" == ctx.triggered_id:
                Plot.__mode = 2
                Plot.__interval = Plot.__checkVale(value)

            if Plot.__mode == 0:
                Plot.__listToPlot = Plot.__resultsHistory
                Plot.__titlePlot = "Result history - All results"

            elif Plot.__mode == 1:
                Plot.__listToPlot = Plot.__listToAverageList()
                Plot.__titlePlot = "Result history - Average 1/" + str(Plot.__interval)

            elif Plot.__mode == 2:
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

        Plot.__dashThread: Thread = Thread(target=Plot.__app.run_server, args=("0.0.0.0",))
        Plot.__dashThread.start()

    @staticmethod
    def __listToAverageList() -> List:
        """
        Converts the results history list to a list of average values, based on the specified interval.

        Returns:
            List: A list of average values for the results history. If the interval is 1, returns the original results history.
        """

        if Plot.__interval == 1:
            Plot.__titlePlot = "Result history - All results"
            return Plot.__resultsHistory

        __resultsHistoryAverage: List = [[], [], []]
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

    @staticmethod
    def __listToMedianList() -> List:
        """
        Converts the results history list to a list of median values, based on the specified interval.

        Returns:
            List: A list of median values for the results history. If the interval is 1, returns the original results history.
        """

        if Plot.__interval == 1:
            Plot.__titlePlot = "Result history - All results"
            return Plot.__resultsHistory

        __resultsHistoryMedian: List = [[], [], []]
        __listScore: List = []
        __listStep: List = []

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
                    __resultsHistoryMedian[1].append((__listScore[Plot.__interval // 2] + __listScore[(Plot.__interval // 2) - 1]) / 2)
                    __resultsHistoryMedian[2].append((__listStep[Plot.__interval // 2] + __listStep[(Plot.__interval // 2) - 1]) / 2)

                else:
                    __resultsHistoryMedian[1].append(__listScore[Plot.__interval // 2])
                    __resultsHistoryMedian[2].append(__listStep[Plot.__interval // 2])

                __listScore.clear()
                __listStep.clear()

        return __resultsHistoryMedian

    @staticmethod
    def __checkVale(value: int) -> int:
        """
        Checks if the provided value is a positive integer.

        Args:
            value (int): The value to be checked.

        Returns:
            int: The checked value. If the provided value is not a positive integer, returns 1.
        """

        if type(value) != int:
            return 1
        elif value <= 0:
            return 1

        return value

    @staticmethod
    def updateData(numberGame: int, score: int, step: int) -> None:
        """
        Updates the results history list with the provided values.

        Args:
            numberGame (int): The number of the game.
            score (int): The score obtained in the game.
            step (int): The number of steps taken in the game.

        Returns:
            None
        """

        Plot.__resultsHistory[0].append(numberGame)
        Plot.__resultsHistory[1].append(score)
        Plot.__resultsHistory[2].append(step)

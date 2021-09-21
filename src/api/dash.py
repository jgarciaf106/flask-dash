from flask import Blueprint
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd


def dash_app(flask_server):
    app = dash.Dash(__name__, server=flask_server)

    df = pd.DataFrame(
        {
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
        }
    )

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    app.layout = html.Div(
        children=[
            html.H1(children="Hello Dash"),
            html.Div(
                children="""
            Dash: A web application framework for your data.
        """
            ),
            dcc.Graph(id="example-graph", figure=fig),
        ]
    )

    return app

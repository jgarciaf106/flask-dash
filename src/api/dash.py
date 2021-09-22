import datetime as dt
import sys
import os

sys.path.append("./src/")
from flask import Blueprint
import dash
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd


# import data.data_getter as dg


def dash_app(flask_server):
    # bootstrap
    BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css"
    # initialize dash app
    app = dash.Dash(__name__, server=flask_server, external_stylesheets=[BS])

    # set db engine
    # engine = dg.set_engine('credentials','HRODS')

    # # query db

    # div_data = hr.externalQuery('DEI_New_HP', engine)

    # data path
    dir_name = os.getcwd()
    data_path = dir_name + "\src\data_files\data_output.xlsx"

    # read data
    df = pd.read_excel(data_path)

    ## change date format
    df["Date Value"] = pd.to_datetime(df["Report Date"], errors="coerce")

    df["Date"] = df["Date Value"].dt.strftime("%Y/%m/%d")

    ## remove unformatted date fields
    del df["Report Date"]
    del df["Date Value"]

    ## reorder formatted date column
    col = df.pop("Date")
    df.insert(0, col.name, col)

    ## rename date field
    df = df.rename(columns={"Date": "Report Date"})

    # components

    fig = dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        filter_action="native",
        style_table={
            "height": 400,
        },
        style_data={
            "width": "150px",
            "minWidth": "150px",
            "maxWidth": "150px",
            "overflow": "hidden",
            "textOverflow": "ellipsis",
        },
    )

    NAV_LOGO = "https://brandcentral.hp.com/content/dam/sites/brand-central/downloads/logos/HP_Logo_White_RGB.png"
    navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=NAV_LOGO, height="85px", className="ml-5")),
                        dbc.Col(dbc.NavbarBrand("Dashboard", className="ml-2")),
                    ],
                    align="center",
                    #no_gutters=True,
                ),
                href="https://plotly.com",
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        ],
        color="primary",
        dark=True,
    )
    # layout rendering
    app.layout = html.Div(
        children=[
            navbar,
            html.H1(children="Hello Dash"),
            html.Div(
                children="""
            Dash: A web application framework for your data.
        """
            ),
            fig,
        ],
        style={"font-family":"HP Simplified Light"}
    )

    return app

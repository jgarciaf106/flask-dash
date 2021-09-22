# library imports
import os
import datetime as dt
import json
import pandas as pd
import numpy as np
import pyodbc
from sqlalchemy import create_engine
import tkinter as tk
import xlwings as xw

# set engine db
def set_engine(
    cred_file,
    dsn,
    path="flask-dash/src/credentials/",
):
    credentials = path + "{0}.json".format(cred_file)
    with open(credentials) as get:
        data = json.load(get)
        user_name = data["userName"]
        password = data["password"]
    # db create connection engine
    return create_engine(
        "postgresql://{0}:{1}@localhost/{2}".format(user_name, password, dsn)
    )

# query external file queries
def external_query(
    query_name,
    engine,
    path="flask-dash/src/queries",
):
    query_path = path + "{0}.sql".format(query_name)
    with open(query_path) as get:
        query = get.read()
    return pd.read_sql_query(query, engine)


# query inline queries
def internal_query(query, engine):
    return pd.read_sql_query(query, engine)


# read  files
def file_query(
    file_name,
    folder,
    path="flask-dash/src/data_files/",
):
    file = path + folder + "/" + file_name
    return pd.read_excel(file, index_col=0)


# delete existing file
def file_cleaner(file):
    if os.path.exists(file):
        os.remove(file)


# save formatted file
def file_saver(path, data):

    # workbook / sheet variables
    app = xw.App(visible=False)
    wb = xw.Book()
    ws = wb.sheets[0]

    # excel data header formatting
    ws.range("A1").options(index=False).value = data
    header_format = ws.range("A1").expand("right")
    header_format.color = (0, 150, 214)
    header_format.api.Font.Name = "HP Simplified Light"
    header_format.api.Font.Color = 0xFFFFFF
    header_format.api.Font.Bold = True
    header_format.api.Font.Size = 13

    # excel data content formatting
    data_format = ws.range("A2").expand("table")
    data_format.api.Font.Name = "HP Simplified Light"
    data_format.api.Font.Size = 12

    # save password protect file
    wb.api.SaveAs(path, Password="password")
    app.quit()


def password_tracker(request_date, file_name, path, password):
    app = xw.App(visible=False)
    wb = xw.Book(
        r'C:/Users/garciand/OneDrive - HP Inc/Desktop/Deliverables/Password Tracker/Password_Tracker.xlsx'
    )
    ws = wb.sheets[0]

    next_row = xw.Range('A1').end('up').offset(1).address
    ws.range(next_row).options(index=False).value = [
        request_date,
        file_name,
        path,
        password,
    ]

    wb.save()
    app.quit()


# export file to folder
def export_data(
    odf,
    custom_filename="",
    request_type="",
    path="C:\\Users\\garciand\\OneDrive - HP Inc\\Desktop\\Deliverables",
):

    # assign file name
    if custom_filename == "":
        today = dt.datetime.today()
        fileDate = today.strftime("%Y-%m-%d")
        if request_type == 1:
            folder = "/DEI/"
            filename = "DEI " + fileDate
        elif request_type == 2:
            folder = "/PD/"
            filename = "PD " + fileDate
        else:
            folder = "/MISC/"
            filename = "MISC " + fileDate
    else:
        filename = custom_filename
        if request_type == 1:
            folder = "/DEI/"
        elif request_type == 2:
            folder = "/PD/"
        else:
            folder = "/MISC/"

    # remove existing files before save
    file_cleaner("{0}{1}{2}.xlsx".format(path, folder, filename))

    # save file
    file_saver("{0}{1}{2}.xlsx".format(path, folder, filename), odf)

    # update password tracker
    password_tracker(
        "date", filename, "{0}{1}{2}.xlsx".format(path, folder, filename), "password"
    )

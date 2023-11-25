import os
import pandas as pd


def create_data_frame():
    # meta variables
    files = os.listdir("./files/")
    row_start = 6

    # check if there are no files
    if len(files) == 0:
        return pd.DataFrame()

    # read all csv files and concat them to one DataFrame
    raw_data = pd.DataFrame()
    for file in files:
        file_data = pd.read_csv(
            "./files/" + file, skiprows=row_start, delimiter=";", encoding="UTF-8")
        file_data["File"] = file
        raw_data = pd.concat([raw_data, file_data], ignore_index=True)

    # create blank DataFrame and fill just necessary columns
    data_frame = pd.DataFrame()
    data_frame["file"] = raw_data["File"]
    data_frame["date"] = raw_data["Buchungstag"]
    data_frame["month"] = raw_data["Buchungstag"].str[3:5].astype(int)
    data_frame["year"] = raw_data["Buchungstag"].str[6:10].astype(int)
    data_frame["paytype"] = raw_data["Buchungstext"]
    data_frame["payee"] = raw_data["Auftraggeber / Begünstigter"].astype(
        str)
    data_frame["purpose"] = raw_data["Verwendungszweck"].astype(
        str)
    data_frame["payid"] = (raw_data["Auftraggeber / Begünstigter"] +
                           " [" + raw_data["Verwendungszweck"] + "]").astype(str)
    data_frame["amount"] = raw_data["Betrag (EUR)"].str.replace(
        ".", "").str.replace(",", ".").astype(float)
    data_frame["amount_display"] = raw_data["Betrag (EUR)"]
    data_frame["category"] = None
    data_frame = data_frame[data_frame.paytype != "Abschluss"]

    return (data_frame)

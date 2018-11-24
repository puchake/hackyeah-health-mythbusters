import csv
import pandas as pd
import numpy as np


def split_administrative_id(administrative_id):
    district_part = administrative_id % 100000
    voivodeship_part = administrative_id // 100000
    return voivodeship_part, district_part


def get_voivodeship_part(administrative_id):
    return split_administrative_id(administrative_id)[0]


def get_district_part(administrative_id):
    return split_administrative_id(administrative_id)[1]


def merge_administrative_id(voivodeship_part, district_part):
    return voivodeship_part * 100000 + district_part


def is_district(administrative_id):
    voivodeship_part, district_part = split_administrative_id(administrative_id)
    return district_part != 0


def is_voivodeship(administrative_id):
    voivodeship_part, district_part = split_administrative_id(administrative_id)
    return voivodeship_part != 0


def contains_districts(dataframe):
    return dataframe.where(lambda row: is_district(row.Kod)).count()[0] > 0


def save_voivodeship_id_to_district_id(voivodeship_id_to_district_id):
    with open(
        "processed_data/voivodeship_id_to_district_id.csv", "w", newline=""
    ) as file:
        csv_writer = csv.writer(file, delimiter=";")
        csv_writer.writerow(["KodWojewodztwo", "KodyPowiatow"])
        for key, values in voivodeship_id_to_district_id.items():
            csv_writer.writerow(
                [str(key), ",".join([str(value) for value in values])])


def load_voivodeship_id_to_district_id():
    voivodeship_id_to_district_id = {}
    with open("processed_data/voivodeship_id_to_district_id.csv") as file:
        csv_reader = csv.reader(file, delimiter=";")
        next(csv_reader)
        for row in csv_reader:
            voivodeship_id_to_district_id[int(row[0])] = [
                int(value) for value in row[1].split(",")]
    return voivodeship_id_to_district_id


def load_administrative_id_to_district_name():
    administrative_id_to_district_name = {}
    source_csv = pd.read_csv("processed_data/admin_id_to_district_name.csv")
    for administrative_id, district_name \
            in zip(source_csv.Kod, source_csv.Nazwa):
        administrative_id_to_district_name[administrative_id] = district_name
    return administrative_id_to_district_name


def expand_voivodeship_data_to_district_data(source_csv):
    voivodeship_id_to_district_id = load_voivodeship_id_to_district_id()
    source_csv.Kod = source_csv.Kod.astype(np.int64)
    source_csv.Kod = source_csv.Kod.map(
        lambda value: [
            merge_administrative_id(
                get_voivodeship_part(value), district_id)
            for district_id in voivodeship_id_to_district_id[
                get_voivodeship_part(value)]]
    )
    expanded_source_csv = source_csv.apply(
        lambda row: pd.Series(row["Kod"]), axis=1)
    expanded_source_csv["Date"] = source_csv.Date
    expanded_source_csv["Value"] = source_csv.Value
    expanded_source_csv = expanded_source_csv.set_index(
        ["Date", "Value"]).stack().reset_index()
    expanded_source_csv = expanded_source_csv.drop("level_2", axis=1)
    expanded_source_csv = expanded_source_csv.rename(columns={0: "Kod"})
    expanded_source_csv.Kod = expanded_source_csv.Kod.astype(np.int64)
    expanded_source_csv = expanded_source_csv[["Kod", "Date", "Value"]]
    return expanded_source_csv

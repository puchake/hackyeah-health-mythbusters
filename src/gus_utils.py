import csv
import pandas as pd


def split_administrative_id(administrative_id):
    district_part = administrative_id % 100000
    voivodeship_part = administrative_id // 100000
    return voivodeship_part, district_part


def merge_administrative_id(voivodeship_part, district_part):
    return voivodeship_part * 100000 + district_part


def is_district(administrative_id):
    voivodeship_part, district_part = split_administrative_id(administrative_id)
    return district_part != 0


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

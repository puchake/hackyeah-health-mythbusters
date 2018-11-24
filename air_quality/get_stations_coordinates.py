import argparse
import math

import pandas as pd
import requests


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("api_key", type=str)
    arg_parser.add_argument("stations_csv_path", type=str)
    arg_parser.add_argument("out_csv_path", type=str)
    return arg_parser.parse_args()


API_REQUEST_PATTERN = "https://maps.googleapis.com/maps/api/geocode/json?" \
                      "address={address}&key={key}"


def address_to_url_str(address):
    address = address.replace(" ", "+")
    address = address.replace("/", "%2F")
    return address


def merge_row_to_address(row):
    voivodeship = row["WOJEWÓDZTWO"].lower()
    city = row["MIEJSCOWOSC"]
    street = row["ADRES"]
    address = list(
        filter(lambda x: type(x) != float, [voivodeship, city, street]))
    return " ".join(address)


def main(args):
    stations_csv = pd.read_csv(args.stations_csv_path)
    addresses = stations_csv.apply(merge_row_to_address, axis=1)
    lats = []
    lngs = []
    for address in addresses:
        response = requests.get(
            API_REQUEST_PATTERN.format(
                address=address_to_url_str(address), key=args.api_key))
        location = response.json()["results"][0]["geometry"]["location"]
        lats.append(location["lat"])
        lngs.append(location["lng"])
    stations_csv["lats"] = lats
    stations_csv["lngs"] = lngs
    stations_csv.to_csv(args.out_csv_path)


if __name__ == "__main__":
    args = parse_args()
    main(args)

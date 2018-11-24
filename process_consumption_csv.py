import argparse

import pandas as pd
import numpy as np

from src.gus_utils import contains_districts, is_district, is_voivodeship, \
    expand_voivodeship_data_to_district_data


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("csv_path", type=str)
    arg_parser.add_argument("out_path", type=str)
    return arg_parser.parse_args()


def product_column_name_to_year(product_column_name):
    if ";" not in product_column_name:
        return product_column_name
    return product_column_name.split(";")[1]


def main():
    parsed_args = parse_args()

    source_csv = pd.read_csv(parsed_args.csv_path, sep=";")

    source_csv = source_csv.drop("Nazwa", axis=1)
    source_csv = source_csv.rename(
        product_column_name_to_year, axis="columns")
    source_csv = pd.melt(source_csv, id_vars=["Kod"], var_name="Date",
                         value_name="Value")
    source_csv = source_csv.dropna()

    if contains_districts(source_csv):
        source_csv = (source_csv.where(lambda row: is_district(row.Kod))
                      .dropna(subset=["Kod"]))
        source_csv.Kod = source_csv.Kod.astype(np.int64)
    else:
        source_csv = (source_csv.where(lambda row: is_voivodeship(row.Kod))
                      .dropna(subset=["Kod"]))
        source_csv = expand_voivodeship_data_to_district_data(
            source_csv)

    if source_csv.Value.dtype == object:
        source_csv.Value = source_csv.Value.map(
            lambda row: float(str(row).replace(",", ".")))
    source_csv.to_csv(parsed_args.out_path, index=False)


if __name__ == "__main__":
    main()

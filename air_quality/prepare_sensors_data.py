import os
import argparse

import pandas as pd


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("in_dir", type=str)
    arg_parser.add_argument("out_dir", type=str)
    return arg_parser.parse_args()


def main(args):
    for filename in os.listdir(args.in_dir):
        print(filename)
        year_data = pd.read_excel(os.path.join(args.in_dir, filename))
        year = int(filename.split("_")[0])
        if year >= 2016:
            year_data = year_data.drop(["Nr"], axis=1)
            year_data.columns = year_data.iloc[0]
            pollution_name = year_data.iloc[1, 0]
            year_data = year_data.drop([0, 1, 2, 3, 4])
            year_data = year_data.applymap(
                lambda x:
                    float(str(x).replace(",", ".")) if "," in str(x) else x)
        else:
            year_data = year_data.drop(["Kod stacji"], axis=1)
            pollution_name = year_data.iloc[0, 0]
            year_data = year_data.drop([0, 1])
        year_data = year_data.mean(skipna=True)
        year_data.to_csv(
            os.path.join(
                args.out_dir, "{}_{}.csv".format(year, pollution_name)))


if __name__ == "__main__":
    args = parse_args()
    main(args)

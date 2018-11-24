import pandas as pd
import numpy as np

from src.gus_utils import is_district, split_administrative_id, \
    save_voivodeship_id_to_district_id


def main():
    source_csv = pd.read_csv(
        "raw_data/choroby_ukladu_krazenia_ogolem_gus.csv", sep=";")

    administrative_ids = source_csv.Kod.map(split_administrative_id)
    voivodeship_id_to_district_id = {}
    for voivodeship_id, district_id in administrative_ids:
        if voivodeship_id not in voivodeship_id_to_district_id \
                and district_id != 0:
            voivodeship_id_to_district_id[voivodeship_id] = []
        if district_id != 0:
            voivodeship_id_to_district_id[voivodeship_id].append(district_id)
    save_voivodeship_id_to_district_id(voivodeship_id_to_district_id)

    source_csv = (source_csv.where(lambda row: is_district(row.Kod))
                  .dropna(subset=["Kod"]))
    source_csv.Kod = source_csv.Kod.astype(np.int64)
    administrative_id_to_district_name = source_csv[["Kod", "Nazwa"]]
    administrative_id_to_district_name.to_csv(
        "processed_data/admin_id_to_district_name.csv", index=False)


if __name__ == "__main__":
    main()

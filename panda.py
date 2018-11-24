import pandas as pd

zach = 'LUDN_2286_CTAB_20181124162831.csv'
df = pd.read_csv(zach, sep=";")
print(df.columns)
exit()
df = df.loc[df['Nazwa'].str.contains('Powiat')]

def print_pd(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

def for_year(df, year):
    ill = 'choroby układu krążenia ogółem;{};[-]'.format(year)
    df['ill'] = df[ill]
    df['Nazwa'] = df['Nazwa'] + str(year)
    return df[['Nazwa', 'ill']]


def all_years(df, start=2003, stop=2017):
    dfs = []
    for year in range(start, stop + 1):
        dfs.append(for_year(df, year))
    return pd.concat(dfs)

df = all_years(df)
print(df)
print(df.columns)


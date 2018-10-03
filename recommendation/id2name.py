import pandas as pd

original_data = pd.read_csv('./foundation.csv')

def id_2_name(original_data):
    id_to_name = original_data[["popId", "name"]].drop_duplicates()
    id_to_name = id_to_name.reset_index(drop=True)
    id_to_name = id_to_name.drop(columns="popId", axis=1)
    return id_to_name

dada = id_2_name(original_data)
print(dada)
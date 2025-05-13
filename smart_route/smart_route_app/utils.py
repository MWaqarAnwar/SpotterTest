import pandas as pd

class SmartRouteUtils:
    def load_csv_data(csv_file_object):
        df = pd.read_csv(csv_file_object)
        return df

    def convert_row_to_full_address(row):
        full_address = f"{row['Address']}, {row['City']}, {row['State']}, USA"
        return full_address

    def convert_df_to_list_of_full_addresses(df):
        addresses_list = []
        for index, row in df.iterrows():
           addresses_list.append(SmartRouteUtils.convert_row_to_full_address(row))
        return addresses_list
    
from pandas import DataFrame
from lyricsgenius import Genius
from pandas import read_hdf

def start_genius_api(api_key:str):
    """load the genius api object using client key"""
    api_obj = Genius(api_key, sleep_time=0.2, timeout=20) # note sleep time between api calls could be further reduced only
    # by changing package directly to change the min_sleep_time param in API Class
    # check it has worked?
    return api_obj

def save_df(df,
            df_path:str,
            hdf_key:str):
    df.to_hdf(df_path, key=hdf_key)

def load_df(df_path:str,
            hdf_key:str):
    df = read_hdf(df_path, hdf_key)
    return df

def save_text_file(text, save_path:str):
    with open(save_path, 'a') as f:
        f.write(text)
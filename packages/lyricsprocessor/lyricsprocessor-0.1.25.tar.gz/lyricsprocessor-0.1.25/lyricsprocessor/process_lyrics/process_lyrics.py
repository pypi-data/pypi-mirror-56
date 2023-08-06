from lyricsprocessor.utils import start_genius_api, save_df, load_df

import logging
from typing import Dict, Tuple
from pandas import DataFrame, to_datetime, read_hdf
from argparse import ArgumentParser
from re import split, findall
from collections import OrderedDict

########################################################################################################################

def df_lyrics_to_dict(lyrics_series):
    return lyrics_series.apply(lyrics_to_dict)

def lyrics_to_dict(lyrics:str):
    verses = get_verses(lyrics)
    verses = clean_verses(verses)
    verse_keys = get_verse_keys(lyrics)
    lyrics_dict = OrderedDict(zip(verse_keys, verses))
    return lyrics_dict

def get_verses(lyrics:str):
    verses = split("\[.+\]", lyrics)[1:]
    if not len(verses):
        verses = [lyrics, ]
    return verses

def clean_verses(verses:list):
    cleaned_verses = [clean_verse(verse) for verse in verses]
    return cleaned_verses

def clean_verse(verse:str):
    cleaned_verse = verse.split('\n')
    cleaned_verse = [line for line in cleaned_verse if line] # get rid of empty strings
    return cleaned_verse

def get_verse_keys(lyrics:str):
    verse_keys = findall("\[.+\]", lyrics)
    if not len(verse_keys):
        verse_keys = ['verse_1',]
    return verse_keys
########################################################################################################################

def clean_df(df:DataFrame,
             dropna:bool=True,
             id_col:str='primary_artist',
             datetime_col:str='release_date',
             check_lyrics_state:bool=True):
    artist_id = df['artist_id']
    df[datetime_col] = to_datetime(df[datetime_col]) #fail if empty?
    df[id_col] = df[id_col].apply(lambda x: x['id'])
    df = df[df[id_col] == artist_id]
    df.drop('artist_id', axis=1, inplace=True)
    if check_lyrics_state: # sometimes the fields will be Nan
        if len(df[df['lyrics_state'] == 'complete']):
            df = df[df['lyrics_state'] == 'complete']
        else:
            logging.Warning('Warning: Checking lyrics state has resulted in no data rows, possible that Nan is value for all,'
                  ' change check_lyrics_state to False to avoid this step') 
    df.dropna(inplace=dropna, subset=['lyrics', 'title'])  # if false is passed then it will just not be saved
    return df

########################################################################################################################
# fix this
def get_featured_artists(featured_artists):
    featured_artists_names = featured_artists.apply(lambda x: [x_['name'] for x_ in x])# this might fail if its not a list of dicts
    return featured_artists_names

def get_artist_name(api_obj, artist_id:int):
    art_obj = get_artist_obj(api_obj, artist_id)
    artist_name, alternate_names = art_obj['artist']['name'], art_obj['artist']['alternate_names']
    alternate_names.append(artist_name.lower().strip('the'))
    return artist_name, alternate_names

def get_artist_obj(api_obj, artist_id:int):
    art_obj = api_obj.get_artist(artist_id)
    return art_obj

########################################################################################################################

# improvements:
# better way of matching artists name
# better matching of standard names (.e.g intro, verse 1 etc.) - then can keep any verses with these labels only, as well as those with artists name
# then would always have verses, and could get rid of any with other artists in them.
# would still have leftover some poorly labelled ones but would be more robust
# for now will leave it alone as it works well enough
# this is a bit sloppy, have the column labels passed in so no assumptions, try to clean up without slowing down

# also try maybe seeing if artist is in any of the verses, if they are, i.e. length of processed lyrics dict isn't zero,
def df_drop_verses(lyrics_series, artist_name:str, alternate_names:list):
    lyrics_series_dropped = lyrics_series.apply(lambda x: drop_verses(x.lyrics_dict, x.featured_artists, artist_name, alternate_names), axis=1)
    return lyrics_series_dropped

def drop_verses(lyrics_dict, featured_artists, artist_name:str, alternate_names:list):
    names_list = alternate_names + [artist_name,]
    lyrics_dropped = {verse_key: verse for verse_key, verse in lyrics_dict.items()
                   if artist_verse_check(verse_key, names_list)}
    if not lyrics_dropped: # second bit is kind of redundant
        # then we have no verses, but the primary artist is the one we are after so instead,
        # remove verses with other people on them, using only their first name
        if not featured_artists:
            # then the featured artists aren't on there so just return everything
            return lyrics_dict
        else:
            lyrics_dropped = {verse_key: verse for verse_key, verse in lyrics_dict.items()
                          if not artist_verse_check(verse_key, featured_artists)}

    return lyrics_dropped

def artist_verse_check(verse_key:str, names_list:list):
    names_test = any([name.lower().replace('.', '') in verse_key.lower().replace('.', '') for name in names_list])
    return names_test

########################################################################################################################

def main(api_key:str,
         df,
         hdf_key:str='',
         dropna:bool=True,
         check_lyrics_state:bool=True,
         save_path:str=''):

    api_obj = start_genius_api(api_key)

    df = clean_df(df,
                  dropna=dropna,
                  id_col='primary_artist',
                  datetime_col='release_date',
                  check_lyrics_state=check_lyrics_state)

    df['lyrics_dict'] = df_lyrics_to_dict(df['lyrics'])

    artist_id = df['primary_artist'][0]
    artist_name, alternate_names = get_artist_name(api_obj, artist_id)
    df['featured_artists'] = get_featured_artists(df['featured_artists'])

    # note this still fails sometimes if featured artists weren't labelled properly, nothing to do about that though?
    df['lyrics_dict'] = df_drop_verses(df[['lyrics_dict', 'featured_artists']],
                                                         artist_name=artist_name, alternate_names=alternate_names)

    if save_path:
        if hdf_key:
            save_df(df, save_path, hdf_key)
        else:
            logging.Warning('No HDF key supplied, but save path supplied, saving if hdf key="default"')
            save_df(df, save_path, 'default')
    return df

########################################################################################################################

if __name__ == '__main__':
    parser = ArgumentParser(description='Process inputs for downloading lyrics.')
    parser.add_argument('--api_key', type=str,
                        help='api key for genius api')
    parser.add_argument('--df_path', type=str,
                        help='path for where to load hdf file from')
    parser.add_argument('--hdf_key', type=str,
                        help='hdf key of file')
    parser.add_argument('--save_path', type=str, default='',
                        help='path for where to save hdf file, leave blank if not wanting to save')
    parser.add_argument('--dropna', default=True, type=bool,
                        help='should dropna be performed on the df?')
    parser.add_argument('--check_lyrics_state', default=True, type=bool,
                        help='should the lyrics state be checked?')
    args = parser.parse_args()

    logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')

    df = load_df(args.df_path, args.hdf_key)
    main(args.api_key, df, args.hdf_key, args.dropna, args.check_lyrics_state, args.save_path)
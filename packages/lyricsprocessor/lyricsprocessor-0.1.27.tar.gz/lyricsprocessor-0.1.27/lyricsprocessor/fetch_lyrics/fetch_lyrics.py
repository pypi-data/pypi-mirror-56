from lyricsprocessor.utils import start_genius_api, save_df

from pandas import DataFrame
from lyricsgenius import Genius
from json import loads as jsonloads
from argparse import ArgumentParser
from typing import Dict, Tuple
from collections import OrderedDict

#TODO
# add tests
# also check status of api check, and check where to fail if that isn't valid
# remove client key before publishing

def find_artist(api_obj,
                art_search_term:str):
    """find the artist object from genius"""
    art_obj = api_obj.search_artist(art_search_term)
    return art_obj

def get_artist_dict(art_obj):
    """Get the artist dictionary"""
    art_json = art_obj.to_json()
    art_dict = jsonloads(art_json)
    return art_dict

def get_lyrics_dict(art_dict:Dict,
                    lyrics_field='songs'):
    return art_dict[lyrics_field]

def df_from_lyrics_dict(lyrics_dict:Dict,
                        keep_fields:Tuple=('id','title','lyrics','lyrics_state','primary_artist','release_date', 'featured_artists')):
    df = DataFrame(lyrics_dict)
    df = df[list(keep_fields)]
    return df

def get_artist_id(art_dict:Dict):
    return art_dict['id']

def main(api_key:str,
         artist_search_term:str,
         save_path:str=''):
    api_obj = start_genius_api(api_key)

    art_obj = find_artist(api_obj, artist_search_term)
    art_dict = get_artist_dict(art_obj)
    lyrics_dict = get_lyrics_dict(art_dict,lyrics_field='songs')
    df = df_from_lyrics_dict(lyrics_dict,
                             keep_fields=['id','title','lyrics','lyrics_state','primary_artist','release_date', 'featured_artists'])

    df['artist_id'] = get_artist_id(art_dict)

    if save_path:
        hdf_key = artist_search_term.replace(' ', '_')
        save_df(df, save_path, hdf_key)
    return df

if __name__ == '__main__':
    parser = ArgumentParser(description='Process inputs for downloading lyrics.')
    parser.add_argument('--api_key', type=str,
                        help='api key for genius api')
    parser.add_argument('--artist_search_term', type=str,
                        help='search term for genius to find artist')
    parser.add_argument('--save_path', default='', type=str,
                        help='path for where to save hdf file')

    args = parser.parse_args()
    main(args.api_key, args.artist_search_term, args.save_path)

## fix the lyrics parser, some empty strings, alsosome verses that shouldn't be there!
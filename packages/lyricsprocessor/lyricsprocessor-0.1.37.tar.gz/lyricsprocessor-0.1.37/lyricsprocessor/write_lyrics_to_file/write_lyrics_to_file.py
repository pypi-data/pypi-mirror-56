# load lyrics df
from lyricsprocessor.utils import start_genius_api, load_df, save_text_file

import os
from pathlib import Path
from typing import Dict, Tuple
from argparse import ArgumentParser
from collections import OrderedDict
import logging

########################################################################################################################

def process_lyrics(lyrics_dict):
    song_as_str = ''
    for verse in lyrics_dict.values():
        joined_verse = '\n'.join(verse)
        song_as_str += joined_verse
        song_as_str += '\n\n\n'
    return song_as_str

########################################################################################################################

def main(df, save_path:str=''):
    logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')
    if not os.path.exists(os.path.dirname(save_path)):
        try:
            os.mkdir(os.path.dirname(save_path))
        except FileNotFoundError:
            logging.Warning("Didn't make a new directory as none was specified.")
        Path(save_path).touch()
    for index, song in df.iterrows(): # maybe instead of writing each one we should write to one file with a good seperator?
        lyrics_dict = song['lyrics_dict']
        processed_lyrics_str = f"\n\n= = {song['title']} = =\n\n"
        processed_lyrics_str += process_lyrics(lyrics_dict)
        save_text_file(processed_lyrics_str, save_path)

########################################################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process inputs for downloading lyrics.')
    parser.add_argument('--df_path', type=str,
                        help='path for where to load hdf file from')
    parser.add_argument('--hdf_key', type=str,
                        help='hdf key of file')
    parser.add_argument('--save_path', type=str, default='',
                        help='path for where to save hdf file, leave blank if not wanting to save')

    args = parser.parse_args()

    df = load_df(args.df_path, args.hdf_key)
    main(df, args.save_path)
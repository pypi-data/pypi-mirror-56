from lyricsprocessor import fetch_lyrics, process_lyrics, write_lyrics_to_file
from argparse import ArgumentParser
import logging

# note argparse is inside as main() is called when this is made to a script, maybe should change all the others too?
def main():
    logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')
    print('logging setup')

    parser = ArgumentParser(description='Process inputs for downloading and processing lyrics.')
    parser.add_argument('--api_key', type=str,
                        help='api key for genius api')
    parser.add_argument('--artist_search_term', type=str,
                        help='search term for genius to find artist')
    parser.add_argument('--dropna', default=True, type=bool,
                        help='should dropna be performed on the df?')
    parser.add_argument('--check_lyrics_state', default=True, type=bool,
                        help='should the lyrics state be checked?')
    parser.add_argument('--save_raw_df_path', default='', type=str,
                        help='where to save the raw df file with everything')
    parser.add_argument('--save_processed_df_path', default='', type=str,
                        help='where to save the text file with everything')
    parser.add_argument('--save_processed_hdf_key', default='default', type=str,
                        help='where to save the text file with everything')
    parser.add_argument('--save_txt_path', default='./lyrics.txt', type=str,
                        help='where to save the text file with everything')
    args = parser.parse_args()

    api_key=args.api_key
    artist_search_term=args.artist_search_term
    dropna=args.dropna
    check_lyrics_state=args.check_lyrics_state
    save_raw_df_path=args.save_raw_df_path
    save_processed_df_path=args.save_processed_df_path
    save_processed_hdf_key=args.save_processed_hdf_key
    save_txt_path=args.save_txt_path

    print('fetching lyrics')
    df = fetch_lyrics.main(api_key=api_key, artist_search_term=artist_search_term, save_path=save_raw_df_path)
    print('got lyrics', df.head())
    df = process_lyrics.main(api_key=api_key, df=df, dropna=dropna, check_lyrics_state=check_lyrics_state, save_path=save_processed_df_path, hdf_key=save_processed_hdf_key)
    print('processed lyrics', df.head())
    write_lyrics_to_file.main(df=df, save_path=save_txt_path)
    print('wrote lyrics to file')

if __name__ == "__main__":
    main()
from lyricsprocessor import fetch_lyrics, process_lyrics, wirte_lyrics_to_file

def main(api_key, artist_search_term, dropna, check_lyrics_state, save_raw_df_path, save_processed_df_path, save_processed_hdf_key, save_txt_path):
	df = fetch_lyrics.main(api_key, artist_search_term, save_path=save_raw_df_path)
	df = process_lyrics.main(api_key, df, dropna, check_lyrics_state, save_path=save_processed_df_path, hdf_key=save_processed_hdf_key)
	wirte_lyrics_to_file.main(df, save_path=save_txt_path)


# write this so can fetch, process then write to text files in one shot
if __name__ == '__main__':
	logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')
	parser = ArgumentParser(description='Process inputs for downloading and processing lyrics.')
	parser.add_argument('--api_key', type=str,
						help='api key for genius api')
	parser.add_argument('--artist_search_term', type=str,
						help='search term for genius to find artist')
	parser.add_argument('--dropna', default=True, type=bool,
						help='should dropna be performed on the df?')
	parser.add_argument('--check_lyrics_state', default=True, type=bool,
						help='should the lyrics state be checked?')
	parser.add_argument('--save_raw_df_path', default='', type=bool,
						help='where to save the raw df file with everything')
	parser.add_argument('--save_processed_df_path', default='', type=bool,
						help='where to save the text file with everything')
	parser.add_argument('--save_processed_hdf_key', default='', type=bool,
						help='where to save the text file with everything')
	parser.add_argument('--save_txt_path', default='./lyrics.txt', type=bool,
						help='where to save the text file with everything')
	args = parser.parse_args()
	main(args.api_key, args.artist_search_term, args.dropna, args.check_lyrics_state, args.save_raw_df_path, args.save_processed_df_path, args.save_processed_hdf_key, args.save_txt_path)
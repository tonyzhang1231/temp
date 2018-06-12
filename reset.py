import os,sys
from utils import *


LOG_FILE = 'hyyb_log.log'
HYYB_DIR = 'hyyb'
HYYB_PDF_DIR = 'hyyb_pdf'
EXTRACTED_HYYB_IDS_FILE = 'hyyb_extracted_ids.txt'

"""
this script will remove all the reports in hyyb folder, all the log files, all the pdfs
be very careful when using reset()
"""

def reset():
	# reset log file and extracted ids file
	remove_file_if_exists(LOG_FILE)
	create_file_if_not_exists(LOG_FILE)

	remove_file_if_exists(EXTRACTED_HYYB_IDS_FILE)
	create_file_if_not_exists(EXTRACTED_HYYB_IDS_FILE)


	# reset folders
	remove_dir_if_exists(HYYB_DIR, force=True)
	create_dir_if_not_exists(HYYB_DIR)

	remove_dir_if_exists(HYYB_PDF_DIR, force=True)
	create_dir_if_not_exists(HYYB_PDF_DIR)

	# above functions have been tested

if __name__ == '__main__':
	reset()












# python reset.py

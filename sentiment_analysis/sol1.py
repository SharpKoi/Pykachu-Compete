import json
from langdetect import detect
import pandas as pd
import re
from spellchecker import SpellChecker


def trim_letters(s):
    # look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"([a-zA-z_])\1{2,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


def detect_language(df):
	langs = []
	for index, row in df.iterrows():
		try:
			if detect(row['review']) != 'en':
				x.append('id')
			else:
				x.append('en')
		except Exception:
			langs.append('en')
	df['language']= langs
	return df


def spell_checker(word_list):
	spell = SpellChecker()
	misspelled = spell.unknown(word_list)
	# misspelled = spell.unknown(['Let','rexomend', 'us', 'wlak','on','the','gooood','smille'])
	for word in misspelled:
		# Get the one `most likely` answer
		word_list[word_list.index(word)] = spell.correction(word)
	return word_list


# stopwordList
with open('data/lib/en.json') as f:
	stopword_en = json.load(f)

with open('data/lib/id.json') as f:
	stopword_id = json.load(f)

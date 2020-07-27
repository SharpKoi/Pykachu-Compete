import json
from langdetect import detect
import pandas as pd
import re
from spellchecker import SpellChecker

def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

def detect_language(df):
	x = []
	for index, row in df.iterrows():
		try:
			x.append = detect(row['review'])
		except Exception:
			pass
	df['language']= x
	return df

def spell_checker(word_list):
	spell = SpellChecker()
	misspelled = spell.unknown(word_list)
	#misspelled = spell.unknown(['Let','rexomend', 'us', 'wlak','on','the','gooood','smille'])
	for word in misspelled:
	    # Get the one `most likely` answer
	    word_list[word_list.index(word)] = spell.correction(word)
	return word_list

# stopwordList	
with open('en.json') as f:
    stopword_en = json.load(f)
with open('id.json') as f:
    stopword_id = json.load(f)
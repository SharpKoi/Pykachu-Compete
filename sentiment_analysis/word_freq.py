import nltk
# nltk.download('stopwords') 沒下載過的話把註解拿掉
# nltk.download('punkt') 沒下載過的話把註解拿掉

import string
from nltk.corpus import stopwords

import re
import numpy as np
import pandas as pd

df = pd.read_csv('data/cleaned_data/data_sol241.csv')

# 先把符號過濾掉
df['review'] = df['review'].str.replace(r'[^\w\s\r\n]', '')

# 把所有單詞丟進words
words = []
stops = stopwords.words('english') + list(string.punctuation)
wordslist = df['review'].apply(nltk.word_tokenize)
for i in range(len(df)):
    words.extend([word for word in wordslist[i] if word not in stops])

# 統計每個單詞出現的量(詞頻)
wordfreqs = nltk.FreqDist(words)


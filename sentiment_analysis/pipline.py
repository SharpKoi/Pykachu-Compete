import re
import numpy as np
import pandas as pd

import emoji

import nltk
# nltk.download('stopwords') 沒下載過的話把註解拿掉
# nltk.download('punkt') 沒下載過的話把註解拿掉

import string
from nltk.corpus import stopwords

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical

from tensorflow.keras.models import Model

from sklearn.model_selection import train_test_split

import plotly.graph_objects as go
from plotly.subplots import make_subplots


# feature engineering
def widen_emoji(text):
    for c in text:
        if c in emoji.UNICODE_EMOJI.keys():
            text = ' '.join(text.replace(c, (' ' + c + ' ')).split())
    return text


def emoji_transform(text):
    text = widen_emoji(text)
    return emojis.demoji(text)


def check_contractions(df, col='review'):
    abbr_pat = re.compile(r'[\w]+\'[\w]+')
    return df[df[col].str.contains(abbr_pat)]


def contractions_decompose(df, col='review'):
    _df = df.copy()
    mapping = {'\'s': ' ', '\'m': ' am', '\'re': ' are', '\'ll': ' will', '\'d': ' would', '\'t': ' not',
               '\'ve': ' have'}

    for abbr in mapping.keys():
        _df[col] = _df[col].str.replace(abbr, mapping[abbr])

    _df[col] = _df[col].str.replace('\'', '').str.replace('oclock', 'o\'clock')
    return _df


def get_words_list(df):
    words_list = df['review'].apply(nltk.word_tokenize)
    return words_list


def get_words_count(words_list):
    words = []
    stops = stopwords.words('english') + list(string.punctuation)
    for i in range(len(words_list)):
        words.extend([word for word in words_list[i] if word not in stops])

    wordfreqs = nltk.FreqDist(words)
    return wordfreqs


def get_meanless_words_dict(wordfreqs, tolerance=3, maxlen=10):
    removables = {}
    wordfreq_arr = np.array(list(wordfreqs.items()))
    for wf in wordfreq_arr:
        if (int(wf[1]) <= tolerance) and (len(wf[0]) >= maxlen):
            removables[wf[0]] = wf[1]

    return removables


def clean_meanless_words(df, tolerance=3, maxlen=10):
    words_list = get_words_list(df)
    meanless_words_dict = get_meanless_words_dict(get_words_count(words_list))
    meanless_words = list(meanless_words_dict.keys())

    cleaned_texts = []
    for wl in words_list:
        cleaned_words = []
        for w in wl:
            if w not in meanless_words:
                cleaned_words.append(w)
        cleaned_texts.append(' '.join(cleaned_words))

    df['review'] = cleaned_texts


# model
def save_model_history(model, file_path, mode='csv'):
    hist_df = pd.DataFrame(model.history)
    with open(file_path, mode='w') as f:
        if mode == 'csv':
            hist_df.to_csv(f)
        elif mode == 'json':
            hist_df.to_json(f)


def plot_model_history(model: Model):
    history = model.history

    h_accuracy = history.history['accuracy']
    h_val_accuracy = history.history['val_accuracy']
    h_loss = history.history['loss']
    h_val_loss = history.history['val_loss']

    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(go.Scatter(y=h_accuracy, mode='lines+markers', name='accuracy', line=dict(color='skyblue')),
                  row=1, col=1)
    fig.add_trace(
        go.Scatter(y=h_val_accuracy, mode='lines+markers', name='validation accuracy', line=dict(color='dodgerblue')),
        row=1, col=1)

    fig.add_trace(go.Scatter(y=h_loss, mode='lines+markers', name='loss', line=dict(color='lightsalmon')),
                  row=1, col=2)
    fig.add_trace(go.Scatter(y=h_val_loss, mode='lines+markers', name='validation loss', line=dict(color='tomato')),
                  row=1, col=2)

    fig.update_xaxes(title_text='Epochs', row=1, col=1)
    fig.update_xaxes(title_text='Epochs', row=1, col=2)
    fig.update_yaxes(title_text='Accuracy', row=1, col=1)
    fig.update_yaxes(title_text='Loss', row=1, col=2)

    fig.update_layout(title='Model Fitting History', height=480, width=1080)


class FittingData:
    # variables
    #   fitting_labels
    #   fitting_sequences
    #   word_id_dict

    def __init__(self, df: pd.DataFrame, training_col, label_col, max_words, seq_len, fitting_size=1.0):
        fitting_texts = df[training_col].tolist()
        self.fitting_labels = df[label_col].tolist()

        if fitting_size is not 1.0:
            _fitting_size = int(len(df) * fitting_size)
            random_index = np.random.choice([i for i in range(len(df))], _fitting_size, replace=False)

            fitting_texts = np.array(fitting_texts)[random_index].tolist()
            self.fitting_labels = np.array(self.fitting_labels)[random_index].tolist()

        tokenizer = Tokenizer(num_words=max_words)
        tokenizer.fit_on_texts(fitting_texts)
        self.fitting_sequences = tokenizer.texts_to_sequences(fitting_texts)
        self.fitting_sequences = pad_sequences(self.fitting_sequences, padding='post', maxlen=seq_len)
        self.fitting_labels = to_categorical(np.asarray(self.fitting_labels))

        self.word_id_dict = tokenizer.word_index

    def get_fitting_data(self, test_ratio=0.2):
        return train_test_split(self.fitting_sequences, self.fitting_labels, test_size=test_ratio)

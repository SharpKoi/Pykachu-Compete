import numpy as np
import pandas as pd

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical

from tensorflow.keras.models import Model

from sklearn.model_selection import train_test_split

import plotly.graph_objects as go
from plotly.subplots import make_subplots


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

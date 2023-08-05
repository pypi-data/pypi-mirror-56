import json
import logging
from typing import Tuple, List

import tensorflow as tf
from headliner.model.summarizer_transformer import SummarizerTransformer

from headliner.model import SummarizerAttention
from sklearn.model_selection import train_test_split
from tensorflow_datasets.core.features.text import SubwordTextEncoder
from transformers import BertTokenizer

from headliner.model.summarizer_bert import SummarizerBert
from headliner.preprocessing import Preprocessor, Vectorizer
from headliner.trainer import Trainer


def read_data_json(file_path: str,
                   max_sequence_length: int) -> List[Tuple[str, str]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        data_out = json.load(f)
        return [d for d in zip(data_out['desc'], data_out['heads']) if len(d[0].split(' ')) <= max_sequence_length]


def read_data(file_path: str) -> List[Tuple[str, str]]:
    data_out = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for l in f.readlines():
            x, y = l.strip().split('\t')
            data_out.append((x, y))
        return data_out


if __name__ == '__main__':
    from headliner.trainer import Trainer
    from headliner.model.summarizer_transformer import SummarizerTransformer

    data = [
        ('You are the stars, earth and sky for me!', 'I love you I love you I love you.'),
        ('You are the stars, earth and sky for me!', 'I love you.')
    ]

    summarizer = SummarizerTransformer(embedding_size=64, max_prediction_len=20)
    trainer = Trainer(batch_size=1, steps_per_epoch=100, model_save_path='/tmp/summarizer')
    trainer.train(summarizer, data, num_epochs=1)
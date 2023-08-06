# encoding: utf-8

import logging
import os
from typing import Tuple, List

import pandas as pd
from tensorflow.python.keras.utils import get_file

from band import macros as k
from band import utils

CORPUS_PATH = os.path.join(k.DATA_PATH, 'corpus')


class DataReader(object):

    @staticmethod
    def read_conll_format_file(file_path: str,
                               text_index: int = 0,
                               label_index: int = 1) -> Tuple[List[List[str]], List[List[str]]]:
        """
        Read conll format data_file
        Args:
            file_path: path of target file
            text_index: index of text data, default 0
            label_index: index of label data, default 1

        Returns:

        """
        x_data, y_data = [], []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            x, y = [], []
            for line in lines:
                rows = line.split(' ')
                if len(rows) == 1:
                    x_data.append(x)
                    y_data.append(y)
                    x = []
                    y = []
                else:
                    x.append(rows[text_index])
                    y.append(rows[label_index])
        return x_data, y_data


class ChineseDailyNerCorpus(object):
    """
    Chinese Daily New New Corpus
    https://github.com/zjy-ucas/ChineseNER/
    """
    __corpus_name__ = 'china-people-daily-ner-corpus'
    __zip_file__name = 'http://s3.bmio.net/kashgari/china-people-daily-ner-corpus.tar.gz'

    def __init__(self):
        self.train_x, self.train_y = self.load_data('train')
        self.valid_x, self.valid_y = self.load_data('valid')
        self.test_x, self.test_y = self.load_data('test')

    @classmethod
    def load_data(cls,
                  subset_name: str = 'train',
                  shuffle: bool = True) -> Tuple[List[List[str]], List[List[str]]]:
        """
        Load dataset as sequence labeling format, char level tokenized

        Sample::

            train_x, train_y = ChineseDailyNerCorpus.load_data('train')
            test_x, test_y = ChineseDailyNerCorpus.load_data('test')

        Args:
            subset_name: {train, test, valid}
            shuffle: should shuffle or not, default True.

        Returns:
            dataset_features and dataset labels
        """
        corpus_path = get_file(cls.__corpus_name__,
                               cls.__zip_file__name,
                               cache_dir=k.DATA_PATH,
                               untar=True)

        if subset_name == 'train':
            file_path = os.path.join(corpus_path, 'example.train')
        elif subset_name == 'test':
            file_path = os.path.join(corpus_path, 'example.test')
        else:
            file_path = os.path.join(corpus_path, 'example.dev')

        x_data, y_data = DataReader.read_conll_format_file(file_path)
        if shuffle:
            x_data, y_data = utils.unison_shuffled_copies(x_data, y_data)
        logging.debug(f"loaded {len(x_data)} samples from {file_path}. Sample:\n"
                      f"x[0]: {x_data[0]}\n"
                      f"y[0]: {y_data[0]}")
        return x_data, y_data


class CONLL2003ENCorpus(object):
    __corpus_name__ = 'conll2003_en'
    __zip_file__name = 'http://s3.bmio.net/kashgari/conll2003_en.tar.gz'

    def __init__(self):
        self.train_x, self.train_y = self.load_data('train')
        self.valid_x, self.valid_y = self.load_data('valid')
        self.test_x, self.test_y = self.load_data('test')

    @classmethod
    def load_data(cls,
                  subset_name: str = 'train',
                  task_name: str = 'ner',
                  shuffle: bool = True) -> Tuple[List[List[str]], List[List[str]]]:
        """

        """
        corpus_path = get_file(cls.__corpus_name__,
                               cls.__zip_file__name,
                               cache_dir=k.DATA_PATH,
                               untar=True)

        if subset_name not in {'train', 'test', 'valid'}:
            raise ValueError()

        file_path = os.path.join(corpus_path, f'{subset_name}.txt')

        if task_name not in {'pos', 'chunking', 'ner'}:
            raise ValueError()

        data_index = ['pos', 'chunking', 'ner'].index(task_name) + 1

        x_data, y_data = DataReader.read_conll_format_file(file_path, label_index=data_index)
        if shuffle:
            x_data, y_data = utils.unison_shuffled_copies(x_data, y_data)
        logging.debug(f"loaded {len(x_data)} samples from {file_path}. Sample:\n"
                      f"x[0]: {x_data[0]}\n"
                      f"y[0]: {y_data[0]}")
        return x_data, y_data


class SMP2018ECDTCorpus(object):
    """
    https://worksheets.codalab.org/worksheets/0x27203f932f8341b79841d50ce0fd684f/

    This dataset is released by the Evaluation of Chinese Human-Computer Dialogue Technology (SMP2018-ECDT)
    task 1 and is provided by the iFLYTEK Corporation, which is a Chinese human-computer dialogue dataset.
    """

    __corpus_name__ = 'SMP2018ECDTCorpus'
    __zip_file__name = 'http://s3.bmio.net/kashgari/SMP2018ECDTCorpus.tar.gz'

    def __init__(self):
        self.train_x, self.train_y = self.load_data('train')
        self.valid_x, self.valid_y = self.load_data('valid')
        self.test_x, self.test_y = self.load_data('test')

    @classmethod
    def load_data(cls,
                  subset_name: str = 'train',
                  shuffle: bool = True,
                  cutter: str = 'char') -> Tuple[List[List[str]], List[str]]:
        """
        Load dataset as sequence classification format, char level tokenized
        Samples::
            train_x, train_y = SMP2018ECDTCorpus.load_data('train')
            test_x, test_y = SMP2018ECDTCorpus.load_data('test')

        Args:
            subset_name: {train, test, valid}
            shuffle: should shuffle or not, default True.
            cutter: sentence cutter, {char, jieba}

        Returns:
            dataset_features and dataset labels
        """

        corpus_path = get_file(cls.__corpus_name__,
                               cls.__zip_file__name,
                               cache_dir=k.DATA_PATH,
                               untar=True)

        if cutter not in ['char', 'jieba', 'none']:
            raise ValueError('cutter error, please use one onf the {char, jieba}')

        df_path = os.path.join(corpus_path, f'{subset_name}.csv')
        df = pd.read_csv(df_path)
        if cutter == 'jieba':
            try:
                import jieba
            except ModuleNotFoundError:
                raise ModuleNotFoundError(
                    "please install jieba, `$ pip install jieba`")
            x_data = [list(jieba.cut(item)) for item in df['query'].tolist()]
        elif 'char':
            x_data = [list(item) for item in df['query'].tolist()]
        y_data = df['label'].tolist()

        if shuffle:
            x_data, y_data = utils.unison_shuffled_copies(x_data, y_data)
        logging.debug(f"loaded {len(x_data)} samples from {df_path}. Sample:\n"
                      f"x[0]: {x_data[0]}\n"
                      f"y[0]: {y_data[0]}")
        return x_data, y_data

if __name__ == "__main__":
    a, b = CONLL2003ENCorpus.load_data()
    print(a[:2])
    print(b[:2])
    print("Hello world")

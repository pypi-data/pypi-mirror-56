"""
Senta Reader
"""

import os
import types
import csv
import numpy as np
from .utils import load_vocab
from .utils import data_reader

import paddle
import paddle.fluid as fluid

class SentaProcessor(object):
    """
    Processor class for data convertors for senta
    """

    def __init__(self,
                 vocab_path,
                 random_seed,
                 max_seq_len,
                 train_data = None,
                 dev_data = None,
                 test_data = None):
        self.vocab = load_vocab(vocab_path)
        self.num_examples = {"train": -1, "dev": -1, "infer": -1}
        np.random.seed(random_seed)
        self.max_seq_len = max_seq_len
        self.train_data = train_data
        self.dev_data = dev_data
        self.test_data = test_data

    def word_to_ids(self, words):
        """convert word to word index"""
        unk_id = len(self.vocab)
        pad_id = 0
        wids = [self.vocab[x] if x in self.vocab else unk_id
                for x in words]
        seq_len = len(wids)
        if seq_len < self.max_seq_len:
            for i in range(self.max_seq_len - seq_len):
                wids.append(pad_id)
        else:
            wids = wids[:self.max_seq_len]
            seq_len = self.max_seq_len

        return wids, seq_len

    def get_train_examples(self, data_dir, epoch, max_seq_len):
        """
        Load training examples
        """
        return data_reader((self.train_data), self.vocab, self.num_examples, "train", epoch, max_seq_len)

    def get_dev_examples(self, data_dir, epoch, max_seq_len):
        """
        Load dev examples
        """
        return data_reader((self.dev_data), self.vocab, self.num_examples, "dev", epoch, max_seq_len)

    def get_test_examples(self, data_dir, epoch, max_seq_len):
        """
        Load test examples
        """
        return data_reader((self.test_data), self.vocab, self.num_examples, "infer", epoch, max_seq_len)

    def get_labels(self):
        """
        Return Labels
        """
        return ["0", "1"]

    def get_num_examples(self, phase):
        """
        Return num of examples in train, dev, test set
        """
        if phase not in ['train', 'dev', 'infer']:
            raise ValueError(
                "Unknown phase, which should be in ['train', 'dev', 'infer'].")
        return self.num_examples[phase]

    def get_train_progress(self):
        """
        Get train progress
        """
        return self.current_train_example, self.current_train_epoch

    def data_generator(self, batch_size, phase='train', epoch=1, shuffle=True):
        """
        Generate data for train, dev or infer
        """
        if phase == "train":
            return paddle.batch(self.get_train_examples(self.train_data, epoch, self.max_seq_len), batch_size)
            #return self.get_train_examples(self.data_dir, epoch, self.max_seq_len)
        elif phase == "dev":
            return paddle.batch(self.get_dev_examples(self.dev_data, epoch, self.max_seq_len), batch_size)
        elif phase == "infer":
            return paddle.batch(self.get_test_examples(self.test_data, epoch, self.max_seq_len), batch_size)
        else:
            raise ValueError(
                "Unknown phase, which should be in ['train', 'dev', 'infer'].")

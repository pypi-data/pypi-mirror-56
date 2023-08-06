# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2019 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
本文件定义了Senta类，实现其情感分类，训练模型的接口。

"""
import os

import paddle.fluid as fluid
from paddle.fluid.core import PaddleBuf
from paddle.fluid.core import PaddleDType
from paddle.fluid.core import PaddleTensor
from paddle.fluid.core import AnalysisConfig
from paddle.fluid.core import create_paddle_predictor
import numpy as np
import io

from .model_check import check_cuda
from .config import PDConfig
from ._compat import *
from . import run_classifier
from . import reader

name = 'Senta'
version = "1.0.1"
version_info = (1, 0, 1)

_get_abs_path = lambda path: os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__), path))

DEFAULT_MODEL = _get_abs_path('infer_model')

class Senta(object):
    """docstring for Senta"""
    def __init__(self, model_path=DEFAULT_MODEL, use_cuda=False):
        super(Senta, self).__init__()
        check_cuda(use_cuda)

        self.args = PDConfig(_get_abs_path('senta_config.json'))
        self.args.build()
        self.args.print_arguments()
        self.args.use_cuda = use_cuda
        self.args.vocab_path = _get_abs_path(self.args.vocab_path)
        self.model_path = model_path
        config = AnalysisConfig(model_path)

        # init executor
        if use_cuda:
            self.place = fluid.CUDAPlace(int(os.getenv('FLAGS_selected_gpus', '0')))
            config.enable_use_gpu(memory_pool_init_size_mb=500,
                                  device_id=int(os.getenv('FLAGS_selected_gpus', '0')),
                                  )
        else:
            self.place = fluid.CPUPlace()
        self.exe = fluid.Executor(self.place)

        self.dataset = reader.SentaProcessor(vocab_path=self.args.vocab_path,
                                        random_seed=self.args.random_seed,
                                        max_seq_len=self.args.max_seq_len)


        self.predictor = create_paddle_predictor(config)

    def predict(self, texts):
        """
        the sentiment classifier's function
        :param texts: a unicode string or a list of unicode strings.
        :return: sentiment prediction results.
        """

        if isinstance(texts, text_type):
            texts = [texts]

        data, seq_len = self.create_input(texts)
        np_probs = self.predictor.run([data, seq_len])
        np_probs = np_probs[0]
        size = np_probs.shape
        np_probs = np.reshape(np.array(np_probs.data.float_data()), size)

        results = []
        for text, probs in zip(texts, np_probs):
            results.append((text, np.argmax(probs), probs[0], probs[1]))

        return results

    def calculate_acc(self, texts, labels):
        if isinstance(texts, text_type):
            texts = [texts]

        data, seq_len = self.create_input(texts)
        np_probs = self.predictor.run([data, seq_len])
        np_probs = np_probs[0]
        size = np_probs.shape
        np_probs = np.reshape(np.array(np_probs.data.float_data()), size)

        total = 0.0
        correct = 0.0
        for label, probs in zip(labels, np_probs):
            pred = np.argmax(probs)
            if pred == label:
                correct += 1
            total += 1

        return correct / total if total > 0.0  else 0.0

    def train(self, model_save_dir, train_data, test_data=None):
        """
        the function use to retrain model
        :param model_save_dir: where to saving model after training
        """
        if self.model_path:
            self.args.init_checkpoint = self.model_path

        self.args.model_save_dir = model_save_dir
        self.args.train_data=train_data
        self.args.do_train = True
        if test_data:
            self.args.test_data=test_data
            self.args.do_infer = True
        # train the model.
        run_classifier.train(self.args)

        config = AnalysisConfig(model_save_dir)
        if self.args.use_cuda:
            config.enable_use_gpu(memory_pool_init_size_mb=500,
                                  device_id=int(os.getenv('FLAGS_selected_gpus', '0')),
                                  )
        # create inference model.
        self.predictor = create_paddle_predictor(config)

    def load_model(self, model_dir):
        """
        load pretrain model
        """
        config = AnalysisConfig(model_dir)
        self.predictor = create_paddle_predictor(config)

    def create_input(self, texts):
        """
        convert the string to model's input tensor
        :param texts: a list of strings
        :return: tensor
        """

        tensor_data = PaddleTensor()
        tensor_seq_lens = PaddleTensor()

        data = []
        seq_lens = []

        for i, text in enumerate(texts):
            text_inds, seq_len = self.dataset.word_to_ids(text)

            data.extend(text_inds)
            seq_lens.append(seq_len)

        tensor_data.shape = [len(texts), self.args.max_seq_len, 1]
        tensor_data.data = PaddleBuf(data)
        tensor_data.name = "src_ids"
        tensor_data.dtype = PaddleDType.INT64

        tensor_seq_lens.shape = [len(texts), 1]
        tensor_seq_lens.data = PaddleBuf(seq_lens)
        tensor_seq_lens.name = "seq_len"
        tensor_seq_lens.dtype = PaddleDType.INT64

        return tensor_data, tensor_seq_lens


if __name__ == "__main__":
    senta = Senta('infer_model')

    # load test data
    # test_data = []
    # test_labels = []
    # with io.open("Senta_data.char/test.tsv", "r", encoding='utf8') as fin:
    #     for line in fin:
    #         if line.startswith('text_a'):
    #             continue
    #         cols = line.strip().split("\t")
    #         if len(cols) != 2:
    #             sys.stderr.write("[NOTICE] Error Format Line!")
    #             continue
    #         label = int(cols[1])
    #         wids = cols[0].split(" ")
    #         sent = "".join(wids)
    #         test_data.append(sent)
    #         test_labels.append(label)
    #
    # acc = senta.calculate_acc(test_data, test_labels)
    # print("accuracy on the new test data: {:.2f}".format(acc))  # 0.86

    test_data = [u'百度是一家高科技公司', u'中山大学是岭南第一学府', '']

    print('######### sentiment prediction, list of sentences ##############')
    results = senta.predict(test_data)
    for res in results:
        print(res)

    # post-train the model
    # senta.train(model_save_dir = 'models_test', train_data="post_train_data/train.tsv")
    #
    # print('######### sentiment prediction, list of sentences ##############')
    # result = senta.predict(test_data)
    # for res in result:
    #     print(res)

    # acc = senta.calculate_acc(test_data, test_labels)
    # print("accuracy on the new test data: {:.2}".format(acc))  # 0.90


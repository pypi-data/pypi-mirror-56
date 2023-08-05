# -*- coding: utf-8 -*-
"""
BertTokenizer类
"""

import tensorflow as tf
from bert.tokenization import FullTokenizer


class BertTokenizer(tf.keras.layers.Layer):

    def __init__(self, vocab_file=None, sos=True, eos=True):
        super(BertTokenizer, self).__init__(self, dynamic=True)
        self.tokenizer = None
        self.vocab_file = vocab_file
        self.sos = sos
        self.eos = eos
        self.tokenizer = FullTokenizer(vocab_file=self.vocab_file)

    def compute_output_shape(self, input_shape):
        batch_size = input_shape[0]
        max_length = input_shape[1]
        return tf.TensorShape([
            batch_size, max_length
        ])

    def build(self, input_shape):
        self.built = True

    def transform(self, X):
        def _trans(text):
            tokens = self.tokenizer.tokenize(text)
            if self.sos and self.eos:
                tokens = ['[CLS]'] + tokens + ['[SEP]']
            elif self.sos:
                tokens = ['[CLS]'] + tokens
            elif self.eos:
                tokens = tokens + ['[SEP]']
            ids = self.tokenizer.convert_tokens_to_ids(tokens)
            return ids
        result = [
            _trans(x)
            for x in X
        ]
        max_length = max([len(x) for x in result])
        pad = self.tokenizer.convert_tokens_to_ids(['[PAD]'])
        result = [
            x + (max_length - len(x)) * pad
            for x in result
        ]
        return result

    def call(self, inputs):
        x = inputs
        x = self.transform(inputs)
        x = tf.convert_to_tensor(x)
        return x


def test():
    layer = BertTokenizer('./chinese_L-12_H-768_A-12/vocab.txt')
    x = [
        '你好',
        '你好吗'
    ]
    print(layer(x))


if __name__ == "__main__":
    test()

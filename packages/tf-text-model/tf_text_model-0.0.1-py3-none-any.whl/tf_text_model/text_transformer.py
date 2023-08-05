# -*- coding: utf-8 -*-
"""
TextTransformer类，主要目的是成为tf2的一层，用来让系统能将已经tokenlize的文本转换为ids

这里为什么叫Transformer而不是Tokenizer？
str: 一句话（或一个文档）的字符串，例如 "我喜欢你"
token: 已经分割好的字符，例如中文分词，中文直接按字分割（例如list("我喜欢你")），或者如bert的分词方法（比较复杂）
ids: 指已经数字化后的数字向量（矩阵），如 [0, 1, 2, 3]
Tokenizer: str到token，或者str直接到ids
Transformer: 这里是指从token到ids
"""

import os
import numpy as np
import tensorflow as tf

PAD = '[PAD]'
UNK = '[UNK]'
SOS = '[CLS]'
EOS = '[SEP]'


class TextTransformer(tf.keras.layers.Layer):

    def __init__(self, vocab=None, sos=True, eos=True):
        """
            vocab:
                - 当为list或tuple时，它是一个词表列表
                - 当为str并且存在路径时，是一个以换行为分割的，每行一个词的词表文件
            sos: 是否在转换的时候加入[CLS]开头
            sos: 是否在转换的时候加入[SEP]结尾
        """
        super(TextTransformer, self).__init__(self, dynamic=True)
        self.sos = sos
        self.eos = eos
        self.fitted = False
        self.word_index = {
            PAD: 0,
            UNK: 1,
            SOS: 2,
            EOS: 3
        }
        if isinstance(vocab, (list, tuple)):
            words = []
            wordi = {}
            for i, w in enumerate(vocab):
                if w not in wordi:
                    wordi[w] = True
                    words.append(w)
            words = [x for x in [PAD, UNK, SOS, EOS] if x not in wordi] + words
            self.word_index = {w: i for i, w in enumerate(words)}
            self.index_word = {v: k for k, v in self.word_index.items()}
            self.vocab_size = len(self.word_index)
            self.fitted = True
        elif isinstance(vocab, str) and os.path.exists(vocab):
            words = []
            wordi = {}
            with open(vocab, 'r', encoding='utf-8') as fp:
                for line in fp:
                    if line.endswith('\n'):
                        line = line[:-1]
                    if len(line) and line not in wordi:
                        wordi[line] = True
                        words.append(line)
            words = [x for x in [PAD, UNK, SOS, EOS] if x not in wordi] + words
            self.word_index = {w: i for i, w in enumerate(words)}
            self.index_word = {v: k for k, v in self.word_index.items()}
            self.vocab_size = len(self.word_index)
            self.fitted = True

    def fit(self, X):
        for sent in X:
            for word in sent:
                if word not in self.word_index:
                    self.word_index[word] = len(self.word_index)
        self.vocab_size = len(self.word_index)
        self.index_word = {v: k for k, v in self.word_index.items()}
        self.fitted = True

    def inverse_transform(self, X):
        assert self.fitted
        ret = []
        for sent in X:
            words = []
            for w in sent:
                if w <= 0:
                    break
                if w in self.index_word:
                    words.append(self.index_word[w])
            ret.append(words)
        return ret

    def build(self, input_shape):
        self.built = True

    def transform(self, X):
        assert self.fitted
        if hasattr(X, 'shape'):
            batch_size = X.shape[0]
        else:
            batch_size = len(X)
        max_length = max([len(x) for x in X]) + (
            1 if self.sos else 0) + (1 if self.eos else 0)
        result = np.zeros((batch_size, max_length), dtype=np.int32)
        for sent_id, sent in enumerate(X):
            if self.sos:
                result[sent_id][0] = self.word_index[SOS]
            for word_id, word in enumerate(sent):
                result[sent_id][
                    word_id + (1 if self.sos else 0)
                ] = self.word_index.get(
                    word, self.word_index[UNK])
            if self.eos:
                result[sent_id][
                    len(sent) + (1 if self.sos else 0)
                ] = self.word_index[EOS]
        return result

    def call(self, inputs):
        x = inputs
        x = self.transform(inputs)
        return tf.convert_to_tensor(x)


def test():
    vocab = ['你', '好', '吗']
    layer = TextTransformer(vocab=vocab)
    layer1 = TextTransformer(vocab=vocab, sos=False)
    layer2 = TextTransformer(vocab=vocab, eos=False)
    layer3 = TextTransformer(vocab=vocab, sos=False, eos=False)
    print(layer.word_index)
    x = [
        ['你', '好'],
        ['你', '好', '吗']
    ]
    print(layer(x))
    print(layer1(x))
    print(layer2(x))
    print(layer3(x))


if __name__ == "__main__":
    test()

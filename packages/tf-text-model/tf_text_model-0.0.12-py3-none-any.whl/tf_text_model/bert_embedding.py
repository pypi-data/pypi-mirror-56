# -*- coding: utf-8 -*-
"""
BERT类，主要目的是成为tf2的一层，用来让系统直接能转换文本到embedding
"""

import os
import tensorflow as tf
from bert import BertModelLayer
from bert import params_from_pretrained_ckpt
from bert import load_stock_weights


class BertEmbedding(tf.keras.layers.Layer):

    def __init__(self, bert_params, trainable=False, model_dir=None):
        super(BertEmbedding, self).__init__(self)

        if isinstance(bert_params, str) and os.path.exists(bert_params):
            bert_params = params_from_pretrained_ckpt(
                os.path.dirname(bert_params))
            self.bert_params = bert_params

        self.bert = BertModelLayer.from_params(bert_params, name="bert")

        input_ids = tf.keras.layers.Input(
            shape=(bert_params.max_position_embeddings,),
            dtype='int32', name="input_ids")
        output = self.bert(input_ids)
        model = tf.keras.Model(inputs=input_ids, outputs=output)
        model.build(input_shape=(None, bert_params.max_position_embeddings))

        def _flatten_layers(root_layer):
            if isinstance(root_layer, tf.keras.layers.Layer):
                yield root_layer
            for layer in root_layer._layers:
                for sub_layer in _flatten_layers(layer):
                    yield sub_layer
        if not trainable:
            for layer in _flatten_layers(self.bert):
                layer.trainable = False

        if model_dir is not None:
            bert_ckpt_file = os.path.join(model_dir, "bert_model.ckpt")
            load_stock_weights(self.bert, bert_ckpt_file)

    def compute_output_shape(self, input_shape):
        batch_size = input_shape[0]
        max_length = input_shape[1]
        return tf.TensorShape([
            batch_size, max_length, self.bert_params.hidden_size])

    def build(self, input_shape):
        self.built = True

    def call(self, inputs, mask=None):
        return self.bert(inputs)


if __name__ == "__main__":
    bd = './chinese_L-12_H-768_A-12/'
    BertEmbedding(bd, False, bd)

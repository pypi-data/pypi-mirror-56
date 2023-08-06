# -*- coding: utf-8 -*-
import math
import numpy as np
import tensorflow as tf
from tqdm import tqdm
from .model_wrapper import ModelWrapper


class Classifier(ModelWrapper):

    def __call__(self, inputs, batch_size=32):
        total_batch = math.ceil(len(inputs) / batch_size)
        ret = []
        for i in range(total_batch):
            x_batch = inputs[i * batch_size: (i + 1) * batch_size]
            ret_batch = tf.argmax(self.model(inputs), -1)
            ret += ret_batch.numpy().tolist()
        return ret

    def predict(self, inputs, batch_size=32):
        return self.__call__(inputs, batch_size)

    def fit(self, X, y, epoch=10, batch_size=32):
        if self.model is None:
            self.model = model = self.build()
        y = np.array(y)
        if len(y.shape) == 1:
            y = tf.keras.utils.to_categorical(y)
        optimizer = tf.keras.optimizers.Adam()

        total_batch = math.ceil(len(X) / batch_size)
        for e in range(epoch):
            pbar = tqdm(range(total_batch))
            losses = []
            for i in pbar:
                x_batch = X[i * batch_size: (i + 1) * batch_size]
                y_batch = y[i * batch_size: (i + 1) * batch_size]
                with tf.GradientTape() as tape:
                    logits = model(x_batch)
                    loss = tf.keras.losses.categorical_crossentropy(logits, y_batch)
                gradients = tape.gradient(loss, model.trainable_variables)
                optimizer.apply_gradients(
                    zip(gradients, model.trainable_variables))
                loss_ = loss.numpy().mean()
                losses.append(loss_)
                pbar.set_description(f'epoch {e + 1} loss {np.mean(losses):.4f}')

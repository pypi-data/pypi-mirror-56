# -*- coding: utf-8 -*-
import tensorflow as tf
from tqdm import tqdm


class ModelWrapper(object):

    def __init__(self, builder):
        self.build = builder
        self.model = None

    def __getstate__(self):
        """Pickle compatible."""
        state = self.__dict__.copy()
        if self.model is not None:
            state['model_weights'] = state['model'].get_weights()
            del state['model']
        return state

    def __setstate__(self, state):
        """Pickle compatible."""
        if 'model_weights' in state:
            model_weights = state.get('model_weights')
            del state['model_weights']
            state['bert_model_dir'] = None
            self.__dict__.update(state)
            self.model = self.build()
            self.model.set_weights(model_weights)
        else:
            self.__dict__.update(state)

    def __call__(self, inputs):
        return self.model(inputs)

    def predict(self, inputs):
        return self.__call__(inputs)

    def fit(self, X, y):
        if self.model is None:
            self.model = model = self.build()
        optimizer = tf.keras.optimizers.Adam()
        pbar = tqdm(range(10))
        for i in pbar:
            with tf.GradientTape() as tape:
                logits = model(X)
                loss = tf.keras.losses.categorical_crossentropy(logits, y)
            gradients = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(
                zip(gradients, model.trainable_variables))
            loss_ = loss.numpy().mean()
            pbar.set_description(f'epoch {i + 1} loss {loss_}')

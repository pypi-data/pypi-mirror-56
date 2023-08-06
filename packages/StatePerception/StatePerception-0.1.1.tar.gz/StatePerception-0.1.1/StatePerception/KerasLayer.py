"""
@author: Torben Gräber
"""

import tensorflow as tf
from keras.engine.topology import Layer
from keras.losses import mean_squared_error
from keras import backend as K
import numpy as np

# =============================================================================
# Custom Loss
# =============================================================================


class loss_with_convergence_time():

    def __init__(self, loss_function=mean_squared_error, convergence_time=100):
        self.loss_function = loss_function
        self.convergence_time = convergence_time
        self.__name__ = loss_function.__name__ + \
            '_convtime' + str(convergence_time)

    def __call__(self, y_true, y_pred):
        # Apply Mask
        y_true, y_pred = self._mask(y_true, y_pred)
        # Calculate Loss
        return self.loss_function(y_true, y_pred)

    def _mask(self, y_true, y_pred):
        # Apply Mask
        y_true = y_true[:, self.convergence_time:, :]
        y_pred = y_pred[:, self.convergence_time:, :]
        return y_true, y_pred


class weighted_loss():

    def __init__(self, loss_function=mean_squared_error, loss_weights=None):
        # Tensor
        self.loss_function = loss_function
        self.loss_weights = tf.expand_dims(
            tf.expand_dims(
                tf.constant(
                    value=loss_weights,
                    dtype=tf.float32),
                axis=0),
            axis=1)
        self.__name__ = loss_function.__name__ + '_weighted'

    def __call__(self, y_true, y_pred):
        # Weight Vectors
        y_true, y_pred = self._weight_outputs(y_true, y_pred)
        # Calculate Loss
        loss = self.loss_function(y_true, y_pred)
        # Return
        return loss

    def _weight_outputs(self, y_true, y_pred):
        # Multiply Weights to y_true and y_pred
        y_true_weighted = tf.multiply(y_true, self.loss_weights)
        y_pred_weighted = tf.multiply(y_pred, self.loss_weights)
        # Return
        return y_true_weighted, y_pred_weighted


# =============================================================================
# Instantiated Custom Loss
# =============================================================================
mean_squared_error_convtime100 = loss_with_convergence_time(
    loss_function=mean_squared_error,
    convergence_time=100)
mse_conv100_w2 = weighted_loss(
    loss_function=mean_squared_error_convtime100,
    loss_weights=np.array([0.5, 2]))

# =============================================================================
# Custom Layers
# =============================================================================


class PCA_Layer(Layer):

    def __init__(self, components, idx, input_dim, **kwargs):
        self._components = components  # np array
        self._idx = idx
        self._input_dim = input_dim

        # build kernel
        kernel = np.diag(np.ones(self._input_dim))
        for i, idx_curr in enumerate(self._idx):
            kernel[idx_curr, self._idx] = components[i, :]
        self._kernel = np.transpose(kernel)

        super(PCA_Layer, self).__init__(**kwargs)

    def build(self, input_shape):

        # Get Initializers
        kernel_init = tf.constant_initializer(
            value=self._kernel, dtype=tf.float32)

        # Create a trainable weight variable for this layer.
        self.kernel = self.add_weight(name='kernel',
                                      shape=self._kernel.shape,
                                      initializer=kernel_init,
                                      trainable=False)
        # Be sure to call this somewhere!
        super(PCA_Layer, self).build(input_shape)

    def call(self, x):
        return K.dot(x, self.kernel)

    def compute_output_shape(self, input_shape):
        return input_shape


class ConstantNormalizationLayer(Layer):

    def __init__(self, scale, mean=None, position='input', **kwargs):
        self._mean = mean
        self._scale = scale
        self._position = position

        super(ConstantNormalizationLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        # Get Initializers
        if self._mean is not(None):
            mean_init = tf.constant_initializer(
                value=self._mean, dtype=tf.float32)
        scale_init = tf.constant_initializer(
            value=self._scale, dtype=tf.float32)

        # Create Constants for Normalization
        if self._mean is not(None):
            self.mean = self.add_weight(
                name='mean',
                shape=(
                    self._mean.shape[0],
                ),
                trainable=False,
                initializer=mean_init)
        self.scale = self.add_weight(
            name='scale',
            shape=(
                self._scale.shape[0],
            ),
            trainable=False,
            initializer=scale_init)

        super(ConstantNormalizationLayer, self).build(input_shape)

    def call(self, x):
        if self._position == 'input':
            if self._mean is not(None):
                x = x - self.mean
            x = tf.multiply(x, tf.divide(1, self.scale))
        if self._position == 'output':
            x = tf.multiply(x, self.scale)
            if self._mean is not(None):
                x = x + self.mean
        return x

    def compute_output_shape(self, input_shape):
        return input_shape


class DerivativeLayer(Layer):

    def __init__(self, dt, order=1, factor=1, **kwargs):
        # Write Arguments
        self._dt = dt
        self._order = order
        self._factor = factor
        # Init Super
        super(DerivativeLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        # Get Initializers
        dt_init = tf.constant_initializer(value=self._dt, dtype=tf.float32)
        factor_init = tf.constant_initializer(
            value=self._factor, dtype=tf.float32)
        # Create Constants
        self.dt = self.add_weight(name='dt', shape=(
            1,), trainable=False, initializer=dt_init)
        self.factor = self.add_weight(name='factor', shape=(
            1,), trainable=False, initializer=factor_init)
        # Build Super
        super(DerivativeLayer, self).build(input_shape)

    def call(self, x):
        # Loop over derivatives (order)
        for i in range(self._order):
            # Differences
            der_start = (x[:, 1:, :] - x[:, 0:-1, :]) / self._dt  # Right DQ
            # der_center = (x[:,2:,:]-x[:,0:-2,:])/self._dt # Central DQ
            der_end = (x[:, -1:, :] - x[:, -2:-1, :]) / self._dt  # Left DQ
            # Concatenate
            x = tf.concat([der_start, der_end], axis=1)
        # Apply Factor
        if self._factor != 1:
            x = self.factor * x
        return x

    def compute_output_shape(self, input_shape):
        return input_shape


class AddMeanSignalsToSignal(Layer):

    def __init__(
            self,
            ind_mean_signals=[
                4,
                5,
                6,
                7],
            ind_target_signal=0,
            **kwargs):
        # Write Arguments
        self.ind_mean_signals = ind_mean_signals
        self.ind_target_signal = ind_target_signal
        # Init Super
        super(AddMeanSignalsToSignal, self).__init__(**kwargs)

    def build(self, input_shape):
        # Build Super
        super(AddMeanSignalsToSignal, self).build(input_shape)

    def call(self, x):
        # Map tensors
        x0 = x[0]
        x1 = x[1]
        # Average of Soruce Signals
        av = tf.mean(x0[:, :, ind_mean_signals], axis=2) / \
            len(self.ind_mean_signals)

        return

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[1], 1)


class BetaFromVyVx(Layer):

    def __init__(self, ind_vx=0, ind_vy=1, **kwargs):
        # Write Arguments
        self.ind_vx = ind_vx
        self.ind_vy = ind_vy
        # Init Super
        super(BetaFromVyVx, self).__init__(**kwargs)

    def build(self, input_shape):
        # Build Super
        super(BetaFromVyVx, self).build(input_shape)

    def call(self, x):
        vx = x[:, :, self.ind_vx]
        vy = x[:, :, self.ind_vy]
        return tf.expand_dims(tf.atan(tf.divide(vy, vx)), axis=2)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[1], 1)


# =============================================================================
# Custom Functions Lib
# =============================================================================
class CustomFunctionsLib():

    def __init__(self):
        self.fundict = {
            'mean_squared_error_convtime100': mean_squared_error_convtime100,
            'PCA_Layer': PCA_Layer,
            'ConstantNormalizationLayer': ConstantNormalizationLayer}

# coding=utf-8

import numpy as np
import autograd.numpy as anp
from autograd import grad
from autograd.misc.optimizers import adam


def conv2d_spatial_decomposition(conv_weight, conv_bias, optimizer_params):
    assert conv_weight.dtype == conv_bias.dtype
    param_dtype = conv_weight.dtype

    original_out_channels = conv_weight.shape[0]
    new_out_channels = optimizer_params['new_out_channels']
    loss_lambda = optimizer_params['loss_lambda']
    num_iters = optimizer_params['num_iters']
    learning_rate = optimizer_params['learning_rate']
    verbose = optimizer_params['verbose']

    new_conv_weight = anp.random.rand(new_out_channels, 1, conv_weight.shape[2], conv_weight.shape[3]).astype(param_dtype)
    new_conv_bias = anp.random.rand(new_out_channels).astype(param_dtype)
    alpha = anp.random.rand(original_out_channels, new_out_channels).astype(param_dtype)

    def loss_fun(params, iter):
        new_conv_weight, new_conv_bias, alpha = params

        a = anp.tile(new_conv_weight, [1, conv_weight.shape[1], 1, 1])
        b = conv_weight.reshape(conv_weight.shape[0], -1) - alpha @ a.reshape([new_conv_weight.shape[0], -1])
        c = anp.linalg.norm(b)

        d = conv_bias - alpha @ new_conv_bias
        e = anp.linalg.norm(d)

        f = 0.0
        for i in anp.split(new_conv_weight, new_conv_weight.shape[0]):
            i = i.squeeze()
            assert len(i.shape) == 2
            f += anp.linalg.norm(i, ord='nuc')

        loss = c + e + loss_lambda * f

        if verbose:
            print(loss)
        return loss

    grad_fun = grad(loss_fun)

    new_conv_weight, new_conv_bias, alpha = adam(
        grad_fun,
        [new_conv_weight, new_conv_bias, alpha],
        num_iters=num_iters,
        step_size=learning_rate
    )

    return new_conv_weight, new_conv_bias, alpha


def conv2d_channel_decomposition(conv_weight, conv_bias, optimizer_params):
    assert conv_weight.dtype == conv_bias.dtype
    assert conv_weight.shape[0] == conv_bias.shape[0]

    new_out_channels = optimizer_params['new_out_channels']

    flattened_params = np.concatenate([conv_weight.reshape(conv_weight.shape[0], -1),
                                       conv_bias.reshape(conv_bias.shape[0], 1)], axis=1)

    u, _, _ = np.linalg.svd(flattened_params, full_matrices=False)
    u = u[:, :new_out_channels]

    new_conv_weight = u.T @ conv_weight.reshape(conv_weight.shape[0], -1)
    new_conv_bias = u.T @ conv_bias.reshape(conv_bias.shape[0], 1)

    new_conv_weight = new_conv_weight.reshape(new_conv_weight.shape[0], conv_weight.shape[1], conv_weight.shape[2], conv_weight.shape[3])
    new_conv_bias = new_conv_bias.reshape(new_conv_bias.shape[0])

    return new_conv_weight, new_conv_bias, u


def conv2d_network_decoupling():
    pass

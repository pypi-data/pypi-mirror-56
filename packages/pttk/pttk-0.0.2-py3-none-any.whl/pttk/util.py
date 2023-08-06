# coding=utf-8

import numpy as np
import uuid


def get_numpy_dtype(onnx_data_type):
    # see onnx-ml.proto -> DataType
    return {1: np.float32, 2: np.uint8, 3: np.int8, 4: np.uint16, 5: np.int16,
            6: np.int32, 7: np.int64, 8: np.str, 9: np.bool, 10: np.float16,
            11: np.double, 12: np.uint32, 13: np.uint64, 14: np.complex64, 15: np.complex128}[onnx_data_type]


def get_onnx_data_type(numpy_dtype):
    return {np.float32: 1, np.uint8: 2, np.int8: 3, np.uint16: 4, np.int16: 5,
            np.int32: 6, np.int64: 7, np.str: 8, np.bool: 9, np.float16: 10,
            np.double: 11, np.uint32: 12, np.uint64: 13, np.complex64: 14, np.complex128: 15}[numpy_dtype]


def get_name():
    return str(uuid.uuid1())


def get_raw_data(onnx_model):
    raw_data_info = {}

    for node in onnx_model.graph.node:
        if node.op_type == 'Constant':
            assert len(node.attribute) == 1
            assert node.attribute[0].name == 'value'
            assert node.attribute[0].type == 4  # TENSOR

            node_t = node.attribute[0].t

            raw_data_dims = node_t.dims
            raw_data_dtype = get_numpy_dtype(node_t.data_type)
            raw_data = np.frombuffer(node_t.raw_data, dtype=raw_data_dtype).reshape(raw_data_dims)

            for node_output in node.output:
                raw_data_info[node_output] = raw_data_dims, raw_data

    for initializer in onnx_model.graph.initializer:
        raw_data_dims = initializer.dims
        raw_data_dtype = get_numpy_dtype(initializer.data_type)
        raw_data = np.frombuffer(initializer.raw_data, dtype=raw_data_dtype).reshape(raw_data_dims)
        raw_data_info[initializer.name] = raw_data_dims, raw_data

    return raw_data_info

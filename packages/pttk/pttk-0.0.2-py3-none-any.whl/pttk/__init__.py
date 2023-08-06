# coding=utf-8

import numpy as np
import yaml
import onnx
from toposort import toposort_flatten
import pttk.optimizer as optimizer
import pttk.util as util


def analyze_model(model_path, output_config_path):
    onnx_model = onnx.load(model_path)

    op_type_stat = {}
    optimizable_ops = {}

    raw_data_info = util.get_raw_data(onnx_model)

    # analyze ops
    for node_index, node in enumerate(onnx_model.graph.node):
        if node.op_type == 'Conv':
            is_2d_conv = False
            for attr in node.attribute:
                if attr.name == 'kernel_shape' and len(attr.ints) == 2:
                    is_2d_conv = True
                    break

            node_op_type = 'Conv2d' if is_2d_conv else 'NonConv2d'
        else:
            node_op_type = node.op_type

        if node_op_type not in op_type_stat:
            op_type_stat[node_op_type] = 0
        op_type_stat[node_op_type] += 1

        if node_op_type in ['Conv2d']:
            if node_op_type not in optimizable_ops:
                optimizable_ops[node_op_type] = []
            optimizable_ops[node_op_type].append({
                'basic_info': {
                    'node_index': node_index,
                    'original_out_channels': raw_data_info[node.input[1]][0][0]
                },
                'optimizer': {
                    'spatial_decomposition': {
                        'new_out_channels': None,
                        'loss_lambda': None,
                        'num_iters': None,
                        'learning_rate': None,
                        'verbose': None
                    },
                    'channel_decomposition': {
                        'new_out_channels': None
                    },
                    'network_decoupling': None
                }
            })

    print(op_type_stat)

    with open(output_config_path, 'w', encoding='utf-8') as fout:
        yaml.dump(optimizable_ops, fout)


def optimize_model(model_path, config_path, output_model_path):
    onnx_model = onnx.load(model_path)
    raw_data_info = util.get_raw_data(onnx_model)

    with open(config_path, encoding='utf-8') as fin:
        optimizable_op_config = yaml.load(fin)

    for op_type, op_config_list in optimizable_op_config.items():
        if op_type == 'Conv2d':
            for op_config in op_config_list:
                op_node = onnx_model.graph.node[op_config['basic_info']['node_index']]

                conv_weight, conv_bias = raw_data_info[op_node.input[1]][1], raw_data_info[op_node.input[2]][1]
                op_optimizer_name = list(op_config['optimizer'].keys())[0]

                if op_optimizer_name == 'spatial_decomposition':
                    new_conv_weight, new_conv_bias, alpha = optimizer.conv2d_spatial_decomposition(
                        conv_weight,
                        conv_bias,
                        op_config['optimizer'][op_optimizer_name]
                    )

                    conv_weight_initializer = onnx.helper.make_tensor(
                        name=util.get_name(),
                        data_type=util.get_onnx_data_type(type(np.ones(1, dtype=new_conv_weight.dtype)[0])),
                        dims=new_conv_weight.shape,
                        vals=new_conv_weight.tobytes(),
                        raw=True
                    )
                    onnx_model.graph.initializer.append(conv_weight_initializer)

                    conv_weight_expand_dims = onnx.helper.make_tensor(
                        name=util.get_name(),
                        data_type=util.get_onnx_data_type(np.int64),
                        dims=[4],
                        vals=np.array(
                            [new_conv_weight.shape[0],
                             conv_weight.shape[1],
                             new_conv_weight.shape[2],
                             new_conv_weight.shape[3]],
                            dtype=np.int64
                        ).tobytes(),
                        raw=True
                    )
                    onnx_model.graph.initializer.append(conv_weight_expand_dims)

                    conv_weight_expand_node = onnx.helper.make_node(
                        op_type='Expand',
                        inputs=[conv_weight_initializer.name, conv_weight_expand_dims.name],
                        outputs=[util.get_name()]
                    )
                    onnx_model.graph.node.append(conv_weight_expand_node)

                    op_node.input[1] = conv_weight_expand_node.output[0]
                elif op_optimizer_name == 'channel_decomposition':
                    new_conv_weight, new_conv_bias, alpha = optimizer.conv2d_channel_decomposition(
                        conv_weight,
                        conv_bias,
                        op_config['optimizer'][op_optimizer_name]
                    )

                    conv_weight_initializer = onnx.helper.make_tensor(
                        name=util.get_name(),
                        data_type=util.get_onnx_data_type(type(np.ones(1, dtype=new_conv_weight.dtype)[0])),
                        dims=new_conv_weight.shape,
                        vals=new_conv_weight.tobytes(),
                        raw=True
                    )
                    onnx_model.graph.initializer.append(conv_weight_initializer)

                    op_node.input[1] = conv_weight_initializer.name
                elif op_optimizer_name == 'network_decoupling':
                    pass

                conv_bias_initializer = onnx.helper.make_tensor(
                    name=util.get_name(),
                    data_type=util.get_onnx_data_type(type(np.ones(1, dtype=new_conv_bias.dtype)[0])),
                    dims=new_conv_bias.shape,
                    vals=new_conv_bias.tobytes(),
                    raw=True
                )
                onnx_model.graph.initializer.append(conv_bias_initializer)

                op_node.input[2] = conv_bias_initializer.name

                original_node_output = list(op_node.output)
                for _ in range(len(op_node.output)):
                    op_node.output.pop()
                op_node.output.append(util.get_name())

                conv_result_shape0 = onnx.helper.make_node(
                    op_type='Shape',
                    inputs=op_node.output,
                    outputs=[util.get_name()]
                )
                conv_result_shape1 = onnx.helper.make_node(
                    op_type='Shape',
                    inputs=op_node.output,
                    outputs=[util.get_name()]
                )
                conv_result_shape2 = onnx.helper.make_node(
                    op_type='Shape',
                    inputs=op_node.output,
                    outputs=[util.get_name()]
                )
                conv_result_shape3 = onnx.helper.make_node(
                    op_type='Shape',
                    inputs=op_node.output,
                    outputs=[util.get_name()]
                )
                onnx_model.graph.node.extend([
                    conv_result_shape0,
                    conv_result_shape1,
                    conv_result_shape2,
                    conv_result_shape3
                ])

                conv_result_gather0_input = onnx.helper.make_node(
                    op_type='Constant',
                    inputs=[],
                    outputs=[util.get_name()],
                    value=onnx.helper.make_tensor(
                        name='',
                        data_type=util.get_onnx_data_type(np.int64),
                        dims=[],
                        vals=np.array([0]).tobytes(),
                        raw=True
                    )
                )
                conv_result_gather1_input = onnx.helper.make_node(
                    op_type='Constant',
                    inputs=[],
                    outputs=[util.get_name()],
                    value=onnx.helper.make_tensor(
                        name='',
                        data_type=util.get_onnx_data_type(np.int64),
                        dims=[],
                        vals=np.array([1]).tobytes(),
                        raw=True
                    )
                )
                conv_result_gather2_input = onnx.helper.make_node(
                    op_type='Constant',
                    inputs=[],
                    outputs=[util.get_name()],
                    value=onnx.helper.make_tensor(
                        name='',
                        data_type=util.get_onnx_data_type(np.int64),
                        dims=[],
                        vals=np.array([2]).tobytes(),
                        raw=True
                    )
                )
                conv_result_gather3_input = onnx.helper.make_node(
                    op_type='Constant',
                    inputs=[],
                    outputs=[util.get_name()],
                    value=onnx.helper.make_tensor(
                        name='',
                        data_type=util.get_onnx_data_type(np.int64),
                        dims=[],
                        vals=np.array([3]).tobytes(),
                        raw=True
                    )
                )
                onnx_model.graph.node.extend([
                    conv_result_gather0_input,
                    conv_result_gather1_input,
                    conv_result_gather2_input,
                    conv_result_gather3_input
                ])

                conv_result_gather0 = onnx.helper.make_node(
                    op_type='Gather',
                    inputs=[conv_result_shape0.output[0], conv_result_gather0_input.output[0]],
                    outputs=[util.get_name()],
                    axis=0
                )
                conv_result_gather1 = onnx.helper.make_node(
                    op_type='Gather',
                    inputs=[conv_result_shape1.output[0], conv_result_gather1_input.output[0]],
                    outputs=[util.get_name()],
                    axis=0
                )
                conv_result_gather2 = onnx.helper.make_node(
                    op_type='Gather',
                    inputs=[conv_result_shape2.output[0], conv_result_gather2_input.output[0]],
                    outputs=[util.get_name()],
                    axis=0
                )
                conv_result_gather3 = onnx.helper.make_node(
                    op_type='Gather',
                    inputs=[conv_result_shape3.output[0], conv_result_gather3_input.output[0]],
                    outputs=[util.get_name()],
                    axis=0
                )
                onnx_model.graph.node.extend([
                    conv_result_gather0,
                    conv_result_gather1,
                    conv_result_gather2,
                    conv_result_gather3
                ])

                conv_result_unsqueeze0 = onnx.helper.make_node(
                    op_type='Unsqueeze',
                    inputs=[conv_result_gather0.output[0]],
                    outputs=[util.get_name()],
                    axes=[0]
                )
                conv_result_unsqueeze1 = onnx.helper.make_node(
                    op_type='Unsqueeze',
                    inputs=[conv_result_gather1.output[0]],
                    outputs=[util.get_name()],
                    axes=[0]
                )
                conv_result_unsqueeze2 = onnx.helper.make_node(
                    op_type='Unsqueeze',
                    inputs=[conv_result_gather2.output[0]],
                    outputs=[util.get_name()],
                    axes=[0]
                )
                conv_result_unsqueeze3 = onnx.helper.make_node(
                    op_type='Unsqueeze',
                    inputs=[conv_result_gather3.output[0]],
                    outputs=[util.get_name()],
                    axes=[0]
                )
                onnx_model.graph.node.extend([
                    conv_result_unsqueeze0,
                    conv_result_unsqueeze1,
                    conv_result_unsqueeze2,
                    conv_result_unsqueeze3
                ])

                standalone_tensor = onnx.helper.make_node(
                    op_type='Constant',
                    inputs=[],
                    outputs=[util.get_name()],
                    value=onnx.helper.make_tensor(
                        name='',
                        data_type=util.get_onnx_data_type(np.int64),
                        dims=[],
                        vals=np.array([-1]).tobytes(),
                        raw=True
                    )
                )
                standalone_unsqueeze = onnx.helper.make_node(
                    op_type='Unsqueeze',
                    inputs=[standalone_tensor.output[0]],
                    outputs=[util.get_name()],
                    axes=[0]
                )
                onnx_model.graph.node.extend([standalone_tensor, standalone_unsqueeze])

                conv_result_concat = onnx.helper.make_node(
                    op_type='Concat',
                    inputs=[conv_result_unsqueeze0.output[0],
                            conv_result_unsqueeze1.output[0],
                            standalone_unsqueeze.output[0]],
                    outputs=[util.get_name()],
                    axis=0
                )
                onnx_model.graph.node.append(conv_result_concat)

                conv_result_reshape = onnx.helper.make_node(
                    op_type='Reshape',
                    inputs=[op_node.output[0], conv_result_concat.output[0]],
                    outputs=[util.get_name()]
                )
                onnx_model.graph.node.append(conv_result_reshape)

                alpha_tensor = onnx.helper.make_tensor(
                    name=util.get_name(),
                    data_type=util.get_onnx_data_type(type(np.ones(1, dtype=alpha.dtype)[0])),
                    dims=alpha.shape,
                    vals=alpha.tobytes(),
                    raw=True
                )
                matmul_node = onnx.helper.make_node(
                    op_type='MatMul',
                    inputs=[alpha_tensor.name, conv_result_reshape.output[0]],
                    outputs=[util.get_name()]
                )
                onnx_model.graph.initializer.append(alpha_tensor)
                onnx_model.graph.node.append(matmul_node)

                matmul_result_shape0 = onnx.helper.make_node(
                    op_type='Shape',
                    inputs=[matmul_node.output[0]],
                    outputs=[util.get_name()]
                )
                matmul_result_shape1 = onnx.helper.make_node(
                    op_type='Shape',
                    inputs=[matmul_node.output[0]],
                    outputs=[util.get_name()]
                )
                onnx_model.graph.node.extend([matmul_result_shape0, matmul_result_shape1])

                matmul_result_gather0_input = onnx.helper.make_node(
                    op_type='Constant',
                    inputs=[],
                    outputs=[util.get_name()],
                    value=onnx.helper.make_tensor(
                        name='',
                        data_type=util.get_onnx_data_type(np.int64),
                        dims=[],
                        vals=np.array([0]).tobytes(),
                        raw=True
                    )
                )
                matmul_result_gather1_input = onnx.helper.make_node(
                    op_type='Constant',
                    inputs=[],
                    outputs=[util.get_name()],
                    value=onnx.helper.make_tensor(
                        name='',
                        data_type=util.get_onnx_data_type(np.int64),
                        dims=[],
                        vals=np.array([1]).tobytes(),
                        raw=True
                    )
                )
                onnx_model.graph.node.extend([matmul_result_gather0_input, matmul_result_gather1_input])

                matmul_result_gather0 = onnx.helper.make_node(
                    op_type='Gather',
                    inputs=[matmul_result_shape0.output[0], matmul_result_gather0_input.output[0]],
                    outputs=[util.get_name()],
                    axis=0
                )
                matmul_result_gather1 = onnx.helper.make_node(
                    op_type='Gather',
                    inputs=[matmul_result_shape1.output[0], matmul_result_gather1_input.output[0]],
                    outputs=[util.get_name()],
                    axis=0
                )
                onnx_model.graph.node.extend([matmul_result_gather0, matmul_result_gather1])

                matmul_result_unsqueeze0 = onnx.helper.make_node(
                    op_type='Unsqueeze',
                    inputs=[matmul_result_gather0.output[0]],
                    outputs=[util.get_name()],
                    axes=[0]
                )
                matmul_result_unsqueeze1 = onnx.helper.make_node(
                    op_type='Unsqueeze',
                    inputs=[matmul_result_gather1.output[0]],
                    outputs=[util.get_name()],
                    axes=[0]
                )
                onnx_model.graph.node.extend([matmul_result_unsqueeze0, matmul_result_unsqueeze1])

                matmul_result_concat = onnx.helper.make_node(
                    op_type='Concat',
                    inputs=[matmul_result_unsqueeze0.output[0],
                            matmul_result_unsqueeze1.output[0],
                            conv_result_unsqueeze2.output[0],
                            conv_result_unsqueeze3.output[0]],
                    outputs=[util.get_name()],
                    axis=0
                )
                onnx_model.graph.node.append(matmul_result_concat)

                matmul_result_reshape = onnx.helper.make_node(
                    op_type='Reshape',
                    inputs=[matmul_node.output[0], matmul_result_concat.output[0]],
                    outputs=original_node_output
                )
                onnx_model.graph.node.append(matmul_result_reshape)

    # get nodes' topological relation
    node_input_to_indices = {}
    node_output_to_indices = {}
    for node_index, node in enumerate(onnx_model.graph.node):
        for i in node.input:
            if i not in node_input_to_indices:
                node_input_to_indices[i] = set()
            node_input_to_indices[i].add(node_index)
        for i in node.output:
            if i not in node_output_to_indices:
                node_output_to_indices[i] = set()
            node_output_to_indices[i].add(node_index)

    toposort_param = {}
    for i, input_node_indices in node_input_to_indices.items():
        if i in node_output_to_indices:
            output_node_indices = node_output_to_indices[i]
            for j in input_node_indices:
                if j not in toposort_param:
                    toposort_param[j] = set()
                for k in output_node_indices:
                    toposort_param[j].add(k)

    toposort_result = toposort_flatten(toposort_param)

    # re-sort nodes
    sorted_nodes = [onnx_model.graph.node[i] for i in toposort_result]

    for i in range(len(onnx_model.graph.node)):
        onnx_model.graph.node.pop()

    onnx_model.graph.node.extend(sorted_nodes)

    # eliminate unused initializer
    all_inputs_outputs = set()
    for i in onnx_model.graph.node:
        for j in i.input:
            all_inputs_outputs.add(j)
        for j in i.output:
            all_inputs_outputs.add(j)

    for i in range(len(onnx_model.graph.initializer))[::-1]:
        initializer_name = onnx_model.graph.initializer[i].name
        if initializer_name not in all_inputs_outputs:
            onnx_model.graph.initializer.pop(i)

    onnx.checker.check_model(onnx_model)
    # optimized_model = onnx.optimizer.optimize(onnx_model, ['eliminate_unused_initializer'])
    # inferred_model = onnx.shape_inference.infer_shapes(onnx_model)
    # polished_model = onnx.utils.polish_model(onnx_model)
    onnx.save(onnx_model, output_model_path)


if __name__ == '__main__':
    # model_path = 'my_model1.onnx'
    # output_config_path = 'z.yaml'
    # analyze_model(model_path, output_config_path)

    model_path = 'my_model1.onnx'
    config_path = 'zz.yaml'
    output_model_path = 'my_model999.onnx'
    optimize_model(model_path, config_path, output_model_path)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The NSH Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
keras_convtransformer

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/9/11
"""

import tensorflow as tf
from tensorflow.python.keras import layers
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import backend as K
from ..sparse_dnn.DenseLayerForSparse import DenseLayerForSparse
from ..transformer.ConvAlignTransformer import ConvAlignTransformer


def get_model(config):
    maxlen = config['maxlen']
    class_num = config['class_num']
    cross_size = config['cross_size']
    hist_week_id_output = config['hist_week_id_output']
    user_feature_size = config['user_feature_size']
    hist_id_output = config['hist_id_output']
    label_week_id_output = config['label_week_id_output']
    output_unit = config['output_unit']

    hist_id_input = layers.Input(shape=(maxlen,), dtype='int32')
    hist_week_id_input = layers.Input(shape=(maxlen,), dtype='int32')
    cross_feature_input = layers.Input(shape=(cross_size,), dtype='float32', sparse=True)
    user_feature_input = layers.Input(shape=(user_feature_size,), dtype='float32', sparse=True)
    hist_time_input = layers.Input(shape=(maxlen,), dtype='int32')
    hist_time_gaps_input = layers.Input(shape=(maxlen,), dtype='int32')
    label_week_id_input = layers.Input(shape=(maxlen,), dtype='int32')

    hist_id_embeddings = layers.Embedding(class_num, hist_id_output)(hist_id_input)
    hist_week_id_embeddings = layers.Embedding(7, hist_week_id_output)(hist_week_id_input)
    label_week_id_embeddings = layers.Embedding(7, label_week_id_output, mask_zero=True)(label_week_id_input)
    embeddings = layers.Concatenate(axis=-1)([hist_id_embeddings, hist_week_id_embeddings, label_week_id_embeddings])
    cross_feature = DenseLayerForSparse(cross_size, 64, 'relu')(cross_feature_input)
    user_feature = DenseLayerForSparse(user_feature_size, 64, 'relu')(user_feature_input)
    temp_input = embeddings, hist_time_input
    transformer_enc = ConvAlignTransformer(config)(temp_input)
    all_feature = layers.Concatenate(axis=-1)([transformer_enc, user_feature, cross_feature])
    output = layers.Dense(output_unit, activation='softmax')(all_feature)
    model = Model(inputs=[hist_id_input, hist_week_id_input, cross_feature_input, user_feature_input, hist_time_input,
                          hist_time_gaps_input, label_week_id_input], outputs=[output])
    sess = tf.compat.v1.Session()
    sess.run(tf.compat.v1.local_variables_initializer())
    sess.run(tf.compat.v1.global_variables_initializer())
    sess.run(tf.compat.v1.tables_initializer())
    K.set_session(sess)
    loss_dict = {'1':'mean_squared_error'}
    model.compile(loss=loss_dict.get(str(output_unit),'categorical_crossentropy'),
                  optimizer='adam',
                  metrics=[])
    print(model.summary())
    return model

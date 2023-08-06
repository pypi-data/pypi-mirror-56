# encoding: utf-8
"""
@author: BrikerMan
@contact: eliyar917@gmail.com
@blog: https://eliyar.biz

@version: 1.0
@license: Apache Licence
@file: __init__.py
@time: 2019-05-17 11:15

"""
import os
os.environ['TF_KERAS'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from band import bert4keras
from band.macros import TaskType, config

from band.bert4keras.layers import get_custom_objects
custom_objects = get_custom_objects()

CLASSIFICATION = TaskType.CLASSIFICATION
LABELING = TaskType.LABELING

from band.version import __version__

from band import layers
from band import corpus
from band import embeddings
from band import macros
from band import processors
from band import tasks
from band import utils
from band import callbacks

from band import migeration

migeration.show_migration_guide()

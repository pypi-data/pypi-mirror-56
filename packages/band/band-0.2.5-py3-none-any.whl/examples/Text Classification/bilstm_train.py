"""
@author: SunYanCN
@contact: sunyanhust@163.com
@blog: https://sunyancn.github.io
@version: 1.0
@license: MIT Licence
@file: bilstm_train.py
@time: 2019-11-20 14:20:17
"""

import band
from band.corpus import SMP2018ECDTCorpus
from band.tasks.classification import BiLSTM_Model
from band.callbacks import EvalCallBack
from band import utils

# Dataset
dataset = SMP2018ECDTCorpus()

model = BiLSTM_Model()
eval_callback = EvalCallBack(kash_model=model,
                             valid_x=dataset.valid_x,
                             valid_y=dataset.valid_y,
                             step=5)
model.fit(dataset.train_x,
          dataset.train_y,
          dataset.valid_x,
          dataset.valid_y,
          batch_size=32,
          callbacks=[eval_callback])

model.evaluate(dataset.test_x, dataset.test_y)

# Save model to `saved_classification_model` dir
model.save('saved_classification_model')

# Load model
loaded_model = band.utils.load_model('saved_classification_model')

# Use model to predict
loaded_model.predict(dataset.test_x[:10])

# Save model
utils.convert_to_saved_model(model,
                             model_path='saved_model/bilstm',
                             version='1')


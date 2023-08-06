import requests
from band import utils
import numpy as np


def main():
    endpoint = "http://127.0.0.1:8500"
    text = '这个价不算高，和一天内训相比相差无几'
    processor = utils.load_processor(model_path='saved_model/bilstm/1')
    tensor = processor.process_x_dataset([list(text)])
    json_data = {"model_name": "default", "data": {"input:0": tensor.tolist()}}
    result = requests.post(endpoint, json=json_data)
    preds = dict(result.json())['dense/Softmax:0']
    label_index = np.array(preds).argmax(-1)
    labels = processor.reverse_numerize_label_sequences(label_index)
    print(labels)


if __name__ == "__main__":
    main()

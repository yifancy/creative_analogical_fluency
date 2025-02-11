import numpy as np
import requests


def deal_with_response(word: str):
    url = 'http://127.0.0.1:8000/word_vector?word=' + word
    res1 = requests.get(url)
    res_json = res1.json()
    if res_json['code'] == 200:
        word_vector = res_json['vector']
        print('请求成功 word：' + res_json['word'])
        word_vector = np.array(word_vector)
        return word_vector
    else:
        return res_json['error']


if __name__ == '__main__':
    deal_with_response('悔改')

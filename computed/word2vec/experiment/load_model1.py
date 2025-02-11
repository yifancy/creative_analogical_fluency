import pandas as pd
from gensim.models import KeyedVectors

word2vec_model = None


def load_word2vec_model():
    global word2vec_model
    if word2vec_model is None:
        word2vec_model = KeyedVectors.load('D:/analogy_models/word2vec/tencent_word2vec.wv')
        # D:/analogy_models/word2vec/tencent-ailab-embedding-zh-d200-v0.2.0
        # word2vec_model = KeyedVectors.load_word2vec_format(
        #     'D:/analogy_models/word2vec/tencent-ailab-embedding-zh-d200-v0.2.0/tencent-ailab-embedding-zh-d200-v0.2.0'
        #     '.txt', binary=False)
        a = word2vec_model['皇帝']
        a = word2vec_model['男人']
        c = word2vec_model.similarity('女王', '女人')
        # print(word2vec_model['赞同'])
        print(c)


def load_data(path: str = 'D:/analogy_models/bert/词类比题目v0.2.1.xlsx'):
    df = pd.read_excel(path)
    all_data = []
    for row in df.values:
        data1 = row[1: 5]
        all_data.append(data1)
    return all_data, df


if __name__ == '__main__':
    load_word2vec_model()

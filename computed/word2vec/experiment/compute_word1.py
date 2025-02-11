import numpy as np
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity as cos


def load_data(path: str = 'D:/analogy_models/bert/词类比题目v0.3.3_2.xlsx'):
    df = pd.read_excel(path)
    all_data = []
    for row in df.values:
        data1 = row[1: 5]
        all_data.append(data1)
    return all_data, df


def deal_with_response(word: str):
    url = 'http://127.0.0.1:8000/word_vector?word=' + word
    res1 = requests.get(url)
    res_json = res1.json()
    if res_json['code'] == 200:
        word_vector = res_json['vector']
        # print('请求成功 word：' + res_json['word'])
        word_vector = np.array(word_vector).reshape(1, -1)
        return word_vector
    else:
        return res_json['error']


def compute_cos1(word_pairs: list, estimate_word: str):
    """
    计算词对余弦相似度
    :param word_pairs: 词对列表，需要传入3个词
    :param estimate_word: 需要评估的词
    :return: 余弦相似度 取值范围：[-1,1] 越靠近1越大，越相似，反之亦然
    """
    # 初始化Bert客户端
    # bc = BertClient(ip='192.168.1.105', port=5555, port_out=5556, show_server_config=False, timeout=100000)
    vector_list = []
    for word in word_pairs:
        vector1 = deal_with_response(word)
        if not isinstance(vector1, str):
            vector_list.append(vector1)
        else:
            # vector_list.append(float())
            print(vector1)
            vector_list.append(np.zeros((1, 200)))

    estimate_word_vector = deal_with_response(estimate_word)
    # 传入： 国王：男人：：皇后：___
    # 国王 - 男人 = 皇后 - 女人
    # 皇后 = 国王 - 男人 + 女人

    # 女人 = 皇后 - （国王 - 男人）
    # compute_result = vector_list[0] - vector_list[1] + vector_list[2]
    compute_result = vector_list[2] - (vector_list[0] - vector_list[1])

    # 计算余弦相似度
    if not isinstance(estimate_word_vector, str):
        cos_result = cos(estimate_word_vector, compute_result)[0][0]
        return cos_result
    else:
        return float(-1)


def word2vec_compute_cos2(word_pairs: list, estimate_words: list):
    """
    计算词对余弦相似度，考虑到多传入值
    :param word_pairs:
    :param estimate_words:
    :return: 回传最大值的索引以及对应的评估值
    """
    # vector_list = []
    # for word in word_pairs:
    #     vector_list.append(bc.encode([word]))
    estimate_words_result = []
    # estimate_word_vector = bc.encode([estimate_word])

    # 去重
    estimate_words = list(set(estimate_words))
    new_estimate_words = []
    for old_word in estimate_words:
        new_word = old_word.replace(' ', '')
        new_estimate_words.append(new_word)
    for es_word in new_estimate_words:
        estimate_words_result.append(compute_cos1(word_pairs, es_word))
    # 传入： 国王：男人：：皇后：___
    # 国王 - 男人 = 皇后 - 女人
    # 皇后 = 国王 - 男人 + 女人

    # 女人 = 皇后 - （国王 - 男人）
    # compute_result = vector_list[0] - vector_list[1] + vector_list[2]
    max_score = max(estimate_words_result)
    best_word_index = estimate_words_result.index(max_score)
    best_word = new_estimate_words[best_word_index]
    # 关闭bert连接
    # bc.close()
    return best_word, max_score


def compute_dis1(word_pairs: list, estimate_word: str):
    """
    使用bert计算欧氏距离
    :param word_pairs:
    :param estimate_word:
    :return:
    """
    vector_list = []
    for word in word_pairs:
        vector1 = deal_with_response(word)
        if not isinstance(vector1, str):
            vector_list.append(vector1)
        else:
            # vector_list.append(float())
            print(vector1)
            vector_list.append(np.zeros((1, 200)))
    estimate_word_vector = deal_with_response(estimate_word)
    # 传入： 国王：男人：：皇后：___
    # 国王 - 男人 = 皇后 - 女人
    # 皇后 = 国王 - 男人 + 女人

    # 女人 = 皇后 - （国王 - 男人）
    compute_result = vector_list[2] - (vector_list[0] - vector_list[1])
    # print(estimate_word_vector)
    # 计算欧氏距离
    if isinstance(estimate_word_vector, str):
        return float(100), vector_list
    distance1 = np.linalg.norm(estimate_word_vector - compute_result)
    return distance1, vector_list


def word2vec_compute_dis2(word_pairs: list, estimate_words: list):
    estimate_words_result = []
    # 去重
    estimate_words = list(set(estimate_words))
    new_estimate_words = []
    for old_word in estimate_words:
        new_word = old_word.replace(' ', '')
        new_estimate_words.append(new_word)
    for es_word in new_estimate_words:
        estimate_words_result.append(compute_dis1(word_pairs, es_word)[0])
    # 获取最小值
    min_val = min(estimate_words_result)
    best_word_index = estimate_words_result.index(min_val)
    best_word = new_estimate_words[best_word_index]
    return best_word, min_val


def deal_with_data():
    data1, df = load_data()
    cosine_list = []
    cosine_score_list = []
    dis_list = []
    dis_score_list = []
    for row in data1:
        # print(row)
        estimate_list = row[3].split('/')
        best_word1, similarity = word2vec_compute_cos2([row[0], row[1], row[2]], estimate_list)
        best_word2, min_score = word2vec_compute_dis2([row[0], row[1], row[2]], estimate_list)
        # 余弦相似度
        cosine_list.append(best_word1)
        cosine_score_list.append(similarity)
        print(best_word1, similarity)

        # 欧氏距离
        dis_list.append(best_word2)
        dis_score_list.append(min_score)
        print(best_word2, min_score)
        print('===========')
    df['word2vec_cosine_similarity'] = cosine_score_list
    df['word2vec_cosine_word'] = cosine_list

    df['word2vec_distance_similarity'] = dis_score_list
    df['word2vec_distance_word'] = dis_list
    df.to_excel('词类比题目v0.3.3_3.xlsx', index=False)


if __name__ == '__main__':
    # print(deal_with_response('陶瓷'))
    deal_with_data()

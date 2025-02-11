import re

import numpy as np
import pandas as pd
from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity as cos

try:
    bc = BertClient(ip='127.0.0.1', port=5555, port_out=5556, show_server_config=False, timeout=1000,
                    check_version=False)
except Exception as e:
    print(e.args)


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
        vector_list.append(bc.encode([word]))

    estimate_word_vector = bc.encode([estimate_word])
    # 传入： 国王：男人：：皇后：___
    # 国王 - 男人 = 皇后 - 女人
    # 皇后 = 国王 - 男人 + 女人

    # 女人 = 皇后 - （国王 - 男人）
    # compute_result = vector_list[0] - vector_list[1] + vector_list[2]
    compute_result = vector_list[2] - (vector_list[0] - vector_list[1])

    # 计算余弦相似度
    cos_result = cos(estimate_word_vector, compute_result)[0][0]
    return cos_result


def bert_compute_cos2(word_pairs: list, estimate_words: list):
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


def compute_cos3(word_pairs: list, estimate_words: str):
    vector_list = []
    for word in word_pairs:
        if '/' in word:
            word_list = word.split('/')
            for i in word_list:
                vector_list.append(bc.encode([i]))


def compute_dis1(word_pairs: list, estimate_word: list):
    """
    使用bert计算欧氏距离
    :param word_pairs:
    :param estimate_word:
    :return:
    """
    vector_list = []
    for word in word_pairs:
        vector_list.append(bc.encode([word]))
    estimate_word_vector = bc.encode([estimate_word])
    # 传入： 国王：男人：：皇后：___
    # 国王 - 男人 = 皇后 - 女人
    # 皇后 = 国王 - 男人 + 女人

    # 女人 = 皇后 - （国王 - 男人）
    compute_result = vector_list[2] - (vector_list[0] - vector_list[1])
    # 计算欧氏距离
    distance1 = np.linalg.norm(estimate_word_vector - compute_result)
    return distance1, vector_list


def bert_compute_dis2(word_pairs: list, estimate_words: list):
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


def load_data(file_path: str = '../../词类比题目v1.0.0.xlsx'):
    df = pd.read_excel(file_path)
    cosine_list = []
    cosine_score_list = []
    dis_list = []
    dis_score_list = []
    for row in df.values:
        # 对每一行数据进行处理
        estimate_list = row[5].split('/')
        estimate_list = process_data(estimate_list)
        best_word1, similarity = bert_compute_cos2([row[1], row[2], row[3]], estimate_list)
        best_word2, min_score = bert_compute_dis2([row[1], row[2], row[3]], estimate_list)
        # 余弦相似度
        cosine_list.append(best_word1)
        cosine_score_list.append(similarity)
        print(best_word1, similarity)

        # 欧氏距离
        dis_list.append(best_word2)
        dis_score_list.append(min_score)
        print(best_word2, min_score)
        print('===========')
    df['bert_cosine_similarity'] = cosine_score_list
    df['bert_cosine_word'] = cosine_list

    df['bert_distance_similarity'] = dis_score_list
    df['bert_distance_word'] = dis_list
    df.to_excel('词类比题目v1.0.0_2.xlsx', index=False)


def process_data(word_list: list):
    adv_mark = 0
    adj_mark = 0
    processed_list1 = []
    processed_list2 = []

    for word in word_list:
        if '的' in word:
            adj_mark += 1
        if '地' in word:
            adv_mark += 1
    if adv_mark == 0 and adj_mark != 0:
        for word in word_list:
            if '的' in word:
                word = word.replace('的', '')
                processed_list1.append(word)
            else:
                processed_list1.append(word)
    else:
        processed_list1 = word_list
    pattern = re.compile(r'[^\u4e00-\u9fa5]')

    for word in processed_list1:
        string = re.sub(pattern, '', word)
        processed_list2.append(string)
    return processed_list2


if __name__ == '__main__':
    # print(compute_cos(['国王', '男人', '皇后'], '女人'))
    # print(compute_cos1(['曼谷', '泰国', '北京'], '中国'))
    # print(compute_cos1(['康德', '哲学家', '贝多芬'], '音乐家'))
    # print(compute_cos1(['康德', '哲学家', '贝多芬'], '作曲家'))
    # print(compute_cos2(['康德', '哲学家', '贝多芬'], ['作 曲家', '音 乐家', '怪物 ']))
    load_data()

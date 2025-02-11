import random

import numpy as np
from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity as cos
from db.insert_data import init_db
import requests


# try:
#     bc = BertClient(ip='127.0.0.1', port=5555, port_out=5556, show_server_config=False, timeout=1000,
#                     check_version=False)
# except Exception as e:
#     print(e.args)


# def bert_compute(word_list: list, estimate_word: str):
#     vector_list = []
#     for word in word_list:
#         vector_list.append(bc.encode([word]))
#
#     estimate_word_vector = bc.encode([estimate_word])
#     # 传入： 国王：男人：：皇后：___
#     # 国王 - 男人 = 皇后 - 女人
#     # 皇后 = 国王 - 男人 + 女人
#
#     # 女人 = 皇后 - （国王 - 男人）
#     # compute_result = vector_list[0] - vector_list[1] + vector_list[2]
#     compute_result = vector_list[2] - (vector_list[0] - vector_list[1])


def bert_compute2():
    conn, cursor = init_db()
    questionare_data_sql = "select id, question, answer, bert_euc, bert_cos, word2vec_euc, word2vec_cos from questionare_data_model;"
    row_num = cursor.execute(questionare_data_sql)
    res_data1 = cursor.fetchall()
    for row in res_data1:
        ques_id, question, subject_answer, bert_euc, bert_cos, word2vec_euc, word2vec_cos = row
        q1 = question.split(' ')[1]
        q2 = q1.find('→')
        q3 = q1.find('::')
        word1 = q1[:q2]
        word2 = q1[q2 + 1: q3]
        print('=========*===========')
        select_sql1 = "select * from pre_map where (word1 = '%s' and word2 = '%s');" % (word1, word2)
        cursor.execute(select_sql1)
        res_data2 = cursor.fetchone()
        bert_cos2, bert_euc2, word2vec_cos2, word2vec_euc2 = res_data2[8: 12]
        bert_word1, bert_word2 = res_data2[12: 14]
        word2vec_word1, word2vec_word2 = res_data2[14: 16]
        bert_cos = float(bert_cos)
        word2vec_cos = float(word2vec_cos)
        word4 = res_data2[4]
        print(res_data2)
        # 主逻辑判断 bert
        if float(bert_euc) <= bert_euc2:
            # bert_score = 2
            bert_score = 1
        else:
            # bert_score = float(bert_cos) + 1
            if bert_cos < 0:
                bert_score = 0
            else:
                bert_score = bert_cos

        # 主逻辑2 (单选题)
        # if subject_answer == bert_word1 or subject_answer == bert_word2:
        #     bert_score2 = 1
        # else:
        #     bert_score2 = 0
        answer_list = word4.split('/')
        test_list = split_word(subject_answer)
        bert_score2 = 0
        for i in answer_list:
            for j in test_list:
                if i == j:
                    bert_score2 = 1

        # 主逻辑判断 word2vec
        if float(word2vec_euc) <= word2vec_euc2:
            word2vec_score = 1
        else:
            if word2vec_cos < 0:
                word2vec_score = 0
            else:
                word2vec_score = word2vec_cos

        # 主逻辑2
        # if subject_answer == word2vec_word1 or subject_answer == word2vec_word2:
        #     word2vec_score2 = 1
        # else:
        #     word2vec_score2 = 0
        word2vec_score2 = 0
        for i in answer_list:
            for j in test_list:
                if i == j:
                    word2vec_score2 = 1

        update_sql = ("update questionare_data_model set bert_score = %s, word2vec_score = %s, bert_score2 = %s, "
                      "word2vec_score2 = %s where id = %s;") % (
                         bert_score2, word2vec_score2, bert_score, word2vec_score, ques_id)
        print(update_sql)
        cursor.execute(update_sql)
    conn.commit()
    conn.close()


def gpt_compute():
    conn, cursor = init_db()
    # pre_map
    subject_list_sql = "select id, word1, word2, word3, estimate_word from pre_map;"
    cursor.execute(subject_list_sql)
    words_res = cursor.fetchall()
    for _ in words_res:
        subject_id = _[0]
        words_list = _[1: 4]
        estimate_word = _[-1]
        vector_list = []
        for word in words_list:
            find_word_sql = "select * from word_embedding where word = '%s';" % word
            cursor.execute(find_word_sql)
            word_res = cursor.fetchone()
            if word_res is None:
                print(subject_id, word)
                url = 'http://192.168.1.112:8000/gpt?word={}'.format(word)
                res = requests.get(url)
                res_json = res.json()
                if res_json['code'] == 200:
                    word_vector = res_json['vector']
                    update_sql = "insert into word_embedding (word, embedding) values ('%s', '%s');" % (
                        word, word_vector)
                    print(update_sql)
                    cursor.execute(update_sql)
                    conn.commit()
        if '/' in estimate_word:
            word_list = estimate_word.split('/')
            for i in word_list:
                estimate_vector = "select * from word_embedding where word = '%s';" % i
                cursor.execute(estimate_vector)
                res1 = cursor.fetchone()
                if res1 is None:
                    url = 'http://192.168.1.112:8000/gpt?word={}'.format(i)
                    res = requests.get(url)
                    res_json = res.json()
                    if res_json['code'] == 200:
                        word_vector = res_json['vector']
                        update_sql = "insert into word_embedding (word, embedding) values ('%s', '%s');" % (
                            i, word_vector)
                        print(update_sql)
                        cursor.execute(update_sql)
                        conn.commit()
        if '/' not in estimate_word:
            estimate_vector = "select * from word_embedding where word = '%s';" % estimate_word
            cursor.execute(estimate_vector)
            res2 = cursor.fetchone()
            if res2 is None:
                url = 'http://192.168.1.112:8000/gpt?word={}'.format(estimate_word)
                res = requests.get(url)
                res_json = res.json()
                if res_json['code'] == 200:
                    word_vector = res_json['vector']
                    update_sql = "insert into word_embedding (word, embedding) values ('%s', '%s');" % (
                        estimate_word, word_vector)
                    print(update_sql)
                    cursor.execute(update_sql)
                    conn.commit()
    # model


def gpt_compute2():
    conn, cursor = init_db()
    # pre_map
    subject_list_sql = "select id, word1, word2, word3, estimate_word from pre_map;"
    cursor.execute(subject_list_sql)
    words_res = cursor.fetchall()
    for _ in words_res:
        subject_id = _[0]
        words_list = _[1: 4]
        estimate_word = _[-1]
        vector_list = []
        for word in words_list:
            find_word_sql = "select * from word_embedding where word = '%s';" % word
            cursor.execute(find_word_sql)
            word_res = cursor.fetchone()
            vector = eval(word_res[2])
            vector = np.array(vector)
            vector_list.append(vector)
        if '/' in estimate_word:
            word_list = estimate_word.split('/')
            dis_list = []
            cos_list = []
            for i in word_list:
                find_word_sql2 = "select * from word_embedding where word = '%s';" % i
                cursor.execute(find_word_sql2)
                word_res2 = cursor.fetchone()
                vector_ = eval(word_res2[2])
                vector_ = np.array(vector_)
                answer_vector, dis, cosine = general_compute(vector_list, vector_)
                dis_list.append(dis)
                cos_list.append(cosine)

            min_dis = dis_list.index(min(dis_list))
            min_dis_word = word_list[min_dis]
            max_cos = cos_list.index(max(cos_list))
            max_cos_word = word_list[max_cos]
            update_sql1 = "update pre_map set gpt_cosine_word = '%s', gpt_distance_word = '%s', gpt_cosine_similarity = %s, gpt_distance_similarity = %s where id = %s;" % (
                max_cos_word, min_dis_word, max(cos_list), min(dis_list), subject_id)
            print(update_sql1)
            cursor.execute(update_sql1)
            conn.commit()
        if '/' not in estimate_word:
            find_word_sql2 = "select * from word_embedding where word = '%s';" % estimate_word
            cursor.execute(find_word_sql2)
            word_res3 = cursor.fetchone()
            vector = eval(word_res3[2])
            vector = np.array(vector)
            answer_vector, dis, cosine = general_compute(vector_list, vector)
            update_sql2 = "update pre_map set gpt_cosine_word = '%s', gpt_distance_word = '%s', gpt_cosine_similarity = %s, gpt_distance_similarity = %s where id = %s;" % (
                estimate_word, estimate_word, cosine, dis, subject_id)
            print(update_sql2)
            cursor.execute(update_sql2)
            conn.commit()
    conn.close()


def general_compute(word_list: list, estimate_word: list):
    word1, word2, word3 = word_list
    # 传入： 国王：男人：：皇后：___
    # 国王 - 男人 = 皇后 - 女人
    # 皇后 = 国王 - 男人 + 女人

    # 女人 = 皇后 - （国王 - 男人）
    answer_vector = word3 - (word1 - word2)
    # 欧式距离
    dis = np.linalg.norm(estimate_word - answer_vector)
    cosine = cos(estimate_word.reshape(1, -1), answer_vector.reshape(1, -1))[0][0]
    return answer_vector, dis, cosine


def general_compute2(word_list: list, estimate_word: str):
    conn, cursor = init_db()
    vector_list = []
    for word in word_list:
        find_word_sql = "select * from word_embedding where word = '%s';" % word
        cursor.execute(find_word_sql)
        res1 = cursor.fetchone()
        vector = eval(res1[2])
        vector = np.array(vector)
        vector_list.append(vector)
    estimate_word_list = split_word(estimate_word)

    answer_vec_list = []
    dis_list = []
    cos_list = []
    for word in estimate_word_list:
        find_word_sql2 = "select * from word_embedding where word = '%s';" % word
        cursor.execute(find_word_sql2)
        res2 = cursor.fetchone()

        estimate_vector = eval(res2[2])
        estimate_vector = np.array(estimate_vector)
        # 传入： 国王：男人：：皇后：___
        # 国王 - 男人 = 皇后 - 女人
        # 皇后 = 国王 - 男人 + 女人

        # 女人 = 皇后 - （国王 - 男人）
        answer_vector = vector_list[2] - (vector_list[0] - vector_list[1])
        answer_vec_list.append(answer_vector)
        # 欧式距离
        distance = np.linalg.norm(estimate_vector - answer_vector)
        dis_list.append(distance)
        # 余弦相似度
        cosine = cos(estimate_vector.reshape(1, -1), answer_vector.reshape(1, -1))[0][0]
        cos_list.append(cosine)

    return answer_vec_list, dis_list, cos_list


def insert_word():
    conn, cursor = init_db()
    sql1 = "select answer from questionare_data_model;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    for _ in res1:
        words = split_word(_[0])
        words2 = [x for x in words if x != '']
        print(words2)
        for word in words2:
            sql2 = "select * from word_embedding where word = '%s';" % word
            cursor.execute(sql2)
            res2 = cursor.fetchone()
            if res2 is None:
                url = 'http://192.168.1.112:8000/gpt?word={}'.format(word)
                res = requests.get(url)
                res_json = res.json()
                if res_json['code'] == 200:
                    word_vector = res_json['vector']
                    update_sql = "insert into word_embedding (word, embedding) values ('%s', '%s');" % (
                        word, word_vector)
                    print(update_sql)
                    cursor.execute(update_sql)
                    conn.commit()


def insert_word2():
    conn, cursor = init_db()
    sql1 = "select word1,word2, word3, word4 from pre_map;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    for _ in res1:
        for i in _:
            words = split_word(i)
            words2 = [x for x in words if x != '']
            print(words2)
            for word in words2:
                sql2 = "select * from word_embedding where word = '%s';" % word
                cursor.execute(sql2)
                res2 = cursor.fetchone()
                if res2 is None:
                    url = 'http://192.168.1.112:8000/gpt?word={}'.format(word)
                    res = requests.get(url)
                    res_json = res.json()
                    if res_json['code'] == 200:
                        word_vector = res_json['vector']
                        update_sql = "insert into word_embedding (word, embedding) values ('%s', '%s');" % (
                            word, word_vector)
                        print(update_sql)
                        cursor.execute(update_sql)
                        conn.commit()
    conn.close()


def split_word(my_chinese_string: str):
    # 定义更全面的中文标点符号
    chinese_punctuation = "，。！？；：、~·@#￥%……&*（）——+=【】｛｝|、：‘’“”《》<>「」『』【】〖〗［］〔〕﹁﹂﹃﹄﹏﹋﹌﹍﹎﹏﹐﹑﹒﹔﹕﹖﹗﹘﹙﹚﹛﹜﹝﹞﹟﹠﹡﹢﹣﹤﹥﹦﹨﹩﹪﹫＋/"

    # 示例中文字符串
    # my_chinese_string = "你好，世界！这是一个示例句子。"

    # 获取中文字符串中标点符号的索引
    punctuation_indices = [index for index, char in enumerate(my_chinese_string) if char in chinese_punctuation]

    # 根据标点符号的索引分割词语
    start = 0
    segments = []
    for idx in punctuation_indices:
        segments.append(my_chinese_string[start:idx])
        start = idx + 1
    segments.append(my_chinese_string[start:])
    segments2 = [x for x in segments if x != '']

    return segments2

    # print("分割后的词语:", segments)


def gpt_compute3():
    conn, cursor = init_db()
    # model
    sql1 = "select id, question, answer from questionare_data_model;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    for _ in res1:
        tb_id, question, answer = _
        q1 = question.split(' ')[1]
        q2 = q1.find('→')
        q3 = q1.find('::')
        word1 = q1[:q2]
        word2 = q1[q2 + 1: q3]
        select_sql1 = "select id, word1, word2, word3, word4, gpt_cosine_word, gpt_distance_word, gpt_cosine_similarity, gpt_distance_similarity from pre_map where (word1 = '%s' and word2 = '%s');" % (
            word1, word2)
        cursor.execute(select_sql1)
        res_data2 = cursor.fetchone()
        word_list = res_data2[1: 4]
        word4 = res_data2[4]
        subject_id = res_data2[0]
        gpt_cos, gpt_dis = res_data2[7:]
        answer_vec_list, dis_list, cos_list = general_compute2(word_list, answer)
        min_val = min(dis_list)
        min_val_index = dis_list.index(min_val)
        min_answer = answer_vec_list[min_val_index]

        max_val = max(cos_list)
        max_val_index = cos_list.index(max_val)
        max_answer = answer_vec_list[max_val_index]

        # 逻辑判断1
        if gpt_dis >= min_val:
            score2 = 1
            best_word2 = min_answer
        else:
            if max_val < 0:
                score2 = 0
                best_word2 = max_answer
            else:
                score2 = max_val
                best_word2 = max_answer

        # 单选题
        answer_list = word4.split('/')
        test_list = split_word(answer)
        score1 = 0
        for i in answer_list:
            for j in test_list:
                if i == j:
                    score1 = 1

        update_sql1 = "update questionare_data_model set gpt_euc = '%s', gpt_cos = '%s', gpt_score = %s, gpt_score2 = %s where id = %s;" % (
            min_val, max_val, score1, score2, tb_id)
        print(update_sql1)
        cursor.execute(update_sql1)
    conn.commit()
    conn.close()


def judge_score():
    conn, cursor = init_db()
    sql1 = "select id, score3, score4 from questionare_data_human;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    for _ in res1:
        tb_id, score3, score4 = _
        average_score = (score3 + score4) / 2
        sql2 = "update questionare_data_human set final_score2 = %s where id = %s;" % (average_score, tb_id)
        print(sql2)
        cursor.execute(sql2)
    conn.commit()
    conn.close()


def renew_info_id():
    conn, cursor = init_db()
    sql1 = "select id from questionare_data_human;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    mark = 1
    for _ in res1:
        tb_id = _[0]

        sql2 = "update questionare_data_human set info_id = %s where id = %s;" % (mark, tb_id)
        sql3 = "update questionare_data_model set info_id = %s where id = %s;" % (mark, tb_id)
        cursor.execute(sql2)
        cursor.execute(sql3)
        if tb_id % 60 == 0:
            mark += 1
    conn.commit()
    conn.close()


# def test1():
#     url = 'http://20.38.1.79:8000/api/generate'
#     api_key = suijiapikey()
#     data = {
#         'prompt': system_prompt,
#         'history': user_prompt,
#         'apikey': api_key,
#         'model': 'gpt-3.5-turbo-16k',
#     }
#     res = requests.post(url, data=data)
#
#
# def suijiapikey():
#     db = pymysql.connect(host="8.138.1.108", user="yyy", port=20308, password="wcaM6zg4532e",
#                          database="goc_test",
#                          charset="utf8mb4")
#
#     sql = "select apikey from `gpt_api_key`"
#     cursor = db.cursor()
#     cursor.execute(sql)
#     rs = cursor.fetchall()
#     api_list = []
#     for api in rs:
#         api_list.append(api[0])
#     apikey = random.choice(api_list)
#     return apikey
def map_score(score):
    if score == 0.0:
        return 0.0
    elif 0.0 < score <= 0.2:
        return 1.0
    elif 0.2 < score <= 0.4:
        return 2.0
    elif 0.4 < score <= 0.6:
        return 3.0
    elif 0.6 < score <= 0.8:
        return 4.0
    elif 0.8 < score <= 1.0:
        return 5.0


def rejudge_origin():
    conn, cursor = init_db()
    query_sql1 = "select id, question, answer, bert_score2, word2vec_score2, gpt_score2 from questionare_data_model2;"
    cursor.execute(query_sql1)
    res1 = cursor.fetchall()
    for _ in res1:
        tb_id, question, answer, bert_score2, word2vec_score2, gpt_score2 = _
        update_sql = ("update questionare_data_model2 set bert_ori_score = %s, word2vec_ori_score = %s, gpt_ori_score ="
                      "%s where id = %s;") % (
                         map_score(bert_score2), map_score(word2vec_score2), map_score(gpt_score2), tb_id)
        print(update_sql)
        cursor.execute(update_sql)
    conn.commit()
    cursor.close()
    conn.close()


def rejudge_origin2():
    conn, cursor = init_db()
    query_sql1 = "select id, question, answer, bert_score2, word2vec_score2, gpt_score2 from questionare_data_model2 where answer = '空';"
    cursor.execute(query_sql1)
    res1 = cursor.fetchall()
    for _ in res1:
        tb_id, question, answer, bert_score2, word2vec_score2, gpt_score2 = _
        update_sql = "update questionare_data_model2 set bert_score2 = 0, word2vec_score2 = 0, gpt_score2 = 0, bert_fluency_score = 0, word2vec_fluency_score = 0, gpt_fluency_score = 0, bert_ori_score = 0, word2vec_ori_score = 0, gpt_ori_score = 0 where id = %s;" % tb_id
        update_sql2 = "update questionare_data_human set score3 = 0, score4 = 0, final_score2 = 0, fluency_score = 0 where id = %s;" % tb_id
        print(update_sql)
        print(update_sql2)
        cursor.execute(update_sql)
        cursor.execute(update_sql2)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    # bert_compute2()
    # gpt_compute2()
    # insert_word2()
    # gpt_compute3()
    # judge_score()
    # renew_info_id()
    rejudge_origin2()

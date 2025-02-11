# from bert.similarity_algorithm1_for_bert import bert_compute_cos2, bert_compute_dis2
import re
import pandas as pd
from computed.bert.similarity_algorithm1_for_bert import *
from db.insert_data import init_db
from computed.word2vec.experiment.compute_word1 import *


def compute_all():
    """
    词类比核心处理函数
    :return:
    """
    conn, cursor = init_db()
    questionare_data_sql = "select id, question, answer from questionare_data_model;"
    row_num = cursor.execute(questionare_data_sql)
    res_data1 = cursor.fetchall()
    for row in res_data1:
        ques_id, question, subject_answer = row
        q1 = question.split(' ')[1]
        q2 = q1.find('→')
        q3 = q1.find('::')
        word1 = q1[:q2]
        word2 = q1[q2 + 1: q3]
        print('=========*===========')
        select_sql1 = "select * from pre_map where (word1 = '%s' and word2 = '%s');" % (word1, word2)
        cursor.execute(select_sql1)
        res_data2 = cursor.fetchone()
        print(res_data2)
        pre_map_id = res_data2[0]
        kind_id = res_data2[7]
        # 三个词 word123
        words = list(res_data2[1: 4])

        scores = list(res_data2[8: 12])
        bert_cosine_similarity, bert_distance_similarity, word2vec_cosine_similarity, word2vec_distance_similarity = scores
        # 计算Bert
        # bert_mark1 = -1
        # bert_mark2 = -1
        bert_cos = bert_compute_cos2(words, [subject_answer])[1]
        if bert_cos >= bert_cosine_similarity:
            bert_mark1 = 1
        else:
            bert_mark1 = 0
        bert_dis = bert_compute_dis2(words, [subject_answer])[1]
        if bert_dis <= bert_distance_similarity:
            bert_mark2 = 1
        else:
            bert_mark2 = 0

        # 计算word2vec
        # word2vec_mark1 = -1
        # word2vec_mark2 = -1
        # 处理符号 以及 去掉
        words = process_data(words)
        change_word = process_data([subject_answer])
        word2vec_cos = word2vec_compute_cos2(words, change_word)[1]
        if word2vec_cos >= word2vec_cosine_similarity:
            word2vec_mark1 = 1
        else:
            word2vec_mark1 = 0

        word2vec_dis = word2vec_compute_dis2(words, change_word)[1]
        if word2vec_dis <= word2vec_distance_similarity:
            word2vec_mark2 = 1
        else:
            word2vec_mark2 = 0

        # 计算gpt
        update_sql1 = "update questionare_data_model set bert_cos = %s, bert_euc = %s, bert_cos_score = %s, bert_euc_score = %s, word2vec_cos = %s, word2vec_euc = %s, word2vec_cos_score = %s, word2vec_euc_score = %s, kind = %s where id = %s;" % (
            bert_cos, bert_dis, bert_mark1, bert_mark2, word2vec_cos, word2vec_dis, word2vec_mark1, word2vec_mark2,
            kind_id,
            ques_id)
        print(update_sql1)
        cursor.execute(update_sql1)

        # 对人工审核表的种类也进行分类
        update_sql2 = "update questionare_data_human set kind = %s where id = %s" % (kind_id, ques_id)
        cursor.execute(update_sql2)
        print('进度： {:.4f}'.format(ques_id / row_num))
    conn.commit()
    cursor.close()
    conn.close()


def judge_human_score():
    conn, cursor = init_db()
    # 先实现打分逻辑
    select_human_sql = "select * from questionare_data_human;"
    cursor.execute(select_human_sql)
    res_data1 = cursor.fetchall()
    for row in res_data1:
        question_id = row[0]
        # scores = row[-4:-1]
        scores = row[-4:-2]
        scores = list(scores)
        try:

            # if sum(scores) >= 2:
            if sum(scores) == 2:
                final_score = 1
            else:
                final_score = 0
            update_final_score_sql = "update questionare_data_human set final_score = %s where id = %s;" % (
                final_score, question_id)
            cursor.execute(update_final_score_sql)
        except Exception as e:
            print(e)
            print('评分失败，可能原因：1 未完成评分 2 程序出错')
            break
    conn.commit()
    print('人工评分统计结束，请查看 questionare_data_human -> final_score')


def merge_data():
    conn, cursor = init_db()
    name_list = []
    question_list = []
    human_list = []
    answer_list = []

    bert_euc_score_list = []
    bert_cos_score_list = []
    word2vec_euc_score_list = []
    word2vec_cos_score_list = []
    gpt_euc_score_list = []
    gpt_cos_score_list = []

    select_human_by_kind_sql1 = "select name, question, answer, final_score from questionare_data_human;"
    cursor.execute(select_human_by_kind_sql1)
    res_data1 = cursor.fetchall()
    for row in res_data1:
        name, question, answer, final_score = row
        name_list.append(name)
        question_list.append(question)
        answer_list.append(answer)
        human_list.append(final_score)

    select_model_sql = "select name, bert_euc_score, bert_cos_score, word2vec_euc_score, word2vec_cos_score, gpt_euc_score, gpt_cos_score from questionare_data_model;"
    cursor.execute(select_model_sql)
    res_data2 = cursor.fetchall()
    for row in res_data2:
        bert_euc_score, bert_cos_score, word2vec_euc_score, word2vec_cos_score, gpt_euc_score, gpt_cos_score = row[1::]
        if gpt_cos_score is not None:
            gpt_euc_score_list.append(gpt_euc_score)
            gpt_cos_score_list.append(gpt_cos_score)
        bert_euc_score_list.append(bert_euc_score)
        bert_cos_score_list.append(bert_cos_score)
        word2vec_euc_score_list.append(word2vec_euc_score)
        word2vec_cos_score_list.append(word2vec_cos_score)
    if len(gpt_euc_score_list) == 0:
        all_data = {
            'name': name_list,
            'question': question_list,
            'answer': answer_list,
            'human': human_list,
            'bert_euc_score': bert_euc_score_list,
            'bert_cos_score': bert_cos_score_list,
            'word2vec_euc_score': word2vec_euc_score_list,
            'word2vec_cos_score': word2vec_cos_score_list,

        }
        df = pd.DataFrame(all_data)
        df.to_excel('./outputs/词类比总表.xlsx', index=False)
    else:
        all_data = {
            'name': name_list,
            'question': question_list,
            'answer': answer_list,
            'human': human_list,
            'bert_euc_score': bert_euc_score_list,
            'bert_cos_score': bert_cos_score_list,
            'word2vec_euc_score': word2vec_euc_score_list,
            'word2vec_cos_score': word2vec_cos_score_list,
            'gpt_euc_score': gpt_euc_score_list,
            'gpt_cos_score': gpt_cos_score_list,

        }
        df = pd.DataFrame(all_data)
        # df.to_excel('./outputs/词类比总表.xlsx', index=True, index_label='id')
        df.to_excel('./outputs/词类比总表.xlsx', index=False)
    print('=======>')
    print('总表已导出，请查看 outputs目录')


def merge_data_by_class():
    conn, cursor = init_db()
    # 先实现打分逻辑
    # select_human_sql = "select * from questionare_data_human;"
    # res_data1 = cursor.execute(select_human_sql)
    # for row in res_data1:
    #     question_id = row[0]
    #     scores = row[-4:-1]
    #     scores = list(scores)
    #     if sum(scores) >= 2:
    #         final_score = 1
    #     else:
    #         final_score = 0
    #     update_final_score_sql = "update questionare_data_human set final_score = %s where id = %s;" % (
    #         final_score, question_id)
    #     cursor.execute(update_final_score_sql)
    # conn.commit()
    # 人工表分组 0:语义 1:语法
    name_list1 = []
    name_list2 = []
    answer_list1 = []
    answer_list2 = []
    question_list1 = []
    question_list2 = []
    semantics_list = []
    grammar_list = []
    select_human_by_kind_sql1 = "select name, question, answer, final_score from questionare_data_human where kind = 0;"
    cursor.execute(select_human_by_kind_sql1)
    kind_data1 = cursor.fetchall()
    for row in kind_data1:
        name, question, answer, final_score = row
        name_list1.append(name)
        semantics_list.append(final_score)
        question_list1.append(question)
        answer_list1.append(answer)
    select_human_by_kind_sql2 = "select name, question, answer, final_score from questionare_data_human where kind = 1;"
    cursor.execute(select_human_by_kind_sql2)
    kind_data2 = cursor.fetchall()
    for row in kind_data2:
        name, question, answer, final_score = row
        name_list2.append(name)
        question_list2.append(question)
        grammar_list.append(final_score)
        answer_list2.append(answer)

    # 模型表分组 0:语义 1:语法
    bert_euc_score_list1 = []
    bert_euc_score_list2 = []
    bert_cos_score_list1 = []
    bert_cos_score_list2 = []
    word2vec_euc_score_list1 = []
    word2vec_euc_score_list2 = []
    word2vec_cos_score_list1 = []
    word2vec_cos_score_list2 = []
    gpt_euc_score_list1 = []
    gpt_euc_score_list2 = []
    gpt_cos_score_list1 = []
    gpt_cos_score_list2 = []
    select_model_by_kind_sql1 = "select name, bert_euc_score, bert_cos_score, word2vec_euc_score, word2vec_cos_score, gpt_euc_score, gpt_cos_score from questionare_data_model where kind = 0;"
    cursor.execute(select_model_by_kind_sql1)
    kind_data3 = cursor.fetchall()
    for row in kind_data3:
        bert_euc_score, bert_cos_score, word2vec_euc_score, word2vec_cos_score, gpt_euc_score, gpt_cos_score = row[1::]
        bert_euc_score_list1.append(bert_euc_score)
        bert_cos_score_list1.append(bert_cos_score)
        word2vec_euc_score_list1.append(word2vec_euc_score)
        word2vec_cos_score_list1.append(word2vec_cos_score)
        gpt_euc_score_list1.append(gpt_euc_score)
        gpt_cos_score_list1.append(gpt_cos_score)

    select_model_by_kind_sql2 = "select name, bert_euc_score, bert_cos_score, word2vec_euc_score, word2vec_cos_score, gpt_euc_score, gpt_cos_score from questionare_data_model where kind = 1;"
    cursor.execute(select_model_by_kind_sql2)
    kind_data4 = cursor.fetchall()
    for row in kind_data4:
        bert_euc_score, bert_cos_score, word2vec_euc_score, word2vec_cos_score, gpt_euc_score, gpt_cos_score = row[1::]
        bert_euc_score_list2.append(bert_euc_score)
        bert_cos_score_list2.append(bert_cos_score)
        word2vec_euc_score_list2.append(word2vec_euc_score)
        word2vec_cos_score_list2.append(word2vec_cos_score)
        gpt_euc_score_list2.append(gpt_euc_score)
        gpt_cos_score_list2.append(gpt_cos_score)
    # 关闭数据库连接
    conn.close()
    if None in gpt_cos_score_list1:
        semantic_all_data = {
            'name': name_list1,
            'question': question_list1,
            'answer': answer_list1,
            'human': semantics_list,
            'bert_euc_score': bert_euc_score_list1,
            'bert_cos_score': bert_cos_score_list1,
            'word2vec_euc_score': word2vec_euc_score_list1,
            'word2vec_cos_score': word2vec_cos_score_list1,
        }

        grammar_all_data = {
            'name': name_list2,
            'question': question_list2,
            'answer': answer_list2,
            'human': grammar_list,
            'bert_euc_score': bert_euc_score_list2,
            'bert_cos_score': bert_cos_score_list2,
            'word2vec_euc_score': word2vec_euc_score_list2,
            'word2vec_cos_score': word2vec_cos_score_list2,
        }
        df1 = pd.DataFrame(semantic_all_data)
        df2 = pd.DataFrame(grammar_all_data)
        # df1.to_excel('./outputs/语义分数.xlsx', index=True, index_label='id')
        df1.to_excel('./outputs/语义分数.xlsx', index=False)
        # df2.to_excel('./outputs/语法分数.xlsx', index=True, index_label='id')
        df2.to_excel('./outputs/语法分数.xlsx', index=False)
    else:
        semantic_all_data = {
            'name': name_list1,
            'question': question_list1,
            'answer': answer_list1,
            'human': semantics_list,
            'bert_euc_score': bert_euc_score_list1,
            'bert_cos_score': bert_cos_score_list1,
            'word2vec_euc_score': word2vec_euc_score_list1,
            'word2vec_cos_score': word2vec_cos_score_list1,
            'gpt_euc_score': gpt_euc_score_list1,
            'gpt_cos_score': gpt_cos_score_list1,
        }

        grammar_all_data = {
            'name': name_list2,
            'question': question_list2,
            'answer': answer_list2,
            'human': grammar_list,
            'bert_euc_score': bert_euc_score_list2,
            'bert_cos_score': bert_cos_score_list2,
            'word2vec_euc_score': word2vec_euc_score_list2,
            'word2vec_cos_score': word2vec_cos_score_list2,
            'gpt_euc_score': gpt_euc_score_list2,
            'gpt_cos_score': gpt_cos_score_list2,
        }
        df1 = pd.DataFrame(semantic_all_data)
        df2 = pd.DataFrame(grammar_all_data)
        # df1.to_excel('./outputs/语义分数.xlsx', index=True, index_label='id')
        df1.to_excel('./outputs/语义分数.xlsx', index=False)
        # df2.to_excel('./outputs/语法分数.xlsx', index=True, index_label='id')
        df2.to_excel('./outputs/语法分数.xlsx', index=False)
    print('=======>')
    print('分类数据已导出，请查看 outputs目录')


def test1():
    a = 'ddffgghjjk'
    print(a[-4:-2])


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


def process_pre_map():
    conn, cursor = init_db()
    sql1 = "select word1, word2, word3, estimate_word, id from pre_map;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    for row in res1:
        word_list = row[:3]
        estimate_word = row[3]
        tb_id = row[4]
        estimate_word = estimate_word.split('/')
        word1, bert_cos = bert_compute_cos2(word_list, estimate_word)
        word2, bert_dis = bert_compute_dis2(word_list, estimate_word)

        # 对于传入的数据进行预处理
        new_word_list = process_data(word_list)
        change_word = process_data(estimate_word)
        word3, word2vec_cos = word2vec_compute_cos2(new_word_list, change_word)
        word4, word2vec_dis = word2vec_compute_dis2(new_word_list, change_word)
        update_sql = "update pre_map set bert_cosine_similarity = %s, bert_cosine_word = '%s', bert_distance_similarity = %s, bert_distance_word = '%s', word2vec_cosine_similarity =%s, word2vec_cosine_word ='%s', word2vec_distance_similarity = %s, word2vec_distance_word ='%s' where id = %s;" % (
            bert_cos, word1, bert_dis, word2, word2vec_cos, word3, word2vec_dis, word4, tb_id)
        cursor.execute(update_sql)
        print(update_sql)
    conn.commit()
    conn.close()


def rejudge_data():
    conn, cursor = init_db()
    sql1 = "select id, question, bert_cos, bert_euc, word2vec_cos, word2vec_euc from questionare_data_model;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    for row in res1:
        tb_id, question, bert_cos, bert_euc, word2vec_cos, word2vec_euc = row
        q1 = question.split(' ')[1]
        q2 = q1.find('→')
        q3 = q1.find('::')
        word1 = q1[:q2]
        word2 = q1[q2 + 1: q3]
        select_sql1 = "select * from pre_map where (word1 = '%s' and word2 = '%s');" % (word1, word2)
        cursor.execute(select_sql1)
        res2 = cursor.fetchone()
        data1 = row[2::]
        data2 = res2[8:12]
        update_list = []
        for index, val in enumerate(data1):
            if index + 1 % 2 == 0:
                score = dispatch_score(val, data2[index])
                update_list.append(score)
            else:
                score = dispatch_score(val, data2[index], 1)
                update_list.append(score)
        update_sql = ("update questionare_data_model set bert_cos_score = %s, bert_euc_score = %s, word2vec_cos_score "
                      "= %s, word2vec_euc_score"
                      "= %s where id = %s;") % (update_list[0], update_list[1], update_list[2], update_list[3], tb_id)
        cursor.execute(update_sql)
        print(update_sql)
    conn.commit()
    conn.close()


def dispatch_score(estimate_score: float or int, score, compute_type: int = 0):
    """

    :param estimate_score:
    :param score:
    :param compute_type: 计算类型 默认为判断余弦相似度
    :return:
    """
    estimate_score = float(estimate_score)
    # 余弦相似度
    if compute_type == 0:
        if estimate_score >= score:
            return 1
        else:
            return 0
    # 欧式距离
    if compute_type == 1:
        if estimate_score <= score:
            return 1
        else:
            return 0


def unformat_data():
    conn, cursor = init_db()
    sql1 = "SELECT id, question, answer FROM `questionare_data_model` WHERE word2vec_cos = -1.0 or word2vec_euc = 100 or bert_cos = -1.0 or bert_euc = 100;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    for row in res1:
        tb_id, question, answer = row
        pattern = re.compile(r'[^\u4e00-\u9fa5]')
        new_answer = re.sub(pattern, '', answer)

        q1 = question.split(' ')[1]
        q2 = q1.find('→')
        q3 = q1.find('::')
        word1 = q1[:q2]
        word2 = q1[q2 + 1: q3]
        select_sql1 = "select * from pre_map where (word1 = '%s' and word2 = '%s');" % (word1, word2)
        cursor.execute(select_sql1)
        res2 = cursor.fetchone()
        bert_cos, bert_euc, word2vec_cos, word2vec_euc = res2[8:12]
        words = list(res2[1:4])
        try:
            bert_cos_ = bert_compute_cos2(words, [new_answer])[1]
            score1 = dispatch_score(bert_cos_, bert_cos)
            bert_euc_ = bert_compute_dis2(words, [new_answer])[1]
            score2 = dispatch_score(bert_euc_, bert_euc, 1)

            new_answer = process_data([new_answer])
            words = process_data(words)
            print(new_answer, words)

            word2vec_cos_ = word2vec_compute_cos2(words, new_answer)[1]
            score3 = dispatch_score(word2vec_cos_, word2vec_cos)
            word2vec_euc_ = word2vec_compute_dis2(words, new_answer)[1]
            score4 = dispatch_score(word2vec_euc_, word2vec_euc, 1)

            update_sql1 = "update questionare_data_model set bert_cos = %s, bert_euc = %s, word2vec_cos = %s, word2vec_euc = %s, bert_cos_score = %s, bert_euc_score = %s, word2vec_cos_score = %s, word2vec_euc_score = %s where id = %s;" % (
                bert_cos_, bert_euc_, word2vec_cos_, word2vec_euc_, score1, score2, score3, score4, tb_id)
            print(update_sql1)
            print("<==============>")
            cursor.execute(update_sql1)
        except Exception as e:
            print(e)
            print(tb_id)
            print("!!!!!!!!!!!!!!!!!")
            continue

    conn.commit()
    conn.close()


if __name__ == '__main__':
    compute_all()
    judge_human_score()
    merge_data()
    merge_data_by_class()

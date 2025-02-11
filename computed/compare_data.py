import re

import pandas as pd
from db.insert_data import init_db
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

df1 = '../outputs/词类比总表.xlsx'
df2 = '../outputs/语义分数.xlsx'
df3 = '../outputs/语法分数.xlsx'


def compare_score(df_path: str):
    print(df_path)
    df = pd.read_excel(df_path)

    human = df['human']
    bert_euc_score = df['bert_euc_score']
    bert_cos_score = df['bert_cos_score']
    word2vec_euc_score = df['word2vec_euc_score']
    word2vec_cos_score = df['word2vec_cos_score']
    # 选择第5列到最后一列的数据
    start_col = 4  # 第5列对应索引为4
    end_col = len(df.columns)
    selected_cols = df.iloc[:, start_col:end_col]

    # print(selected_cols)
    # 循环读取每一列数据
    for col_name in selected_cols.columns:
        mark1 = 0
        col_data = selected_cols[col_name]
        for index, data in enumerate(col_data):
            compare_data = human[index]
            if data == compare_data:
                mark1 += 1
        # print(col_name + ' 一致性：' + str(mark1 / len(col_data)))
        percentage = (mark1 / len(col_data)) * 100
        # print(col_name + ' 一致性：' + str(percentage))
        print(col_name + ' 一致性：' + "{:.2f}%".format(percentage))

    print('=======')


def fluency_score_for_human():
    conn, cursor = init_db()
    sql1 = "select id, info_id, question, answer, reason, final_score2 from questionare_data_human;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    for _ in res1:
        tb_id, info_id, question, answer, reason, final_score2 = _
        cut_list = split_string_by_symbols(answer)
        if final_score2 == 0.0:
            f_score = 0.0
        else:
            f_score = len(cut_list) * 1.0
        sql2 = "update questionare_data_human set fluency_score = %s where id = %s;" % (f_score, tb_id)
        print(sql2)
        cursor.execute(sql2)
    conn.commit()
    cursor.close()
    conn.close()


def fluency_score_for_model():
    conn, cursor = init_db()
    sql1 = "select id, info_id, question, answer, reason, bert_score2, word2vec_score2, gpt_score2 from questionare_data_model;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    for _ in res1:
        tb_id, info_id, question, answer, reason, bert_score2, word2vec_score2, gpt_score2 = _
        cut_list = split_string_by_symbols(answer)
        if bert_score2 == 0.0:
            f_score1 = 0.0
        else:
            f_score1 = len(cut_list) * 1.0
        if word2vec_score2 == 0.0:
            f_score2 = 0.0
        else:
            f_score2 = len(cut_list) * 1.0
        if gpt_score2 == 0.0:
            f_score3 = 0.0
        else:
            f_score3 = len(cut_list) * 1.0
        sql2 = "update questionare_data_model set bert_fluency_score = %s, word2vec_fluency_score = %s, gpt_fluency_score = %s where id = %s;" % (
            f_score1, f_score2, f_score3, tb_id)
        print(sql2)
        cursor.execute(sql2)
    conn.commit()
    cursor.close()
    conn.close()


def find_all_symbols_indices(s):
    # 正则表达式匹配除字母和数字之外的任何字符
    symbol_pattern = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]')
    # 使用finditer来找到所有匹配项
    matches = symbol_pattern.finditer(s)
    # 收集所有符号的起始索引
    indices = [match.start() for match in matches]
    return indices


def split_string_by_symbols(s):
    # 获取所有符号的起始索引
    symbol_indices = find_all_symbols_indices(s)
    # 初始化列表，用于存放分割后的字符串
    substrings = []
    # 添加第一个子串，从字符串开头到第一个符号之前（如果存在符号的话）
    start = 0
    for index in symbol_indices:
        substrings.append(s[start:index].strip())  # 使用strip()去除前导和尾随空格
        start = index + 1  # 更新起始位置到当前符号之后
    # 添加最后一个子串，从最后一个符号之后到字符串末尾，但需检查以避免添加空字符串
    last_substring = s[start:].strip()
    if last_substring:  # 如果不是空字符串，则添加
        substrings.append(last_substring)
    return substrings


def compare_score2():
    conn, cursor = init_db()
    sql1 = "select id, bert_fluency_score, word2vec_fluency_score, gpt_fluency_score from questionare_data_model;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    bert_list = []
    word2vec_list = []
    gpt_list = []
    for _ in res1:
        tb_id, bert_score2, word2vec_score2, gpt_score2 = _
        bert_list.append(bert_score2)
        word2vec_list.append(word2vec_score2)
        gpt_list.append(gpt_score2)
    human_list = []
    sql2 = "select id, fluency_score from questionare_data_human;"
    cursor.execute(sql2)
    res2 = cursor.fetchall()
    for _ in res2:
        tb_id2, human_score = _
        human_list.append(human_score)

    cursor.close()
    conn.close()
    return bert_list, word2vec_list, gpt_list, human_list
    # mark1 = 0
    # mark2 = 0
    # mark3 = 0
    # for k, v in enumerate(human_list):
    #     if bert_list[k] == v:
    #         # print(k, v)
    #         mark1 += 1
    #     if word2vec_list[k] == v:
    #         mark2 += 1
    #     if gpt_list[k] == v:
    #         mark3 += 1
    # print(mark1)
    # print(mark2)
    # print(mark3)


def draw1(tag='micro'):
    # Please choose another average setting, one of [None, 'micro', 'macro', 'weighted']
    bert_list, word2vec_list, gpt_list, human_list = compare_score2()
    all_list = [word2vec_list, bert_list, gpt_list]
    accuracy_score_list = []
    precision_score_list = []
    recall_score_list = []
    f1_score_list = []
    for i in all_list:
        accuracy_score_list.append(accuracy_score(human_list, i))
        precision_score_list.append(precision_score(human_list, i, average=tag))
        recall_score_list.append(recall_score(human_list, i, average=tag))
        f1_score_list.append(f1_score(human_list, i, average=tag))
    print(accuracy_score_list, precision_score_list, recall_score_list, f1_score_list)


def compare_score3():
    conn, cursor = init_db()
    sql1 = "select id, bert_ori_score, word2vec_ori_score, gpt_ori_score from questionare_data_model;"
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    bert_list = []
    word2vec_list = []
    gpt_list = []
    for _ in res1:
        tb_id, bert_score2, word2vec_score2, gpt_score2 = _
        bert_list.append(bert_score2)
        word2vec_list.append(word2vec_score2)
        gpt_list.append(gpt_score2)
    human_list = []
    sql2 = "select id, final_score2 from questionare_data_human;"
    cursor.execute(sql2)
    res2 = cursor.fetchall()
    for _ in res2:
        tb_id2, human_score = _
        human_list.append(human_score)

    cursor.close()
    conn.close()
    return bert_list, word2vec_list, gpt_list, human_list


def draw2(tag='micro'):
    # Please choose another average setting, one of [None, 'micro', 'macro', 'weighted']
    bert_list, word2vec_list, gpt_list, human_list = compare_score3()
    all_list = [word2vec_list, bert_list, gpt_list]
    accuracy_score_list = []
    precision_score_list = []
    recall_score_list = []
    f1_score_list = []
    # for i in all_list:
    #     accuracy_score_list.append(accuracy_score(human_list, i))
    #     precision_score_list.append(precision_score(human_list, i, average=tag))
    #     recall_score_list.append(recall_score(human_list, i, average=tag))
    #     f1_score_list.append(f1_score(human_list, i, average=tag))
    # print(accuracy_score_list, precision_score_list, recall_score_list, f1_score_list)
    for i in all_list:
        print(classification_report(human_list, i))


if __name__ == '__main__':
    # 示例
    # fluency_score_for_model()
    # test_str = "你好， 世界123！"
    # print(split_string_by_symbols(test_str))  # 应输出['你好', '世界123']
    # compare_score2()
    # draw2()

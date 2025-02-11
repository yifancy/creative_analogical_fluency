from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity as cos

bc = BertClient(ip='127.0.0.1', port=5555, port_out=5556, show_server_config=False, timeout=10000)
# 国王 - 男人 = 皇后 - 女人
# 皇后 = 国王 - 男人 + 女人
vec1 = bc.encode(["国王"])
vec2 = bc.encode(["男人"])
vec3 = bc.encode(["女人"])
# print(vec1)
# print("======")
# print(vec2)
# print("======")
# print(vec3)
# 得到正确答案
answer1 = vec1 - vec2 + vec3
artificial_answer1 = bc.encode(["皇后"])
artificial_answer2 = bc.encode(["宠物"])

# 计算余弦相似度
cosine1 = cos(answer1, artificial_answer1)
print(cosine1)

cosine2 = cos(answer1, artificial_answer2)[0][0]
print(cosine2)

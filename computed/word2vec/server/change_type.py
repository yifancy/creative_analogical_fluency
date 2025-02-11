
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format('F:/bert-server/tencent-ailab-embedding-zh-d200-v0.2.0/tencent-ailab-embedding-zh-d200-v0.2.0/tencent-ailab-embedding-zh-d200-v0.2.0.txt')
# model.save('F:/bert-server/tencent-ailab-embedding-zh-d200-v0.2.0/tencent-ailab-embedding-zh-d200-v0.2.0/tencent_word2vec.wv')

# vector = model.wv['你好']
# print(vector)
model.save("F:/bert-server/tencent-ailab-embedding-zh-d200-v0.2.0/tencent-ailab-embedding-zh-d200-v0.2.0/tencent_word2vec.wv")

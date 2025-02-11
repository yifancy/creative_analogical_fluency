import os
import random
import time

import backoff
import openai
import pymysql
from fastapi import FastAPI


@backoff.on_exception(backoff.expo, openai.RateLimitError)  # 添加修饰，触发限流后，进行重试
def get_embedding(word):
    # 添加代理端口，代理端口进入设置查看，不建议修改源码
    os.environ["http_proxy"] = "http://localhost:10809"
    os.environ["https_proxy"] = "http://localhost:10809"

    # 数据库连接，获取apikey
    db = pymysql.connect(host="8.138.1.108",
                         user="yyy",
                         port=20308,
                         password="wcaM6zg4532e",
                         database="goc_test",
                         charset="utf8mb4")
    cursor = db.cursor()

    select_sql = "select apikey from `gpt_api_key` where used = 1"
    cursor.execute(select_sql)
    results = cursor.fetchall()

    apikey_list = []
    for result in results:
        apikey_list.append(result[0])

    # 随机选择apikey
    apikey = random.choice(apikey_list)
    openai.api_key = apikey
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=word,
    )

    embedding = response["data"][0]["embedding"]
    time.sleep(1)
    return embedding


app = FastAPI()


@app.get('/gpt')
def get_word_vector(word: str):
    if word is None:
        return {'code': 400, 'error': 'Missing "word" parameter.'}

    # if word in word2vec_model.wv:
    if word:
        vector = get_embedding(word)
        vector_ = vector.tolist()
        print(vector)
        # vector = word2vec_model[word]
        return {'code': 200, 'word': word, 'vector': vector_}
    else:
        return {'code': 404, 'error': word + 'Word not found.'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8080, host='0.0.0.0')

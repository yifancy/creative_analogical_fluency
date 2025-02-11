from fastapi import FastAPI
from gensim.models import KeyedVectors

app = FastAPI()
word2vec_model = None


def load_word2vec_model():
    global word2vec_model
    if word2vec_model is None:
        # word2vec_model = Word2Vec.load('word2vec_model.bin')
        # D:/analogy_models/word2vec/tencent-ailab-embedding-zh-d200-v0.2.0
        # word2vec_model = KeyedVectors.load('D:/analogy_models/word2vec/tencent_word2vec.wv')
        word2vec_model = KeyedVectors.load('F:/bert-server/tencent-ailab-embedding-zh-d200-v0.2.0/tencent-ailab-embedding-zh-d200-v0.2.0/tencent_word2vec.wv')


@app.get('/word_vector')
def get_word_vector(word: str):
    if word is None:
        return {'code': 400, 'error': 'Missing "word" parameter.'}

    if word2vec_model is None:
        load_word2vec_model()

    # if word in word2vec_model.wv:
    if word in word2vec_model:
        vector = word2vec_model[word]
        vector_ = vector.tolist()
        print(vector)
        # vector = word2vec_model[word]
        return {'code': 200, 'word': word, 'vector': vector_}
    else:
        return {'code': 404, 'error': word + 'Word not found.'}


def start_app():
    import uvicorn

    uvicorn.run(app)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)

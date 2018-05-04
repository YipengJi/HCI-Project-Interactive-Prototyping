import os
import sys
# path = os.path.realpath('') + '/scripts/'
# sys.path.append(path)
path = os.path.realpath('') + '/'
path2 = os.path.realpath('') + '/datas/'
sys.path.append(path)

import time
import numpy as np
from flask import *
from flask_socketio import *
from celery import Celery, chain
from pattern.web import Twitter
from sklearn.externals import joblib
from gensim.models import Word2Vec
from tokenizer import *


# Initialize and configure Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['SOCKETIO_REDIS_URL'] = 'redis://localhost:6379/0'
app.config['BROKER_TRANSPORT'] = 'redis'
app.config['CELERY_ACCEPT_CONTENT'] = ['pickle']


# Initialize SocketIO
socketio = SocketIO(app, message_queue=app.config['SOCKETIO_REDIS_URL'])

# Initialize and configure Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
celery.conf.update(CELERY_ACCEPT_CONTENT = ['json'])

# Load transforms and models
vectorizer = joblib.load(path2 + 'vectorizer_data.pkl')
classifier = joblib.load(path2 + 'classifier_data.pkl')
pca = joblib.load(path2 + 'pca_data.pkl')
word2vec = Word2Vec.load(path2 + 'word2vec_data.pkl')


def classify_tweet(tweet):
    pred = classifier.predict(vectorizer.transform(np.array([tweet.text])))

    return str(pred[0])


def vectorize_tweet(tweet):
    tweet_vector = np.zeros(100)
    for word in tokenize(tweet.text):
        if word in word2vec.wv.vocab:
            tweet_vector = tweet_vector + word2vec[word]

    tweet_vector = np.reshape(tweet_vector, (1,-1))
    components = pca.transform(tweet_vector)
    x = components[0, 0]
    y = components[0, 1]

    return str(x), str(y)


@celery.task
def create_stream(phrase, queue):
    local = SocketIO(message_queue=queue)
    stream = Twitter().stream(phrase, timeout=120)

    for i in range(120):
        stream.update()
        for tweet in reversed(stream):
            sentiment = classify_tweet(tweet)
            x, y = vectorize_tweet(tweet)
            local.emit('tweet', {'id': str(i),
                                 'text': str(tweet.text.encode('ascii', 'ignore')),
                                 'sentiment': sentiment,
                                 'x': x,
                                 'y': y})
        stream.clear()
        time.sleep(1)

    return queue


@celery.task
def send_complete_message(queue):
    local = SocketIO(message_queue=queue)
    local.emit('complete', {'data': 'Visulization Done ~'})


@app.route('/', methods=['GET'])
def index():
    return render_template('view.html')


@app.route('/twitter/<phrase>', methods=['POST'])
def twitter(phrase):
    queue = app.config['SOCKETIO_REDIS_URL']
    chain(create_stream.s(phrase, queue), send_complete_message.s()).apply_async()
    return 'Connecting to Twitter ... Getting Real Time Data ...'


if __name__ == '__main__':
    socketio.run(app, debug=True)

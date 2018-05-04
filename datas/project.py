import os
import sys
path = os.path.realpath('') + '/'
sys.path.append(path)

import pandas as pd
from sklearn.decomposition.pca import PCA
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from gensim.models import Word2Vec
from tokenizer import *


def main():
    print('Read Project Sentiment Analysis Dataset from Sentiment140 ...')
    data = pd.read_csv(path + 'HCI Project-Sentiment Analysis Dataset.csv',
                       usecols=['Sentiment', 'SentimentText'], error_bad_lines=False)

    print('Victorize Tweets with Sentiment (It takes some time) ...')
    corpus = data['SentimentText']
    vectorizer = TfidfVectorizer(decode_error='replace', strip_accents='unicode',
                                 stop_words='english', tokenizer=tokenize)
    X = vectorizer.fit_transform(corpus.values)
    y = data['Sentiment'].values

    print('Classify Sentiment Texts using sklearn Naive Bayes Classifier for Multinomial Models ...')
    classifier = MultinomialNB()
    classifier.fit(X, y)

    print('Produce a Vector Space using Word2Vec Model (It takes some time) ...')
    corpus = corpus.map(lambda x: tokenize(x))
    word2vec = Word2Vec(corpus.tolist(), size=100, window=4, min_count=10, workers=4)
    word2vec.init_sims(replace=True)

    print('Reduce Word Dimensions using Principal Component Analysis (PCA) ...')
    word_vectors = [word2vec[word] for word in word2vec.wv.vocab]
    pca = PCA(n_components=2)
    pca.fit(word_vectors)

    print('Save Analyzed Data to Corresponding Files ...')
    joblib.dump(vectorizer, path + 'vectorizer_data.pkl')
    joblib.dump(classifier, path + 'classifier_data.pkl')
    joblib.dump(pca, path + 'pca_data.pkl')
    word2vec.save(path + 'word2vec_data.pkl')

    print('Sentiment Analysis for Dataset -> Done')


if __name__ == "__main__":
    main()

# HCI-Project-Interactive-Prototyping

EPFL CS486 Human Computer Interaaction Project: AI is Beautiful - Design Brief III

## Getting Started

### Prerequisites

See Dependencies (Build With)

### Installing

Installing dependencies before running using the following:

```
pip install Flask
```

And repeat "pip install" for all other dependencies.

## Running

* Step 1 - Unzip HCI Project-Sentiment Analysis Dataset.csv file and put it in "datas" directory.

* Step 2 - Open Termial Window 1, Move into "datas" diractory from the terminal.

* Step 3 - Run "project.py" and wait for it to be done (instructions show on terminal logs, only need to run one time for analyzing training dataset).

```
python project.py
```
* Step 4 - Open Termial Window 2, Move into the top directory and run a Redis server (wait for the connection to set up and keep the window open)

```
bash redis.sh
```

* Step 5 - Open Termial Window 3, Move into the top directory and run a Celery worker (wait for the connection to set up and keep the window open)

```
celery worker -A app.celery --loglevel=info
```
* Step 6 - Open Termial Window 4, Move into the top directory and start the application (wait for the Debugger to show up)

```
python app.py
```

* Step 7 - Open [Link](http://127.0.0.1:5000/) in your favorate brower

* Final Step - Play with the visualization : )

## Built With

* [Python 3.6.5](https://www.python.org/) - Language used
* Front-End
* [Bootstrap](https://getbootstrap.com/)  
* [JQuery](http://jquery.com/) - Web
* [Flask 1.0.2](http://flask.pocoo.org/docs/1.0/installation/)  
* [Socket.IO](https://socket.io/) 
* [flask-socketio](https://flask-socketio.readthedocs.io/en/latest/) - Events
* [NVD3](http://nvd3.org/) - Visualization
* Back-End (stream Twitter)
* [Redis](https://redis.io/) - Database
* [Celery](http://www.celeryproject.org/) - Task Queues
* [Python-Pattern](https://github.com/clips/pattern) 
* Algorithms
* [scikit-learn](http://scikit-learn.org/stable/) - Classifications
* [gensim](https://radimrehurek.com/gensim/) - Word2Vec models 

## Authors

* **Yipeng Ji** 

## Acknowledgments

* [Sentiment140](http://help.sentiment140.com/for-students) - Dataset used
* [scikit-learn](http://scikit-learn.org/stable/) - Methods used
* [Christopher Potts](http://sentiment.christopherpotts.net/code-data/happyfuntokenizing.py) - Tokenizer used
* [John Wittenauer](https://github.com/jdwittenauer) - Analysis Steps applied



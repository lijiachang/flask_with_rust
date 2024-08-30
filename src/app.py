from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'home for the fib calculator'


if __name__ == '__main__':
    app.run(use_reloader=True, port=5002, threaded=True)

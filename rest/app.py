from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_scores():
    scores = {str(w): {'health': w} for w in range(16)}
    return jsonify(scores)

if __name__ == '__main__':
    app.run()


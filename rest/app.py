from flask import Flask, jsonify
import json


def load_regions():
    with open('data/regions.json') as f:
        return json.load(f)


def provide_metrics(location):
    return [
        {"metric1": 3},
        {"metric2": 4},
        {"metric3": 5}
    ]


app = Flask(__name__)
app.config.regions = load_regions()


@app.route('/regions', methods=['GET'])
def regions():
    return jsonify(app.config.regions)


@app.route('/metrics', methods=['POST'])
def metrics():
    location = request.json
    return jsonify(provide_metrics(location))


if __name__ == '__main__':
    app.run()

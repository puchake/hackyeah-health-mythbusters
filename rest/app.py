from metrics import get_metric_providers

from flask import Flask, jsonify, request
import json


def load_regions():
    with open('data/regions.json') as f:
        return json.load(f)


app = Flask(__name__)
app.config.regions = load_regions()
app.config.metric_providers = get_metric_providers()


@app.route('/regions', methods=['GET'])
def regions():
    return jsonify(app.config.regions)


@app.route('/metrics', methods=['POST'])
def metrics():
    print(vars(request).keys())
    location = request.json
    location = [location['longitude'], location['latitude']]
    metrics = []
    for p in app.config.metric_providers:
        metrics.append({
            "name": p.name,
            "value": p.provide_metrics(location).tolist()
        })
    return jsonify(metrics)


if __name__ == '__main__':
    app.run()

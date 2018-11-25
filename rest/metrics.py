from sklearn.neighbors import NearestNeighbors
import numpy as np

class MetricsProvider:

    def __init__(self, name, sensor_locations, sensor_values, neighbours=3):
        self.name = name
        self._sensor_locations = sensor_locations
        self._sensor_values = sensor_values
        self._nn = NearestNeighbors(
            n_neighbors=neighbours,
            algorithm='ball_tree',
            metric='euclidean').fit(sensor_locations)

    def provide_metrics(self, location):
        dist, idx = self._nn.kneighbors([location])
        neighs = self._sensor_values[idx[0]]
        dist = dist[0]
        weigh = dist / np.sum(dist)
        estmate = weigh * neighs.T
        return estmate.sum(axis=1)


class MockProvider(MetricsProvider):

    def __init__(self):
        super().__init__(
            "mock",
            np.random.rand(100, 2),
            np.random.rand(100, 1))


def get_metric_providers():
    return [MockProvider()]

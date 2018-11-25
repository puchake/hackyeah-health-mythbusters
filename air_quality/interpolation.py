from sklearn.neighbors import NearestNeighbors
import numpy as np
import json
import pandas as pd

#def geographic_distance(p1, p2):
#    return (p1 - p2)[0]lngs.append(location
#
def get_powiaty():
    with open('data/powiaty.json') as f:
        return np.array(list(v['lat'] for v in json.load(f).values()))

stations_pos = pd.read_csv('data/stations_with_coords.csv')[['lats', 'lngs']].as_matrix()
powiaty = get_powiaty()
to_find = 3
nn = NearestNeighbors(n_neighbors=to_find, algorithm='ball_tree',
                      metric='euclidean').fit(stations_pos)

vals = np.random.rand(stations_pos.shape[0], 7)
def get_nn(powiat, sensor_vals):
    dist, idx = nn.kneighbors([powiat])
    neighs = sensor_vals[idx[0]]
    dist = dist[0]
    weigh = dist / np.sum(dist)
    print('\nneighs {} {}'.format(neighs.shape, neighs))
    print('\nweigh {} {}'.format(weigh.shape, weigh))
    est = weigh * neighs.T
    return est.sum(axis=1)

print(get_nn(powiaty[5], vals))

import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

def get_trained_lr(x, y):
    return LinearRegression().fit(x, y)

def save_pickle(model, path):
    with open(path, "wb") as f:
        pickle.dump(model, f)

def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)

# Example
#
#p = 'dupa'
#x = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
#y = np.dot(x, np.array([1, 2])) + 3
#
#model = get_trained_lr(x, y)
#save_pickle(model, p)
#
#model = load_pickle(p)
#
#print(model.predict(np.array([[3, 5]])))

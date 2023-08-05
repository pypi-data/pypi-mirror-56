from sklearn.neighbors import NearestNeighbors
from collections import Counter
import numpy as np


def topN(n, features):
    """:returns distances and indices of closest n vectors
    """
    nbrs = NearestNeighbors(n_neighbors=n+1, algorithm='auto').fit(features)
    return nbrs.kneighbors(features)


def similarity_img_wise(orig_labels, num_labels, indices):
    """returns  image wise similarity matrix
    """
    arr = [[Counter(j)[i] / 10 if i in Counter(j) else 0 for i in range(num_labels)] for j in orig_labels[indices]]
    arr = np.asarray(arr)
    return arr


def similarity_class_wise(arr, orig_labels, num_labels):
    """returns num_labels X num_labels matrix
    """
    similarity_matrix = np.asarray([np.mean(arr[orig_labels == i], axis=0) for i in range(num_labels)])
    return similarity_matrix




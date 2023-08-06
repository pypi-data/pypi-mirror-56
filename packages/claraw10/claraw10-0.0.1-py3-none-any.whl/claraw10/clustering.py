from sklearn import datasets
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
import statistics as st
from sklearn.metrics.cluster import adjusted_rand_score

def create_clusters(x,y,numberofclusters):
    distance_from_centroid = []
    scores = []
    centroids = []
    for i in range(1,21):
        km = KMeans(n_clusters = numberofclusters, n_init=i)
        km.fit(x)
        y_pred = km.predict(x)  
        distance_from_centroid.append(km.inertia_)
        scores.append((adjusted_rand_score(y,y_pred)))
        centroids.append(km.cluster_centers_)
    index = distance_from_centroid.index(min(distance_from_centroid))
    print("Ideal n_init value is: ",str(index+1))
    print("Centroids are: ",centroids[index])
    print("The mean distance of each point from the centroid is: ",str(distance_from_centroid[index]))
    print("The score is: ",str(scores[index]))

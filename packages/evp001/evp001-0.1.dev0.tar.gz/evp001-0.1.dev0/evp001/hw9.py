
print('######################################################################################')
# program: hw9.py
# Emmy Pahmer
# 17-NOV-2019

from sklearn import datasets, cluster
from sklearn import neighbors
from sklearn import model_selection
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn import metrics

iris = datasets.load_iris()
neighbors_classifier = neighbors.KNeighborsClassifier(n_neighbors=3)
# Old...
# X_train, X_test, y_train, y_test = model_selection.train_test_split(iris.data, iris.target, test_size=0.1)
# neighbors_classifier.fit(X_train, y=y_train)
# neighbors_classifier.score(X_test, y=y_test)
model_selection.cross_val_score(neighbors_classifier, iris.data, iris.target, cv=5)


def get_clusters(X, y, num_clusters, seed):
    print('> ================== run kmeans, k =', num_clusters, ', seed = ', seed, ' ======================')
    # n_init : int, default: 10
    # Number of time the k-means algorithm will be run with different centroid seeds. The final 
    # results will be the best output of n_init consecutive runs in terms of inertia.

    # it is common for the algorithm to be run for multiple starting guesses, as indeed Scikit-Learn 
    # does by default (set by the n_init parameter

    km = KMeans(n_clusters=num_clusters, init='k-means++',  # tested k-means++ and random
        n_init=10, max_iter=300,
        tol=1e-04, random_state=seed)  # tested several random_state values, difference is v small
    y_km = km.fit_predict(X)   # numpy.ndarray

    print('> centroids')
    print(km.cluster_centers_)

    print ('> plot the clusters and centroids')
    plt.scatter(
        X[y_km == 0, 0], X[y_km == 0, 1],
        s=50, c='green',
        marker='o', edgecolor='black',
        label='Cluster 1'
    )

    plt.scatter(
        X[y_km == 1, 0], X[y_km == 1, 1],
        s=50, c='orange',
        marker='o', edgecolor='black',
        label='Cluster 2'
    )

    plt.scatter(
        X[y_km == 2, 0], X[y_km == 2, 1],
        s=50, c='blue',
        marker='o', edgecolor='black',
        label='Cluster 3'
    )

    # plot the centroids
    plt.scatter(
        km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
        s=250, marker='*',
        c='red', edgecolor='black',
        label='Centroids'
    )
    plt.legend(scatterpoints=1)
    plt.title('K-means run with random_state=' + str(seed))
    plt.grid()
    plt.show()

    # There are some green points which look like they should be in the blue group (to the right of the 
    # blue centroid). Presentation problem since data is multi-dimensional? 

    print('> actual target values')
    labels_true = y
    print(labels_true)

    print('> labels assigned')
    labels_pred = y_km
    print(labels_pred)

    # If we have the ground truth labels (class information) of the data points available with us then we can 
    # make use of extrinsic methods like homogeneity score, completeness score and so on.
    print('> homogeneity_score')
    hscore = metrics.homogeneity_score(labels_true, labels_pred) 
    print(hscore)
    print('> completeness_score')
    cscore = metrics.completeness_score(labels_true, labels_pred)
    print(cscore)
    print('> combined score')
    tscore = hscore + cscore
    print(tscore)
    # these results are all really, really close

# Random sample consensus, RANSAC, is one of iterative methods to detect outliers. 
# An iterative method uses an initial guess to generate a sequence of improving approximations. 
# It is widely used in the image processing field for cleaning the noise from the dataset.

def main():
    iris = datasets.load_iris()
    X = iris.data   # features
    y = iris.target  # labels
    num_clusters = 3

    seeds = [1, 3, 5, 7, 11, 13, 17, 19]
    for seed in seeds:
        get_clusters(X, y, num_clusters, seed)

if __name__ == "__main__":
    main()
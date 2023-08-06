import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import model_selection
from sklearn.cluster import KMeans
iris = load_iris()
iternim = 10000
a = []
trainselect =[]
for i in range(0,iternim):
    X_train, X_test, y_train, y_test = train_test_split(iris.data,iris.target,test_size=0.1)
    model = KMeans(n_clusters=3)
    model.fit(X_train,y_train)
    b = metrics.silhouette_score(X_test,y_test)
    if b >= 0.80:
        trainselect.append(X_train)
        trainselect.append(y_train)
        print(trainselect)
        print(b)
        print('Threshold is satisfied!')
        break
    a.append(b)
    if i == iternim-1:
        print('10000 iteration is passed and threshold is not satisfied. This is the best result!')
        print(max(a))

















import numpy as np
from sklearn.neighbors import LocalOutlierFactor


def LOF(data):

    point_of_x = []
    point_of_y = []
    k = len(data) if len(data) < 6 else 6
    clf = LocalOutlierFactor(n_neighbors=k, algorithm='auto', contamination=0.1, n_jobs=-1, novelty=False)
    clf.fit_predict(data)
    for index, outlier in enumerate(clf.negative_outlier_factor_):
        if 1.1 > abs(outlier) > 0.9:
            point_of_x.append(data[index][0])
            point_of_y.append(data[index][1])
    x = np.mean(point_of_x)
    y = np.mean(point_of_y)
    return x, y


import numpy as np
import matplotlib.pyplot as plt
import time
import warnings

from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from itertools import cycle, islice

n_samples = 1500
X, y = datasets.make_blobs(n_samples=n_samples, centers=3, random_state=170)

# 定义不同的clustering算法的训练及可视化函数
def plot_cluster(X, y, params, save_name):
    # 利用kneighbors_graph， 建立 connectivity
    connectivity = kneighbors_graph(X, n_neighbors=params["n_neighbors"])
    # make connectivity symmetric
    connectivity = 0.5 * (connectivity + connectivity.T)

    # 定义kmeans，cluster数目根据传进来的参量
    kmeans = cluster.KMeans(n_clusters=params["n_clusters"])

    # 定义DBSCAN，eps和min_samples由传进来的params参量获得
    dbscan = cluster.DBSCAN(eps=params['eps'], min_samples=params["min_samples"])

    # 根据Eulidean欧式距离的average还是maximum得到 AgglomerativeClustering算法的两种average和complete linkage
    average_linkage = cluster.AgglomerativeClustering(linkage="average",
                                                      affinity="euclidean",
                                                      n_clusters=params['n_clusters'],
                                                      connectivity=connectivity)

    complete_linkage = cluster.AgglomerativeClustering(linkage="complete",
                                                       affinity="euclidean",
                                                       n_clusters=params['n_clusters'],
                                                       connectivity=connectivity)
    # GMM算法
    gmm = mixture.GaussianMixture(n_components=params['n_clusters'])

    # Spectral clustering算法
    spectral = cluster.SpectralClustering(n_clusters=params['n_clusters'],
                                          affinity="nearest_neighbors")
    # 选取六种聚类算法
    clustering_algorithms = (
        ('Kmeans', kmeans),
        ('DBSCAN', dbscan),
        ('Average linkage agglomerative clustering', average_linkage),
        ('Complete linkage agglomerative clustering', complete_linkage),
        ('Spectral clustering', spectral),
        ('GaussianMixture', gmm)
    )

    plt.figure(figsize=(10, 10))

    # 画图展示六种聚类算法的分类效果
    for i, (alg_name, algorithm) in enumerate(clustering_algorithms):
        t0 = time.time()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            algorithm.fit(X)
        t1 = time.time()
        if hasattr(algorithm, 'labels_'):
            y_pred = algorithm.labels_.astype(np.int)
        else:
            y_pred = algorithm.predict(X)  # GMM

        plt.subplot(3, 2, i + 1)
        colors = np.array(list(islice(cycle(['#377eb8', '#ff7f00', '#4daf4a',
                                             '#f781bf', '#a65628', '#984ea3',
                                             '#999999', '#e41a1c', '#dede00']),
                                      int(max(y_pred) + 1))))
        plt.scatter(X[:, 0], X[:, 1], s=10, color=colors[y_pred])

        plt.xlim(-2.5, 2.5)
        plt.ylim(-2.5, 2.5)
        plt.xticks(())
        plt.yticks(())
        plt.title(alg_name)
        plt.text(.99, .01, ('time = %.2fs' % (t1 - t0)).lstrip('0'),
                 transform=plt.gca().transAxes, size=15,
                 horizontalalignment='right')
    plt.savefig(save_name)
    plt.show()


if __name__ == '__main__':
    # Circular_Distribution_Data_Input
    n_samples = 1500
    X, y = datasets.make_blobs(n_samples=n_samples, centers=3, random_state=170)
    plt.scatter(X[:, 0], X[:, 1], s=10)
    plt.savefig('test.png')
    plt.show()
    params = {'eps': .3, 'n_clusters': 4, "n_neighbors": 10, "min_samples": 10}
    plot_cluster(X, y, params=params,
                 save_name='Cluster_Six_Clustering_Algorithms_to_Circular_Distribution_Data_1.png')

    # Moon_Shape_Data_Input
    X, y = datasets.make_moons(n_samples=n_samples, noise=.05)
    X = StandardScaler().fit_transform(X)
    params = {'eps': .3, 'n_clusters': 3, "n_neighbors": 20, "min_samples": 10}
    plot_cluster(X, y, params=params, save_name='Cluster_Six_Clustering_Algorithms_to_Moon_shape_Data_2.png')

    # 多种差异的斑点数据输入
    random_state = 170
    X, y = datasets.make_blobs(n_samples=n_samples, cluster_std=[1.0, 2.5, 0.5], random_state=random_state)

    X = StandardScaler().fit_transform(X)
    params = {'eps': 0.18, 'n_clusters': 3, "n_neighbors": 2, "min_samples" : 5}
    plot_cluster(X, y, params=params, save_name='Cluster_Six_Clustering_Algorithms_to_blobs_with_varied_variances_Data_3.png')

    # 各向异性样本数据输入
    X, y = datasets.make_blobs(n_samples=n_samples, random_state=random_state)
    transformation = [[0.6, -0.6], [-0.4, 0.8]]
    X = np.dot(X, transformation)
    X = StandardScaler().fit_transform(X)
    params = {'eps': 0.18, 'n_clusters': 3, "n_neighbors": 2, "min_samples": 5}
    plot_cluster(X, y, params=params, save_name='Cluster_Six_Clustering_Algorithms_to_anisotropy_Data_4.png')

    # 对随机样本的聚类
    X, y = np.random.rand(n_samples, 2), None
    X = StandardScaler().fit_transform(X)
    params = {'eps': 0.3, 'n_clusters': 3, "n_neighbors": 10, "min_samples": 5}
    plot_cluster(X, y, params=params, save_name='Cluster_Six_Clustering_Algorithms_to_Random_Sample_Data_5.png')













#  encoding=utf-8

# 导入编程所需的库函数
import numpy as np  # 导入科学计算库
from sklearn.cluster import DBSCAN   # 导入DBscan密度聚类函数
from sklearn import metrics     # 导入评估指标函数
from sklearn.datasets.samples_generator import make_blobs   # 导入生成样本函数
from sklearn.preprocessing import StandardScaler    # 导入对数据做标准化预处理函数
import matplotlib.pyplot as plt    # 导入绘图函数


class DBScan (object):
    """
    定义该类从对象继承，封装了DBScan算法
    """
    def __init__(self, p, l_stauts):   # 对类的初始化函数

        self.point = p
        self.labels_stats = l_stauts
        self.db = DBSCAN(eps=0.2, min_samples=10).fit(self.point)   # 设置DBscan函数的参数

    def draw(self):    # 画图函数

        coreSamplesMask = np.zeros_like(self.db.labels_, dtype=bool)
        coreSamplesMask[self.db.core_sample_indices_] = True
        labels = self.db.labels_
        nclusters = self.jiangzao(labels)

        # 输出模型评估参数，包括估计的集群数量、均匀度、完整性、V度量、
        # 调整后的兰德指数、调整后的互信息量、轮廓系数
        print('Estimated number of clusters: %d' % nclusters)
        print("Homogeneity: %0.3f" % metrics.homogeneity_score(self.labels_stats, labels))
        print("Completeness: %0.3f" % metrics.completeness_score(self.labels_stats, labels))
        print("V-measure: %0.3f" % metrics.v_measure_score(self.labels_stats, labels))
        print("Adjusted Rand Index: %0.3f"
              % metrics.adjusted_rand_score(self.labels_stats, labels))
        print("Adjusted Mutual Information: %0.3f"
              % metrics.adjusted_mutual_info_score(self.labels_stats, labels))
        print("Silhouette Coefficient: %0.3f"
              % metrics.silhouette_score(self.point, labels))

        # 绘制结果
        # 黑色被移除，并被标记为噪音。
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # 黑色用于噪声
                col = 'k'

            classMemberMask = (labels == k)

            # 画出分类点集
            xy = self.point[classMemberMask & coreSamplesMask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                     markeredgecolor='k', markersize=6)

            # 画出噪声点集
            xy = self.point[classMemberMask & ~coreSamplesMask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                     markeredgecolor='k', markersize=3)
        # 加标题，显示分类数
        plt.title('(DBSCAN)'+'  '+'Estimated number of clusters: %d' % nclusters)
        plt.savefig('Clustering_DBSCAN_clustering_4_10.png')
        plt.show()


    def jiangzao (self, labels):

        # 标签中的簇数，忽略噪声（如果存在）
        clusters = len(set(labels)) - (1 if -1 in labels else 0)
        return clusters








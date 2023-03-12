import os
import sklearn
from sklearn.metrics import calinski_harabasz_score,silhouette_score
import warnings
import copy
import random
import matplotlib
import numpy as np
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings('ignore')


file_dir = './data'
random.seed(112)
csv_files = os.listdir(file_dir)
# df 作为最后输出的 DataFrame 初始化为空
df = pd.DataFrame()
feature = ['cpc', 'cpm']
df_features = []
for col in feature:
    infix = col + '.csv'
    path = os.path.join(file_dir, infix)
    df_feature = pd.read_csv(path)
    # 将两个特征存储起来用于后续连接
    df_features.append(df_feature)

# 2 张 DataFrame 表按时间连接
df = pd.merge(left=df_features[0], right=df_features[1])
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 将 df 数据按时间序列排序，方便数据展示
df = df.sort_values(by='timestamp').reset_index(drop=True)
def simple_distance(data):
    """
    计算当前点（cpc，cpm）到（cpc_mean，cpm_mean）的几何距离（L2 范数）
    :param data: ataDFrame 包含cpc、cpm 列
    :return: Series，每一列cpc、cpm到平均值值点的距离大小
    """
    mean = np.array([data['cpc'].mean(), data['cpm'].mean()])
    distance = []
    for i in range(0, len(data)):
        point = np.array(data.iloc[i, 1:3])
        # 求当前点（cpc，cpm）到平均值点（cpc_mean，cpm_mean）之间的几何距离（L2 范数）
        distance.append(np.linalg.norm(point - mean))
    distance = pd.Series(distance)
    return distance
def get_distance(data, kmeans, n_features):
    """
    计算距离函数
    :param data: 训练 kmeans 模型的数据
    :param kmeans: 训练好的 kmeans 模型
    :param n_features: 计算距离需要的特征的数量
    :return: 每个点距离自己簇中心的距离
    """
    distance = []
    for i in range(0,len(data)):
        point = np.array(data.iloc[i,:n_features])
        center = kmeans.cluster_centers_[int(kmeans.labels_[i]),:n_features]
        distance.append(np.linalg.norm(point - center))
    distance = pd.Series(distance)
    return distance
df['cpc X cpm'] = df['cpm'] * df['cpc']
df['cpc / cpm'] = df['cpc'] / df['cpm']
df['hours'] = df['timestamp'].dt.hour
df['daylight'] = ((df['hours'] >= 7) & (df['hours'] <= 22)).astype(int)
df1 = df[['cpc','cpm','cpc X cpm','cpc / cpm','hours','daylight']]
from sklearn.decomposition import PCA

#在进行特征变换之前先对各个特征进行标准化
columns = ['cpc', 'cpm', 'cpc X cpm', 'cpc / cpm']
data = df[columns]
scaler = StandardScaler()
data = scaler.fit_transform(data)
data = pd.DataFrame(data, columns=columns)

#通过 n_components 指定需要降低到的维度
n_components = 3
pca = PCA(n_components=n_components)
data = pca.fit_transform(data)
data = pd.DataFrame(data,columns=['Dimension' + str(i+1) for i in range(n_components)])
var_explain = pca.explained_variance_ratio_
# 梯形累计和，axis=0，按照行累加。axis=1，按照列累加。axis不给定具体值，就把数组当成一个一维数组
cum_var_explian = np.cumsum(var_explain)


from mpl_toolkits.mplot3d import Axes3D

class KMeans():
    """
    Parameters
    ----------
    n_clusters 指定了需要聚类的个数，这个超参数需要自己调整，会影响聚类的效果
    n_init 指定计算次数，算法并不会运行一遍后就返回结果，而是运行多次后返回最好的一次结果，n_init即指明运行的次数
    max_iter 指定单次运行中最大的迭代次数，超过当前迭代次数即停止运行
    """
    def __init__(
                self,
                n_clusters=8,
                n_init=10,
                max_iter=300
                ):

        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.n_init = n_init


    def fit(self, x):
        """
        用fit方法对数据进行聚类
        :param x: 输入数据
        :best_centers: 簇中心点坐标 数据类型: ndarray
        :best_labels: 聚类标签 数据类型: ndarray
        :return: self
        """
        ###################################################################################
        #### 请勿修改该函数的输入输出 ####
        ###################################################################################
        # #
        best_score = 0
        for i in range(self.n_init):
            initial_points = np.random.randint(0,len(data),8)
            initial_centers = x.iloc[initial_points].values
            labels = np.zeros(len(x))
            for i in range(self.max_iter):
                for row in x.index:
                    point = np.array(x.iloc[row,0:3])
                    min = 99999
                    for i in range(initial_centers.shape[0]):
                        center = initial_centers[i]
                        k = np.linalg.norm(point - center)
                        if k < min:
                            min = k
                            labels[row] = i
                new_center = []
                for i in range(self.n_clusters):
                    new_center.append(x.iloc[np.array(np.where(labels==i))[0]].mean().values)
                new_centers = np.array(new_center) 
                if (new_centers == initial_centers).all():
                    break
                else:
                    initial_centers = new_centers
            score = calinski_harabasz_score(data,labels)
            if score > best_score :
                print(score,best_score)
                print()
                best_score = score
                best_labels = labels
                best_centers = new_centers
        # #
        ###################################################################################
        ############# 在生成 main 文件时, 请勾选该模块 ############# 
        ###################################################################################


        self.cluster_centers_ = best_centers
        self.labels_ = best_labels
        return self
kmeans = KMeans()
kmeans.fit(data)
joblib.dump(data, './results/data.pkl')
joblib.dump(scaler, './results/scaler.pkl')
joblib.dump(pca, './results/pca.pkl')

from copy import deepcopy
ratio = 0.01
num_anomaly = int(len(data) * ratio)
new_data = deepcopy(data)
new_data['distance'] = get_distance(new_data,kmeans,n_features=len(new_data.columns))
threshould = new_data['distance'].sort_values(ascending=False).reset_index(drop=True)[num_anomaly]
print('阈值距离：'+str(threshould))
new_data['is_anomaly'] = new_data['distance'].apply(lambda x: x > threshould)
normal = new_data[new_data['is_anomaly'] == 0]
anormal = new_data[new_data['is_anomaly'] == 1]
fig = plt.figure(1, figsize=(6, 6))
ax = Axes3D(fig)
ax.scatter(anormal.iloc[:, 0], anormal.iloc[:, 1], anormal.iloc[:, 2], c='red', edgecolors='k')
ax.scatter(normal.iloc[:, 0], normal.iloc[:, 1], normal.iloc[:, 2], c='blue', edgecolors='k')
a = df.loc[new_data['is_anomaly'] == 1, ['timestamp', 'cpc','cpm']]
print(a.columns)
plt.figure(figsize=(20,6))
plt.plot(df['timestamp'], df['cpc'], color='blue')
# 聚类后 cpc 的异常点
plt.scatter(a['timestamp'],a['cpc'], color='red')
plt.plot(df['timestamp'], df['cpm'], color='blue')
# # 聚类后 cpm 的异常点
plt.scatter(a['timestamp'],a['cpm'], color='red')
plt.show()
import os
import sklearn
from sklearn.metrics import calinski_harabasz_score,silhouette_score
import warnings
import copy
from copy import deepcopy
import random
from sklearn.externals import joblib
import matplotlib
import numpy as np
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    """
    数据处理及特征工程等
    :param df: 读取原始 csv 数据，有 timestamp、cpc、cpm 共 3 列特征
    :return: 处理后的数据, 返回 pca 降维后的特征
    """
    # 请使用joblib函数加载自己训练的 scaler、pca 模型，方便在测试时系统对数据进行相同的变换
    # ====================数据预处理、构造特征等========================
    # 例如
    # df['hours'] = df['timestamp'].dt.hour
    # df['daylight'] = ((df['hours'] >= 7) & (df['hours'] <= 22)).astype(int)

    df['cpc X cpm'] = df['cpm'] * df['cpc']
    # df['hours'] = df['timestamp'].dt.hour
    # df['daylight'] = ((df['hours'] >= 7) & (df['hours'] <= 22)).astype(int)
    df1 = df[['cpc','cpm','cpc X cpm']]
    columns = ['cpc', 'cpm', 'cpc X cpm']
    data = df[columns]
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    data = pd.DataFrame(data, columns=columns)
    # ========================  模型加载  ===========================
    # 请确认需要用到的列名，e.g.:columns = ['cpc','cpm']
    # columns = ['cpc','cpm']
    # data = df[columns]
    # 例如
    # scaler = joblib.load('./results/scaler.pkl')
    # n_components = 3
    # pca = PCA(n_components=n_components)
    # data = pca.fit_transform(data)
    # ndata = pd.DataFrame(data,columns=['Dimension' + str(i+1) for i in range(n_components)])
    return data

def get_distance(data, kmeans, n_features):
    """
    计算样本点与聚类中心的距离
    :param data: preprocess_data 函数返回值，即 pca 降维后的数据
    :param kmeans: 通过 joblib 加载的模型对象，或者训练好的 kmeans 模型
    :param n_features: 计算距离需要的特征的数量
    :return:每个点距离自己簇中心的距离，Series 类型
    """
    # ====================计算样本点与聚类中心的距离========================
    distance = []
    for i in range(0,len(data)):
        point = np.array(data.iloc[i,:n_features])
        center = kmeans.cluster_centers_[int(kmeans.labels_[i]),:n_features]
        distance.append(np.linalg.norm(point - center))
    distance = pd.Series(distance)
    return distance
    

def get_anomaly(data, kmean, ratio):
    """
    检验出样本中的异常点，并标记为 True 和 False，True 表示是异常点

    :param data: preprocess_data 函数返回值，即 pca 降维后的数据，DataFrame 类型
    :param kmean: 通过 joblib 加载的模型对象，或者训练好的 kmeans 模型
    :param ratio: 异常数据占全部数据的百分比,在 0 - 1 之间，float 类型
    :return: data 添加 is_anomaly 列，该列数据是根据阈值距离大小判断每个点是否是异常值，元素值为 False 和 True
    """
    # ====================检验出样本中的异常点========================
    num_anomaly = int(len(data) * ratio)
    new_data = deepcopy(data)
    # print(new_data.columns)
    new_data['distance'] = get_distance(new_data,kmean,n_features=len(new_data.columns))
    threshould = new_data['distance'].sort_values(ascending=False).reset_index(drop=True)[num_anomaly]
    # print('阈值距离：'+str(threshould))
    new_data['is_anomaly'] = new_data['distance'].apply(lambda x: x > threshould)
    normal = new_data[new_data['is_anomaly'] == 0]
    anormal = new_data[new_data['is_anomaly'] == 1]
    
    
    data['is_anomaly'] = new_data['is_anomaly']
    return new_data

def predict(preprocess_data):
    """
    该函数将被用于测试，请不要修改函数的输入输出，并按照自己的模型返回相关的数据。
    在函数内部加载 kmeans 模型并使用 get_anomaly 得到每个样本点异常值的判断
    :param preprocess_data: preprocess_data函数的返回值，一般是 DataFrame 类型
    :return:is_anomaly:get_anomaly函数的返回值，各个属性应该为（Dimesion1,Dimension2,......数量取决于具体的pca），distance,is_anomaly，请确保这些列存在
            preprocess_data:  即直接返回输入的数据
            kmeans: 通过joblib加载的对象
            ratio:  异常点的比例，ratio <= 0.03   返回非异常点得分将受到惩罚！
    """
    # 异常值所占比率
    ratio = 0.03
    # 加载模型 
    kmeans = joblib.load('./results/model.pkl')
    # 获取异常点数据信息
    is_anomaly = get_anomaly(preprocess_data, kmeans, ratio)
    return is_anomaly, preprocess_data, kmeans, ratio



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
                n_clusters=4,
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
                    point = np.array(x.iloc[row,0:x.shape[1]])
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





# file_dir = './data'
# random.seed(112)
# csv_files = os.listdir(file_dir)
# # df 作为最后输出的 DataFrame 初始化为空
# df = pd.DataFrame()
# feature = ['cpc', 'cpm']
# df_features = []
# for col in feature:
#     infix = col + '.csv'
#     path = os.path.join(file_dir, infix)
#     df_feature = pd.read_csv(path)
#     # 将两个特征存储起来用于后续连接
#     df_features.append(df_feature)

# # 2 张 DataFrame 表按时间连接
# df = pd.merge(left=df_features[0], right=df_features[1])
# df['timestamp'] = pd.to_datetime(df['timestamp'])

# # 将 df 数据按时间序列排序，方便数据展示
# df = df.sort_values(by='timestamp').reset_index(drop=True)
# data = preprocess_data(df)
# print(data.shape,data.columns)
# is_anomaly, preprocess_data, kmeans, ratio = predict(data)
# # kmeans = joblib.load("./results/model.pkl")
# print(kmeans.cluster_centers_.shape)
# print(is_anomaly.shape,is_anomaly.columns)
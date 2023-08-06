import numpy as np
from sklearn.datasets import make_moons
from sklearn.datasets import make_blobs
from sklearn.datasets import make_circles
from sklearn.datasets import make_gaussian_quantiles
import os

#"moons-2class"  "blobs-2class"  "blobs-3class"   "circles-2class"  "gaussian-quantiles-2class"
# "line-regression" "curve-regression"
# "random"
def create_data(n_points, form, store_address,file_name):
    if not os.path.exists(store_address):
        print("path not exists")
        os.makedirs(store_address)
    else:
        pass

    file_address = os.path.join(store_address, "%s-%sForm-%dP.txt"%(file_name, form, n_points))
    print('file address is :',file_address)
    if os.path.exists(file_address):
        print('We have the data files')
        data = np.loadtxt(file_address, delimiter=',')
        X_train = data[:, :-1]
        y_train = data[:, -1]
        print('load existing data')
    else:
        # 生成数据
        # 生成X,y值
        if form == "moons-2class":
            print('We use make_moons')
            # noise 噪声程度 factor 内圈和外圈之间的比例因子
            X, y = make_moons(n_samples=n_points, noise=0.20, random_state=73)
            X_train = np.around(((X - X.min()) * 50), decimals=2)
            y_train = y
        elif form == "blobs-2class":
            print('We use make_blobs')
            # centers设置中心数为3簇,n_features特征列为2列,cluster_std调整各个类别相交程度,
            X_train, y_train = make_blobs(n_samples=n_points, random_state=73, n_features=2,
                                          centers=2, cluster_std=3.5, center_box=(0, 100))
        elif form == "blobs-3class":
            print('We use make_blobs')
            # centers设置中心数为3簇,n_features特征列为2列,cluster_std调整各个类别相交程度,
            X_train, y_train = make_blobs(n_samples=n_points, random_state=73, n_features=2,
                                          centers=3, cluster_std=3.5, center_box=(0, 100))
        elif form == "circles-2class":
            print('We use make_circles')
            X, y = make_circles(n_samples=n_points, factor=0.7, random_state=73, noise=0.07)
            X_train = np.around(((X - X.min()) * 50), decimals=2)
            y_train = y

        elif form == "gaussian-quantiles-2class":
            print('We use make_gaussian_quantiles')
            # 生成数据
            # 生成2维正态分布，生成的数据按分位数分为两类，500个样本,2个样本特征，2个类别, 协方差系数为2
            X1, y1 = make_gaussian_quantiles(cov=2.0, n_samples=n_points, n_features=2, n_classes=2, random_state=73)
            # 生成2维正态分布，生成的数据按分位数分为两类，500个样本,2个样本特征，2个类别, 协方差系数为2
            X2, y2 = make_gaussian_quantiles(mean=(5, 5), cov=3, n_samples=n_points, n_features=2, n_classes=2,
                                             random_state=73)
            # 讲两组数据合成一组数据
            X = np.concatenate((X1, X2))
            # 这里是将数据标签进行球体求外混合,如果没有`- y2 + 1`,则球心同属一类样本
            y = np.concatenate((y1, - y2 + 1))
            X_train = np.around(((X - X.min()) * 7), decimals=2)
            y_train = y

        elif form == "line-regression":
            # 构造满足一元二次方程的函数
            # 参数解读: 我们构建了300个数据点,分布在[-1,1]区间,直接采用np生成等差数列的方式,将结果为300个点的一维数组,转换为300*1的二维数组
            # np.newaxis用来将前面的一维数组的每个元素作为一个新的行,就此产生了二位数组
            X_train = np.around(np.linspace(0, 100, n_points)[:, np.newaxis], decimals=2)
            # print(x_data.shape)  #(300, 1)
            # 加入一些噪声点,使它与x_data的维度一致,并且拟合均值为0、方差为0.05的正态分布
            noise = np.around(np.random.normal(0, 5, X_train.shape), decimals=3)
            # print(noise.shape)  #(300, 1)

            # 根据公式生成相应的数据点
            y_train = np.around(2 * X_train - 3.0 + noise, decimals=2)
        elif form == "curve-regression":
            X = np.around(np.linspace(0, 2*np.pi, n_points)[:, np.newaxis], decimals=2)
            noise = np.around(np.random.normal(0, 0.1, X.shape), decimals=3)
            y = np.around(np.sin(X) + noise, decimals=2)
            X_train = (X - X.min())*16
            y_train = (y-y.min())*16

        elif form == "random":
            # 构造满足一元二次方程的函数
            # 参数解读: 我们构建了n_points个数据点,分布在[-1,1]区间,直接采用np生成等差数列的方式,将结果为100个点的一维数组,转换为100*1的二维数组
            # np.newaxis用来将前面的一维数组的每个元素作为一个新的行,就此产生了二位数组
            X_data = np.linspace(0, 100, n_points)[:, np.newaxis]

            # 根据公式生成相应的数据点
            y_data = np.random.random_sample(X_data.shape) * 100
            # print(y_data.shape)  #(100, 1)
            # 将特征列合并
            X_train = np.c_[X_data, y_data]
            # 生成labels,在[0,3)之间的整数,数量100
            y_train = np.random.randint(3, size=n_points)

        # 将特征与label合并
        data = np.c_[X_train, y_train]
        # 存储,保留4位小数
        np.savetxt(file_address, data, delimiter=',', fmt='%.2f')
    return n_points, X_train, y_train, form
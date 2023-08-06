# 查看这个构造的数据
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import matplotlib.pyplot as plt
import os


def create_data(n_points, load):
    if not os.path.exists("/shared-datasets/33_ModulesDerivation/ML-SL-C-K最近邻-KNearestNeighbor-KNN/"):
        print("path not exists")
        os.makedirs("/shared-datasets/33_ModulesDerivation/ML-SL-C-K最近邻-KNearestNeighbor-KNN/")
    else:
        pass

    if load == True:
        data = np.loadtxt(
            "/shared-datasets/33_ModulesDerivation/ML-SL-C-K最近邻-KNearestNeighbor-KNN/ML-SL-C-KNN-Scatter-%dP.txt" % (
                n_points), delimiter=',')
        X = data[:, :2]
        y = data[:, 2]
        print('load existing data')
    else:
        np.random.seed(73)
        # np.newaxis用来将前面的一维数组的每个元素作为一个新的行,就此产生了二位数组
        X_data = np.linspace(0, 100, n_points)[:, np.newaxis]
        # 根据公式生成相应的数据点
        y_data = np.random.random_sample(X_data.shape) * 100
        # 生成labels,在[0,3)之间的整数,数量n
        y = np.random.randint(3, size=n_points)
        # 将特征列合并
        X = np.c_[X_data, y_data]
        # 将特征与label合并
        data = np.c_[X, y]
        # 保存数据
        # 存储,保留4位小数
        np.savetxt(
            "/shared-datasets/33_ModulesDerivation/ML-SL-C-K最近邻-KNearestNeighbor-KNN/ML-SL-C-KNN-Scatter-%dP.txt" % (
                n_points), data, delimiter=',', fmt='%.4f')
    return n_points, X, y


def knn_plot_l1(n_points, X, y,module, test_array, k):
    # # 训练最近邻分类器
    # knc = KNeighborsClassifier(p=1)
    # _ = knc.fit(X, y)
    module.set_params(p=1)
    # 绘制散点图
    plt.figure(figsize=(12, 12))

    if len(set(y)) == 1:
        # 绘制训练过程
        plt.scatter(X[:, 0], X[:, 1],
                    c="orange", cmap=plt.cm.Paired,
                    s=20, edgecolor='k',
                    label="FAIH Class 0")

    elif len(set(y)) == 2:
        # class_number = 2
        plot_colors = ["gold", "limegreen"]
        # 绘制训练过程
        for i, c in zip(range(2), plot_colors):
            idx = np.where(y == i)
            plt.scatter(X[idx, 0], X[idx, 1],
                        c=c, cmap=plt.cm.Paired,
                        s=20, edgecolor='k',
                        label="FAIH Class %s" % i)
    elif len(set(y)) == 3:
        # class_number = 2
        plot_colors = ["gold", "limegreen", "orangered"]
        # 绘制训练过程
        for i, c in zip(range(3), plot_colors):
            idx = np.where(y == i)
            plt.scatter(X[idx, 0], X[idx, 1],
                        c=c, cmap=plt.cm.Paired,
                        s=20, edgecolor='k',
                        label="FAIH Class %s" % i)
    # 绘制knn图
    n = len(test_array)
    # 保存数据散点图
    plt.xlabel(u"Feature_1")
    plt.ylabel(u"Feature_2")
    plt.title(u"FAIH-KNN-Learning")
    plt.savefig("./Images/ML-SL-C-KNN-Scatter-%dP.jpg" % (n_points))
    # 绘制样本点
    for i in range(n):
        # 查看样本最近邻的k个数值位置
        #         point_array = test_array[i].reshape(1,-1)
        #         kneighbors = module.kneighbors(point_array,k)
        #         print(u'kneighbors数量: \n', kneighbors)
        # 绘制测试点
        plt.scatter(test_array[i][0], test_array[i][1], c='fuchsia', marker='*',s=70,
                    label='FAIH-ObjectivePoint%d (%.2f,%.2f)' % (i + 1, test_array[i][0], test_array[i][1]))
        plt.annotate("T%d point(%d,%d)" % (i + 1, test_array[i][0], test_array[i][1]),
                     (test_array[i][0], test_array[i][1]), xytext=(-20, 10), color='c', textcoords='offset points')
    plt.savefig("./Images/ML-SL-C-KNN-Scatter-%dP-%dT-%dnn-l1.jpg" % (n_points, n, k))

    for i in range(n):
        # 查看样本最近邻的k个数值位置
        point_array = test_array[i].reshape(1, -1)
        kneighbors = module.kneighbors(point_array, k)
        print(u'kneighbors数量: \n', len(kneighbors[0][0]))
        # 绘制测试点
        #         plt.scatter(test_array[i][0],test_array[i][1], c='r', marker='x',s=100,
        #                     label='FAIH-ObjectivePoint%d (%.2f,%.2f)' % (i+1,test_array[i][0],test_array[i][1]))
        # 绘制K最近邻范围圈
        for j in range(k):
            # 查看近邻点坐标
            index = kneighbors[1][0][j]
            x_index = X[:, 0][index]
            y_index = X[:, 1][index]
            label = y[index]
            # theta值
            theta = np.arange(0, 2 * np.pi, 0.01)
            # x范围
            x = np.linspace(test_array[i][0], x_index, 10000)
            # y范围
            y = np.linspace(test_array[i][1], y_index, 10000)
            plt.plot(np.ones(10000, ) * test_array[i][0], y + j / 10,
                     label='FAIH-%d-%d nearest neighbor range Manhattan Distance l1(%.2f, %.2f, %.0f)' % (
                     i + 1, j + 1, x_index, y_index, label))
            plt.plot(x + j / 10, np.ones(10000, ) * y_index)
            plt.annotate("%d-%s point" % (i + 1, j + 1), xy=(x_index, y_index), xytext=(-20, 10), color='m',
                         textcoords='offset points')
        # 绘制测试点注解说明
    #         plt.annotate("Test point for KNN (%.2f,%.2f)" % (test_array[i][0],test_array[i][1]),
    #                      (test_array[i][0],test_array[i][1]), xycoords='data', color='r',
    #                      xytext=(80,90),arrowprops=dict(arrowstyle='->'))

    # 绘制图例(起始点x，起始点y，长度，宽度)
    #     plt.legend(bbox_to_anchor=(0., 1.04, 1., 0.104),loc=3,ncol=2,mode='expand', borderaxespad=0.)
    plt.legend()
    # 保存图片
    plt.savefig("./Images/ML-SL-C-KNN-Scatter-%dP-%dT-%dnn-l1.png" % (n_points, n, k))
    # 显示图片
    plt.show();


def knn_plot_l2(n_points, X, y,module, test_array, k):
    # 训练最近邻分类器
    # knc = KNeighborsClassifier(p=1)
    # _ = knc.fit(X, y)
    # 绘制散点图
    module.set_params(p=2)
    plt.figure(figsize=(12, 12))

    if len(set(y)) == 1:
        # 绘制训练过程
        plt.scatter(X[:, 0], X[:, 1],
                    c="orange", cmap=plt.cm.Paired,
                    s=20, edgecolor='k',
                    label="FAIH Class 0")

    elif len(set(y)) == 2:
        # class_number = 2
        plot_colors = ["gold", "limegreen"]
        # 绘制训练过程
        for i, c in zip(range(2), plot_colors):
            idx = np.where(y == i)
            plt.scatter(X[idx, 0], X[idx, 1],
                        c=c, cmap=plt.cm.Paired,
                        s=20, edgecolor='k',
                        label="FAIH Class %s" % i)
    elif len(set(y)) == 3:
        # class_number = 2
        plot_colors = ["gold", "limegreen", "orangered"]
        # 绘制训练过程
        for i, c in zip(range(3), plot_colors):
            idx = np.where(y == i)
            plt.scatter(X[idx, 0], X[idx, 1],
                        c=c, cmap=plt.cm.Paired,
                        s=20, edgecolor='k',
                        label="FAIH Class %s" % i)

    # 保存数据散点图
    plt.xlabel(u"Feature_1")
    plt.ylabel(u"Feature_2")
    plt.title(u"FAIH-KNN-Learning")
    plt.savefig("./Images/ML-SL-C-KNN-Scatter-%dP.jpg" % (n_points))

    # 绘制knn图
    n = len(test_array)
    # 绘制样本点
    for i in range(n):
        # 绘制测试点
        plt.scatter(test_array[i][0], test_array[i][1], c='fuchsia', marker='*',s=70,
                    label='FAIH-ObjectivePoint%d (%.2f,%.2f)' % (i + 1, test_array[i][0], test_array[i][1]))
        plt.annotate("T%d point(%d,%d)" % (i + 1, test_array[i][0], test_array[i][1]),
                     (test_array[i][0], test_array[i][1]), xytext=(-20, 10), color='c', textcoords='offset points')
    # plt.savefig("./Images/ML-SL-C-KNN-Scatter-%dP-%dT-%dnn-l2.jpg" % (n_points, n, k))

    # for i in range(n):
        # 查看样本最近邻的k个数值位置
        point_array = test_array[i].reshape(1, -1)
        kneighbors = module.kneighbors(point_array, k)

        print(u'kneighbors数量: \n', len(kneighbors[0][0]))
        # 绘制测试点
        #         plt.scatter(test_array[i][0],test_array[i][1], c='r', marker='x',s=100,
        #                     label='FAIH-ObjectivePoint%d (%.2f,%.2f)' % (i+1,test_array[i][0],test_array[i][1]))
        # 绘制K最近邻范围圈
        for j in range(k):
            # 查看近邻点坐标
            index = kneighbors[1][0][j]
            x_index = X[:, 0][index]
            y_index = X[:, 1][index]
            label = y[index]

            # 绘制半径
            #             print(test_array[i])
            #             print([x_index,y_index])
            # plt.plot([test_array[i][0], x_index], [test_array[i][1], y_index], color='k')

            # 半径
            r = np.sqrt((test_array[i][0] - x_index)**2 + (test_array[i][1] - y_index)**2)
            # theta值
            theta = np.arange(0, 2 * np.pi, 0.01)
            # x范围
            x_cicle = test_array[i][0] + r * np.cos(theta)
            # y范围
            y_cicle = test_array[i][1] + r * np.sin(theta)
            plt.plot(x_cicle, y_cicle, label='FAIH-%d-%d nearest neighbor range Euclidean Distance l2(%.2f, %.2f, %.0f)' % (
            i + 1, j + 1, x_index, y_index, label))
            plt.annotate("%d-%s point" % (i + 1, j + 1), xy=(x_index, y_index), xytext=(-20, 10), color='m',
                         textcoords='offset points')
        # 绘制测试点注解说明
    #         plt.annotate("Test point for KNN (%.2f,%.2f)" % (test_array[i][0],test_array[i][1]),
    #                      (test_array[i][0],test_array[i][1]), xycoords='data', color='r',
    #                      xytext=(80,90),arrowprops=dict(arrowstyle='->'))

    # 绘制图例(起始点x，起始点y，长度，宽度)
    #     plt.legend(bbox_to_anchor=(0., 1.04, 1., 0.104),loc=3,ncol=2,mode='expand', borderaxespad=0.)
    plt.legend(loc=4)
    # 保存图片
    plt.savefig("./Images/ML-SL-C-KNN-Scatter-%dP-%dT-%dnn-l2.png" % (n_points, n, k))
    # 显示图片
    plt.show();
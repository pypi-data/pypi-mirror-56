from collections import namedtuple
from operator import itemgetter
from pprint import pformat
import matplotlib.pyplot as plt
import numpy as np

"""
from collections import namedtuple
————————————————
from collections import namedtuple
 
websites = [
    ('Sohu', 'http://www.google.com/', u'张朝阳'),
    ('Sina', 'http://www.sina.com.cn/', u'王志东'),
    ('163', 'http://www.163.com/', u'丁磊')
]
 
Website = namedtuple('Website', ['name', 'url', 'founder'])
 
for website in websites:
    website = Website._make(website)
    print website

————————————————
results:

Website(name='Sohu', url='http://www.google.com/', founder=u'\u5f20\u671d\u9633')
Website(name='Sina', url='http://www.sina.com.cn/', founder=u'\u738b\u5fd7\u4e1c')
Website(name='163', url='http://www.163.com/', founder=u'\u4e01\u78ca')

"""

class Node(namedtuple('Node', 'location left_child right_child')):
    def __repr__(self):
        return pformat(tuple(self))

#绘制kdtree
def kdtree_plt(point_list, depth_list, depth=0, lfOrRi=None, x_start=0, x_end=100, y_start=0, y_end=100):
    #如果没有点列表,
    if not point_list:
        return None
    #设置颜色区分
    colors = ['b', 'g', 'r', 'y', 'c', 'm', 'w']
    #如果当前深度在深度列表中
    if depth in depth_list:
        #不增加深度
        pass
    #否则列表增加当前深度
    else:
        depth_list.append(depth)
        #绘制深度线
        plt.plot(0, 0, label='The %dth split line' % (depth + 1), c=colors[depth % 7])
    #         plt.savefig("./Images/ML-SL-C-KNN-KDTree-%dP-Split-%ddepth.png" % (n_points,depth+1))

    #获取点的维度
    k = len(point_list[0])  # assumes all points have the same dimension假设所有点都具有相同的维度
    # Select axis based on depth so that axis cycles through all valid values
    #循环选取各个维度的轴作为拆分轴
    axis = depth % k

    # Sort point list by axis and choose median as pivot element
    #对点列表进行排序
    point_list.sort(key=itemgetter(axis))
    #     print("\n",point_list)
    #选择排序后的中间点
    median = len(point_list) // 2
    #根据选择点,选择点[维度]值作为拆分值
    staticValue = point_list[median][axis]
    #如果没有设置左或右作为拆分
    if lfOrRi is None:
        #获取中间点[0]维度值
        x_index = point_list[median][0]
        # y = np.linspace(x_start, x_end, 10000)
        #将y轴生成10000个区域
        y = np.linspace(y_start, y_end, 10000)
        #绘制这条线段
        plt.plot(np.ones(10000, ) * x_index, y, c=colors[depth % 7])

        return Node(
            #当前拆分点
            location=point_list[median],
            #左迭代
            left_child=kdtree_plt(point_list[:median], depth_list, depth + 1, 'l', x_start, staticValue, y_start,
                                  y_end),
            #右迭代
            right_child=kdtree_plt(point_list[median + 1:], depth_list, depth + 1, 'r', staticValue, x_end, y_start,
                                   y_end)
        )
    #如果迭代到左边
    elif lfOrRi == 'l':
        #且当前需要拆分的轴为y轴
        if axis == 1:
            #待划分的长度个数(这是和10000做比例的,我们的x轴y轴范围都是100长)
            length = int((x_end - x_start) * 100 // 1)
            #将x轴划分
            x = np.linspace(x_start, x_end, length)
            #找到y划分点
            y = point_list[median][axis]
            #绘制划分线
            plt.plot(x, np.ones(length, ) * y, c=colors[depth % 7])
            #再迭代拆分
            return Node(
                location=point_list[median],
                left_child=kdtree_plt(point_list[:median], depth_list, depth + 1, 'l', x_start, x_end, y_start,
                                      staticValue),
                right_child=kdtree_plt(point_list[median + 1:], depth_list, depth + 1, 'r', x_start, x_end, staticValue,
                                       y_end)
            )
        #且当前为x轴需要划分
        if axis == 0:
            length = int((y_end - y_start) * 100 // 1)
            y = np.linspace(y_start, y_end, length)
            x = point_list[median][axis]
            plt.plot(np.ones(length, ) * x, y, c=colors[depth % 7])
            return Node(
                location=point_list[median],
                left_child=kdtree_plt(point_list[:median], depth_list, depth + 1, 'l', x_start, staticValue, y_start,
                                      y_end),
                right_child=kdtree_plt(point_list[median + 1:], depth_list, depth + 1, 'r', staticValue, x_end, y_start,
                                       y_end)
            )

    #如果是右边来划分
    elif lfOrRi == 'r':
        #判断是y轴来划分
        if axis == 1:
            length = int((x_end - x_start) * 100 // 1)
            x = np.linspace(x_start, x_end, length)
            y = point_list[median][axis]
            plt.plot(x, np.ones(length, ) * y, c=colors[depth % 7])
            return Node(
                location=point_list[median],
                left_child=kdtree_plt(point_list[:median], depth_list, depth + 1, 'l', x_start, x_end, y_start,
                                      staticValue),
                right_child=kdtree_plt(point_list[median + 1:], depth_list, depth + 1, 'r', x_start, x_end, staticValue,
                                       y_end)
            )
        #判断是x轴来划分
        if axis == 0:
            length = int((y_end - y_start) * 100 // 1)
            y = np.linspace(y_start, y_end, length)
            x = point_list[median][axis]
            plt.plot(np.ones(length, ) * x, y, c=colors[depth % 7])
            return Node(
                location=point_list[median],
                left_child=kdtree_plt(point_list[:median], depth_list, depth + 1, 'l', x_start, staticValue, y_start,
                                      y_end),
                right_child=kdtree_plt(point_list[median + 1:], depth_list, depth + 1, 'r', staticValue, x_end, y_start,
                                       y_end)
            )

#生成KDTree图
def getKDTreeGraph(n_points, X, y,title_short,test_array=None):
    # 绘制样本点
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
            
    plt.plot(np.linspace(0, 100, 10000), np.ones(10000, ) * 0, c='k')  # 绘制底框
    plt.plot(np.linspace(0, 100, 10000), np.ones(10000, ) * 100, c='k')  # 绘制高框
    plt.plot(np.ones(10000, ) * 0, np.linspace(0, 100, 10000), c='k')  # 绘制左框
    plt.plot(np.ones(10000, ) * 100, np.linspace(0, 100, 10000), c='k')  # 绘制右框
    plt.xlabel(u"Feature_1")
    plt.ylabel(u"Feature_2")
    plt.title(u"FAIH-KNN-KDTree-Split")

    # 绘制所有样本点的图例
    for i in range(len(X)):
        plt.annotate("P%d" % (i + 1), xy=(X[i][0], X[i][1]), xytext=(-20, 10), color='m',
                     textcoords='offset points')

    # 将array转换为列表
    list_train = X.tolist()
    # 将嵌套的列表转换为元组
    lt_train = []
    for i in list_train:
        j = tuple(i)
        lt_train.append(j)
    # 查看树形结构
    depth_list = []
    kdtree_plt(lt_train, depth_list)
    if test_array==None:
        pass
    else:
        # 绘制待测点
        n = len(test_array)
        # 绘制样本点
        for i in range(n):
            # 绘制测试点
            plt.scatter(test_array[i][0], test_array[i][1], c='r', marker='x', s=100,
                        label='FAIH-ObjectivePoint%d (%.2f,%.2f)' % (i + 1, test_array[i][0], test_array[i][1]))
            plt.annotate("T%d point(%d,%d)" % (i + 1, test_array[i][0], test_array[i][1]),
                         (test_array[i][0], test_array[i][1]), xytext=(-20, 10), color='c', textcoords='offset points')
    # 绘制图
    plt.legend(bbox_to_anchor=(0., 1.04, 1., 0.104), loc=3, ncol=3, mode='expand', borderaxespad=0.)
    # 保存图片
    plt.savefig("./Images/ML-SL-C-%s-KDTree-%dP-Annotate-1T-Split.png" % (title_short,n_points))
    # 显示图片
    plt.show();

# # 生成数据,生成Knn图,可以将下方代码注释,以便统一数据散点图
# n_points, X_train, y_train = create_data(50, load=True)
# # 绘制样本点
# fig = plt.figure(figsize=(12, 12))
# plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=100)
# plt.plot(np.linspace(0, 100, 10000), np.ones(10000, ) * 0, c='k')  # 绘制底框
# plt.plot(np.linspace(0, 100, 10000), np.ones(10000, ) * 100, c='k')  # 绘制高框
# plt.plot(np.ones(10000, ) * 0, np.linspace(0, 100, 10000), c='k')  # 绘制左框
# plt.plot(np.ones(10000, ) * 100, np.linspace(0, 100, 10000), c='k')  # 绘制右框
# plt.xlabel(u"Feature_1")
# plt.ylabel(u"Feature_2")
# plt.title(u"FAIH-KNN-KDTree-Split")
#
# # 绘制所有样本点的图例
# for i in range(len(X_train)):
#     plt.annotate("P%d" % (i + 1), xy=(X_train[i][0], X_train[i][1]), xytext=(-20, 10), color='m',
#                  textcoords='offset points')
#
# # 将array转换为列表
# list_train = X_train.tolist()
# # 将嵌套的列表转换为元组
# lt_train = []
# for i in list_train:
#     j = tuple(i)
#     lt_train.append(j)
# # 查看树形结构
# depth_list = []
# kdtree_plt(lt_train, depth_list)
# plt.scatter(22, 42, c='r', marker='x', s=100, label='FAIH-ObjectivePoint')
# plt.annotate("FAIH-T1(22,42)", (22, 42), xytext=(-20, 10), color='r', textcoords='offset points')
# # 绘制图
# plt.legend(bbox_to_anchor=(0., 1.04, 1., 0.104), loc=3, ncol=3, mode='expand', borderaxespad=0.)
# # 保存图片
# plt.savefig("./Images/ML-SL-C-KNN-KDTree-%dP-Annotate-1T-Split.png" % (n_points))
# # 显示图片
# plt.show();
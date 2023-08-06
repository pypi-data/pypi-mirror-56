import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def plot3D(X,X_test, y_test,module,labels,delta,buff,title_class,title_short,extra_describe=[],function=False):
    extraDescribe = ""
    for i in extra_describe:
        extraDescribe += i
    #绘制图标尺寸
    fig = plt.figure(figsize=(12, 12))
    #加入3D图
    ax = Axes3D(fig)
    #将 delta 设置为 0.2，可避免生成太多的数据点, 加速生成效率
    # 生成代表X轴数据的列表
    x = np.arange(X[:, 0].min()-buff, X[:, 0].max()+buff, delta)
    # 生成代表Y轴数据的列表
    y = np.arange(X[:, 1].min()-buff, X[:, 1].max()+buff, delta)
    # 对x、y数据执行网格化
    x_new,y_new = np.meshgrid(x, y)
    # print(x_new)
    # print(x_new.shape)
    #根据X, Y生成Z1
    if not function:
        Z = function_module(module,x_new,y_new,X_test, y_test)
    else:
        Z = function(x_new,y_new)
    # 绘制3D图形
    ax.plot_surface(x_new,y_new, Z,
        rstride=1,  # rstride（row）指定行的跨度
        cstride=1,  # cstride(column)指定列的跨度
        cmap=plt.get_cmap('rainbow')  # 设置颜色映射
    #     cmap=plt.cm.Paired
                   )
    # 设置Z轴范围
    ax.set_zlim(Z.min()-(Z.max()-Z.min())/3,Z.max()+(Z.max()-Z.min())/3)
    #设置坐标轴label
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])
    # 设置标题
    plt.title("FAIH %s module 3D"%title_class)
    plt.savefig("./Images/FAIH-%sModule-3D%s.jpg"%(title_short,extraDescribe))
    plt.show()

def function_module(module,x,y,X_test, y_test):
    scores = np.zeros(x.shape)
    print(x.shape,y.shape)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            # print(i,j)
            module.coef_[0][0] = x[i][j]
            module.coef_[0][1] = y[i][j]
            # print(x[i][j],y[i][j])
            score = module.score(X_test, y_test)
            # print('测试集的预测准确率:  \n', score)
            scores[i][j] = -score
    return scores
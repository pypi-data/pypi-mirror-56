#导入数据
import matplotlib.pyplot as plt
import numpy as np
import os

#生成散点图
def scatter_plot(n_points, X, y,form, title_class, title_short,test_array=None,mlclass="ML-SL-C",extra_describe=[]):
    extraDescribe = ""
    for i in extra_describe:
        extraDescribe += i

    if not os.path.exists("./Images"):
        print("path not exists")
        os.makedirs("./Images")
    else:
        pass
    plt.figure(figsize=(12, 12))

    if len(set(y)) == 1:
        # 绘制训练过程
        plt.scatter(X[:, 0], X[:, 1],
                    c="orange", cmap=plt.cm.Paired,
                    s=20, edgecolor='k',
                    label="FAIH Class 0")

    elif len(set(y)) == 2:
        # class_number = 2
        plot_colors = ["gold","limegreen"]
        # 绘制训练过程
        for i, c in zip(range(2), plot_colors):
            idx = np.where(y == i)
            plt.scatter(X[idx, 0], X[idx, 1],
                        c=c, cmap=plt.cm.Paired,
                        s=20, edgecolor='k',
                        label="FAIH Class %s" % i)
    elif len(set(y)) == 3:
        # class_number = 2
        plot_colors = ["gold","limegreen","orangered"]
        # 绘制训练过程
        for i, c in zip(range(3), plot_colors):
            idx = np.where(y == i)
            plt.scatter(X[idx, 0], X[idx, 1],
                        c=c, cmap=plt.cm.Paired,
                        s=20, edgecolor='k',
                        label="FAIH Class %s" % i)

    # 打标签
    plt.xlabel(u"Feature_1")
    plt.ylabel(u"Feature_2")
    plt.title(u"FAIH-%s-Learning" % title_class)
    plt.legend(loc=0)
    plt.savefig("./Images/%s-%s-Scatter-%sForm-%dP%s.jpg" % (mlclass,title_short,form, n_points,extraDescribe))

    if test_array is None:
        pass
    else:
        #绘制待测点
        n = len(test_array)
        #绘制样本点
        for i in range(n):
            #绘制测试点
            plt.scatter(test_array[i][0],test_array[i][1], c='fuchsia', marker='*',s=70,
                        label='FAIH-ObjectivePoint%d (%.2f,%.2f)' % (i+1,test_array[i][0],test_array[i][1]))
            plt.annotate("P%d" % (i+1),
                         (test_array[i][0],test_array[i][1]), xytext=(-20, 10),color='black',textcoords='offset points')
        plt.savefig("./Images/%s-%s-Scatter-%sForm-%dP-%dT%s.jpg" % (mlclass,title_short,form,n_points,n,extraDescribe))
    # 显示图
    plt.legend(loc=0)
    plt.show();

def line_regression_plot(n_points, X, y,form, title_class, title_short,test_array=None,mlclass="ML-SL-R",extra_describe=[]):
    extraDescribe = ""
    for i in extra_describe:
        extraDescribe += i

    if not os.path.exists("./Images"):
        print("path not exists")
        os.makedirs("./Images")
    else:
        pass
    plt.figure(figsize=(12, 12))
    plt.scatter(X, y, c='gold', cmap=plt.cm.Paired,
                        s=20, edgecolor='k',
                        label="FAIH Data")
    # 打标签
    plt.xlabel(u"FAIH-x")
    plt.ylabel(u"FAIH-y")
    plt.title(u"FAIH-%s-Learning" % title_class)
    plt.legend(loc=0)
    plt.savefig("./Images/%s-%s-Linear-%sForm-%dP%s.jpg" % (mlclass,title_short, form, n_points,extraDescribe))
    if test_array==None:
        pass
    else:
        #绘制待测点
        n = len(test_array)
        #绘制样本点
        for i in range(n):
            #绘制测试点
            plt.scatter(test_array[i][0],test_array[i][1], c='fuchsia', marker='*',s=70,
                        label='FAIH-ObjectivePoint%d (%.2f,%.2f)' % (i+1,test_array[i][0],test_array[i][1]))
            plt.annotate("T%d point(%d,%d)" % (i+1,test_array[i][0],test_array[i][1]),
                         (test_array[i][0],test_array[i][1]), xytext=(-20, 10),color='c',textcoords='offset points')
        plt.savefig("./Images/%s-%s-Linear-%sForm-%dP-%dT%s.jpg" % (mlclass,title_short,form,n_points,n,extraDescribe))
    # 显示图
    plt.show();


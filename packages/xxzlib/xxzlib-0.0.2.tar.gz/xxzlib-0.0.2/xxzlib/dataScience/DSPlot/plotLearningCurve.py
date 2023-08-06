import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
import numpy as np

def plotLearningCurve(X, y,module,title_class,extra_describe=[]):
    extraDescribe = ""
    for i in extra_describe:
        extraDescribe += i
    #设置标题
    title = r"Learning Curves (%s)"%title_class
    #SVC相比上一个模型效率更高
    cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)
    #绘制得分曲线
    plot_learning_curve(module, title, X, y, (0.0, 1.01), cv=cv, n_jobs=2)
    plt.savefig("./Images/ML-SL-%s-LearningCurves%s.jpg" % (title_class,extraDescribe))
    plt.show()

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure(figsize=(12,12))
    #绘制标题
    plt.title(title)
    if ylim is not None:
        #设置y轴刻度
        plt.ylim(*ylim)
    #x轴标签
    plt.xlabel("Training examples")
    #y轴标签
    plt.ylabel("Score")
    #通过学习率曲线库生成相应的参数
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    #训练准确度的平均值
    train_scores_mean = np.mean(train_scores, axis=1)
    #训练准确度的方差
    train_scores_std = np.std(train_scores, axis=1)
    #测试准确度的平均值
    test_scores_mean = np.mean(test_scores, axis=1)
    #测试准确度的方差
    test_scores_std = np.std(test_scores, axis=1)
    #绘制网格
    plt.grid()
    #绘制训练线条填充阴影
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    #绘制测试线条填充阴影
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    #绘制训练学习率曲线
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    #绘制测试学习率曲线
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")
    #显示标签
    plt.legend(loc="best")
    return plt
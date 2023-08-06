#导入数据
import matplotlib.pyplot as plt
import numpy as np

#生成模型分界图
def module_performance(n_points, X, y,form, module,title_class,title_short,extra_describe=[]):
    extraDescribe = ""
    for i in extra_describe:
        extraDescribe += i
    # print(extraDescribe)
    # 开启新的绘图板
    plt.figure(figsize=(12, 12))
    # 设置绘图参数
    plot_step = 0.2
    # 绘制网络点坐标矩阵
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step), np.arange(y_min, y_max, plot_step))

    # xx.revel(),将(813, 725)铺平为(589425,)
    Z = module.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    # 将各个点绘制为
    plt.contourf(xx, yy, Z, cmap=plt.cm.summer)
    # plt.contourf(xx, yy, Z, cmap=plt.cm.Set2)
    plt.axis("tight")

    if len(set(y)) == 1:
        # 绘制训练过程
        plt.scatter(X[:, 0], X[:, 1],
                    c="orange", cmap=plt.cm.Paired,
                    s=20, edgecolor='k',
                    label="FAIH Class 0")

    # class_number = 2
    elif len(set(y)) == 2:
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

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.legend(loc=0)
    plt.title(u"FAIH-%s-Module"%title_class)
    plt.savefig("./Images/ML-SL-C-%s-Scatter-%sForm-%dP-Module%s.jpg" % (title_short,form, n_points,extraDescribe))

    #     #设置slover参数
    #     arg_solver = module.get_params()['solver']
    #     #设置C参数
    #     arg_c = module.get_params()['C']
    #     #设置max_iter参数
    #     arg_max_iter = module.get_params()['max_iter']
    #     #设置模型分类模式multi_class
    #     arg_multi_class = module.get_params()['multi_class']
    #     #设置并行计算的处理器个数
    #     arg_penalty = module.get_params()['penalty']

    #     plt.savefig("./Images/ML-SL-C-GNB-Scatter-%sForm-%dP-%sSolver-%sPenalty-%fC-%sMaxIter-%sMultipleClass%s.jpg" %
    #                 (form,n_points,arg_solver,arg_penalty,arg_c,arg_max_iter,arg_multi_class,extraDescribe))
    #     print("ML-SL-C-GNB-Scatter-%sForm-%dP-%sSolver-%sPenalty-%fC-%sMaxIter-%sMultipleClass%s.jpg" %
    #                 (form,n_points,arg_solver,arg_penalty,arg_c,arg_max_iter,arg_multi_class,extraDescribe))
    # 显示图
    plt.show();

#生成模型等高线性能图
def plt_contourf(n_points, X, y,form, module, score,title_class,title_short,extra_describe=[]):
    extraDescribe = ""
    for i in extra_describe:
        extraDescribe += i
    # 绘制等高线图
    # 开启新的绘图板
    plt.figure(figsize=(12, 12))
    # 绘制网络点坐标矩阵
    # 设置绘图参数
    plot_step = 0.2
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step), np.arange(y_min, y_max, plot_step))
    # 绘制决策边界,为此,我们将会分配颜色给每一个点(在网格中的[x_min, x_max]x[y_min, y_max])
    # 判断module是否包含`decision_function` 属性
    # 生成预测值
    if hasattr(module, "decision_function"):
        # np.c_合并后面的数据为坐标
        # .ravel()将数据平铺为一个列表
        Z = module.decision_function(np.c_[xx.ravel(), yy.ravel()])
    # elif hasattr(module, "predict"):
    #     Z = module.predict(np.c_[xx.ravel(), yy.ravel()])
    else:
        #
        Z = module.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

    # 给结果绘制颜色
    Z = Z.reshape(xx.shape)
    # print(Z)
    # 根据Z添加xx,yy平面的等高线
    cm = plt.cm.RdBu
    plt.contourf(xx, yy, Z, cmap=cm, alpha=.8)

    # 绘制训练数据点
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
                        # c=c, cmap=plt.cm.Set2,
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

    # 设置x轴边界
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    # 设置刻度
    plt.xticks(())
    plt.yticks(())
    plt.legend(loc=0)
    plt.title(u"FAIH-%s-Contour"%title_class)
    # 设置文字参数
    plt.text(xx.max() - .3, yy.min() + .3, ('FAIH-TestData-Score-%.2f' % score).lstrip('0'),
             size=12, horizontalalignment='right')
    plt.savefig("./Images/ML-SL-C-%s-Scatter-%sForm-%dP-Contour%s.jpg" % (title_short,form, n_points,extraDescribe))

    # 显示图
    plt.show();

#绘制回归模型的单线条
def linear_module(n_points, X, y, form, module, score, title_class, title_short, extra_describe=[],regression=None):
    extraDescribe = ""
    for i in extra_describe:
        extraDescribe += i

    if hasattr(module, "decision_function"):
        # np.c_合并后面的数据为坐标
        # .ravel()将数据平铺为一个列表
        Z = module.decision_function(np.c_[xx.ravel(), yy.ravel()])
    else:
        Z = module.predict(X)

    # 开启新的绘图板
    plt.figure(figsize=(12, 12))
    # 绘制散点图
    plt.scatter(X, y, c='r', cmap=plt.cm.Paired,
                        s=20, edgecolor='k',
                        label="FAIH Data")
    # plt.plot(X, y, 'r.', markersize=12)

    # 绘制模型线
    if regression == "DecisionTreeRegressor":
        plt.plot(X, Z, color="yellowgreen", linewidth=2)
    elif regression == "PolynomialRegression":
        plt.plot(X, Z, color="yellowgreen", linewidth=2)
    else:
        plt.plot(X, Z, 'b-')

    # 设置x轴边界
    #     plt.xlim(X.min(), X.max())
    #     plt.ylim(y.min(), y.max())
    # 设置刻度
    # plt.xticks(())
    # plt.yticks(())
    # 设置标记
    plt.xlabel(u"FAIH-x")
    plt.ylabel(u"FAIH-y")
    plt.legend(('FAIH-RegressionFit','FAIH-Data'), loc=0)
    plt.title(u"FAIH-%s-Contour" % title_class)
    # 设置文字参数
    plt.text(X.max() - .3, y.min() + .3, ('FAIH-TestData-Score-%.2f' % score).lstrip('0'),
             size=12, horizontalalignment='right')
    plt.savefig("./Images/ML-SL-R-%s-Scatter-%sForm-%dP-Contour%s.jpg" % (title_short, form, n_points, extraDescribe))

    # 显示图
    plt.show();

#决策树图
def DecisionTreeRegressionPlot(n_points, X, y, form, module, score, title_class, title_short, extra_describe=[]):
    extraDescribe = ""
    for i in extra_describe:
        extraDescribe += i
    if hasattr(module, "decision_function"):
        # np.c_合并后面的数据为坐标
        # .ravel()将数据平铺为一个列表
        Z = module.decision_function(np.c_[xx.ravel(), yy.ravel()])
    else:
        Z = module.predict(X)
    # 开启新的绘图板
    plt.figure(figsize=(12, 12))
    # 绘制散点图
    plt.scatter(X, y, c='r', cmap=plt.cm.Paired,
                        s=20, edgecolor='k',
                        label="FAIH Data")
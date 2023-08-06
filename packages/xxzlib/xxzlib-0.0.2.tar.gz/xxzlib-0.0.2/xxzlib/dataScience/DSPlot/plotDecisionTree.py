import pydotplus
from IPython.display import display, Image
from sklearn.tree import export_graphviz

#绘制树结构图
def plotDecisionTreeMap(n_points,form,module,title_short,extra_describe=[]):
    extraDescribe = ""
    for i in extra_describe:
        extraDescribe += i
    # for i in range(module.n_features_):
    feature_names_list = ["feature_%d"%(i+1) for i in range(module.n_features_)]
    print("The all features number is : %d   \nThe number of feature used is : %d"%(module.max_features_,module.n_features_))
    dot_data = export_graphviz(module,
                                out_file=None,
                                feature_names=feature_names_list,
                               #设置填充
                                filled = True,
                               #设置圆角
                                rounded =True
                                   )

    graph = pydotplus.graph_from_dot_data(dot_data)
    img = Image(graph.create_png())
    display(img)
    graph.write_png("./Images/ML-SL-%s-Scatter-%sForm-%dP-Structure%s.png" % (title_short, form, n_points, extraDescribe))
# -*- coding: utf-8 -*-

# @Time    : 2019/10/30 21:46
# @Email   : 986798607@qq.ele_ratio
# @Software: PyCharm
# @License: BSD 3-Clause


import warnings

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle

from featurebox.tools.exports import Store
from featurebox.tools.imports import Call
from featurebox.tools.quickmethod import dict_method_reg

warnings.filterwarnings("ignore")

"""
this is a description
"""

if __name__ == '__main__':
    store = Store(r'C:\Users\Administrator\Desktop\band_gap_exp\3.sum')
    data = Call(r'C:\Users\Administrator\Desktop\band_gap_exp')
    data_import = data.csv.all_import
    name_init, abbr_init = data.name_and_abbr

    select = ['destiny', 'energy cohesive brewer', 'distance core electron(schubert)']  # 3
    # select = ['destiny', 'distance core electron(schubert)', 'valence electron number'] #13
    # select = [ 'destiny', 'charge nuclear effective(slater)','electronegativity(martynov&batsanov)'] # 28
    # select = ['destiny', 'electronegativity(martynov&batsanov)']

    select = ['destiny'] + [j + "_%i" % i for j in select[1:] for i in range(2)]

    data216_import = data_import.iloc[np.where(data_import['group_number'] == 216)[0]]
    data225_import = data_import.iloc[np.where(data_import['group_number'] == 225)[0]]
    data216_225_import = pd.concat((data216_import, data225_import))

    X_frame = data225_import[select]
    y_frame = data225_import['exp_gap']

    X = X_frame.values
    y = y_frame.values

    scal = preprocessing.MinMaxScaler()
    X = scal.fit_transform(X)
    X, y = shuffle(X, y, random_state=5)

    from sklearn.model_selection import train_test_split

    X_train, _X_reserved_test, y_train, _y_reserved_test = train_test_split(X, y, test_size=0.25, random_state=2)
    X, y = X_train, y_train

    method_name = ["GPR-set", "SVR-set", 'KRR-set', "KNR-set"]
    pre_y_all = []
    for i in method_name:
        me1, cv1, scoring1, param_grid1 = method = dict_method_reg()[i]
        scoring1 = "r2"
        estimator = GridSearchCV(me1, cv=cv1, scoring=scoring1, param_grid=param_grid1, n_jobs=1)
        estimator.fit(X, y)

        test_pre = estimator.predict(_X_reserved_test)
        y_train_pre = estimator.predict(X_train)

        pre_y_all.append(test_pre)

        score1 = estimator.best_score_

        score2 = r2_score(_y_reserved_test, test_pre)

        print(score1)
        print(score2)
        #
        # p = BasePlot()
        # p.scatter(y_train, y_train_pre, strx='$E_{gap}$ true', stry='$E_{gap}$ calculated')
        # p.scatter(_y_reserved_test, test_pre, strx='$E_{gap}$ true', stry='$E_{gap}$ calculated')
        # plt.show()
        # p.scatter(sc[:, 0], sc[:, 1], strx='number', stry='score')
        # plt.show()

    pre = np.array(pre_y_all)
    # test2
    # data216_import = data_import.iloc[np.where(data_import['group_number'] == 216)[0]]

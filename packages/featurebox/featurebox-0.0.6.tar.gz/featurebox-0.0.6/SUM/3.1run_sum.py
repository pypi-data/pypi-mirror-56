import re
import warnings
from collections import Counter

import numpy as np
import pandas as pd
from sklearn import preprocessing, utils
from sklearn.model_selection import GridSearchCV

from featurebox.selection.sum import SUM
from featurebox.tools.exports import Store
from featurebox.tools.imports import Call
from featurebox.tools.quickmethod import dict_method_reg
from featurebox.tools.tool import name_to_name

warnings.filterwarnings("ignore")

if __name__ == '__main__':
    store = Store(r'C:\Users\Administrator\Desktop\band_gap_exp\3.sum\10times')
    data = Call(r'C:\Users\Administrator\Desktop\band_gap_exp\3.sum\method',
                r'C:\Users\Administrator\Desktop\band_gap_exp')
    data_import = data.csv.all_import
    name_init, abbr_init = data.name_and_abbr

    select = ['volume', 'destiny', 'lattice constants a', 'lattice constants c', 'radii covalent',
              'radii ionic(shannon)',
              'distance core electron(schubert)', 'latent heat of fusion', 'energy cohesive brewer', 'total energy',
              'charge nuclear effective(slater)', 'valence electron number', 'electronegativity(martynov&batsanov)',
              'volume atomic(villars,daams)']

    select = ['volume', 'destiny'] + [j + "_%i" % i for j in select[2:] for i in range(2)]

    data216_import = data_import.iloc[np.where(data_import['group_number'] == 216)[0]]
    data225_import = data_import.iloc[np.where(data_import['group_number'] == 225)[0]]
    data216_225_import = pd.concat((data216_import, data225_import))

    X_frame = data225_import[select]
    y_frame = data225_import['exp_gap']
    # #
    parto = []
    table = []
    for i in range(10):
        print(i)
        X = X_frame.values
        y = y_frame.values

        scal = preprocessing.MinMaxScaler()
        X = scal.fit_transform(X)
        X, y = utils.shuffle(X, y, random_state=i)
        #### X,y = utils.resample(X,y,replace=True,random_state=i)

        # from sklearn.model_selection import train_test_split
        # sample = 0
        # test_size = 1-sample
        # X_train, _X_reserved_test, y_train, _y_reserved_test = train_test_split(X, y, test_size=test_size, random_state=i)
        # X, y = X_train, y_train

        """base_method"""
        method_name = ['GPR-set', 'SVR-set', 'KRR-set', 'KNR-set', 'GBR-em', 'AdaBR-em', 'RFR-em', "DTR-em"]

        index_all = [data.pickle_pd.GPR_set23, data.pickle_pd.SVR_set23, data.pickle_pd.KRR_set23]

        estimator_all = []
        for i in method_name:
            me1, cv1, scoring1, param_grid1 = dict_method_reg()[i]
            estimator_all.append(GridSearchCV(me1, cv=cv1, scoring=scoring1, param_grid=param_grid1, n_jobs=1))

        """union"""
        # [print(_[0]) for _ in index_all]
        index_slice = [tuple(index[0]) for _ in index_all for index in _[:50]]
        index_slice = list(set(index_slice))

        """get x_name and abbr"""
        index_all_name = name_to_name(X_frame.columns.values, search=[i for i in index_slice],
                                      search_which=0, return_which=(1,), two_layer=True)

        index_all_name = [list(set([re.sub(r"_\d", "", j) for j in i])) for i in index_all_name]
        [i.sort() for i in index_all_name]
        index_all_abbr = name_to_name(name_init, abbr_init, search=index_all_name, search_which=1, return_which=2,
                                      two_layer=True)

        """run"""
        self = SUM(estimator_all, index_slice, estimator_n=[0, 1, 2,3,4,5,6,7], n_jobs=4)
        self.fit(X, y)
        mp = self.pareto_method()
        partotimei = list(list(zip(*mp))[0])

        tabletimei = np.vstack([self.resultcv_score_all_0, self.resultcv_score_all_1, self.resultcv_score_all_2])

        parto.extend(partotimei)
        table.append(tabletimei)

    parto = Counter(parto)
    select_index = list(parto.keys())
    table = np.array(table)
    tables = table.reshape((-1, table.shape[2]), order="F").T
    select_support = np.zeros(len(index_slice))
    select_support[select_index] = 1

    store.to_txt(select_index, "select_index")
    store.to_csv(select_support, "select_support")
    store.to_csv(tables, "100_times_score")

    store.to_pkl_pd(index_slice, "index_all")
    store.to_csv(index_all_name, "index_all_name")
    store.to_csv(index_all_abbr, "index_all_abbr")
    store.to_txt(parto, "parto")
    means_y = np.mean(table, axis=0).T
    store.to_csv(means_y, "means_y")

    select_support = np.zeros(len(index_slice))

    mean_parto_index = self._pareto(means_y)

    select_support[mean_parto_index] = 1
    store.to_csv(select_support, "mean_select_support")

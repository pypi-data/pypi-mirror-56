
# coding: utf-8

# In[1]:

def lgb_classifier(df, df_test, target, date = None, encoding = ['label', 'frequency', 'target', 'dummy'], metric = 'auc', nfold = 5, init_points = 15, n_iter = 5):
    
    """ 
    train a lightgbm classifier with categorical encoding and tune parameters with bayesian optimization 
    
    :param df: training set
    :param df_test: test set
    :param target: name of binary label
    :param date: list of names of datetime features
    :param encoding: list of categorical encoding methods to apply
    :param metric: 'auc', 'gini_lgb', 'cross_entropy' and any other metrics for lightgbm classifier
    :param nfold: number of cross validation folds
    :param init_points: number of random points for initialization of bayesian optimization
    :param n_iter: number of bayesian optimization iterations after initialization, total number of iteration of bayesian optimization algorithm would be init_points + n_iter
    :type df: pandas data frame
    :type df_test: pandas data frame
    :type target: str
    :type date: list of str
    :type metric: str
    :type nfold: int
    :type init_points: int
    :type n_iter: int
    :returns: test set prediction, cross validation set performace, k-fold lgb models, processed training set, processed test set
    :rtype: data frame of shape (n,1), float, list, data frame, data frame
    """
    
    import numpy as np
    import pandas as pd
#     import seaborn as sns
#     import matplotlib.pyplot as plt
    from sklearn.model_selection import train_test_split, StratifiedKFold
    from sklearn.utils import shuffle
    from sklearn.metrics import mean_squared_error, mean_absolute_error, auc, roc_curve
    from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
    from sklearn.ensemble import RandomForestClassifier
    import lightgbm as lgb
    from bayes_opt import BayesianOptimization
#     import shap
#     from sklearn.naive_bayes import GaussianNB
    from datetime import datetime as dt
#     import os
    from collections import OrderedDict

    # load data and shuffle
    np.random.seed(100)
    df1 = df
    df2 = df_test
    df1 = shuffle(df1).reset_index(drop = True)

    # date features
    dates = [c for c in df1.columns if 'datetime' in str(df1[c].dtype)]
    if date and type(date) == str:
        date = [date]
    if date:
        dates += date
        dates = list(OrderedDict.fromkeys(dates).keys())

    # utility function to guess date formats    
    def get_date(s_date):
        date_patterns = ['%d-%m-%Y', '%Y-%m-%d', '%m-%d-%Y', '%d/%m/%Y', '%Y/%m/%d', '%m/%d/%Y']
        for pattern in date_patterns:
            try:
                return pd.to_datetime(s_date, format = pattern)
                break
            except:
                pass
        return s_date
    
    # covnert date to timestamp(int)
    for c in dates:    
        if 'datetime' not in str(df1[c].dtype):
            df1[c] = get_date(df1[c])
            df2[c] = get_date(df2[c])
        df1[c] = [dt.timestamp(i) for i in df1[c]]
        df2[c] = [dt.timestamp(i) for i in df2[c]]

    cats = [c for c in df1.columns if df1[c].dtype == 'object' and c != target]
    nums = [c for c in df1.columns if df1[c].dtype != 'object' and c != target]
    feats = [c for c in df1.columns if c != target]

    # fill missing value
    for c in cats:
        df1[c] = df1[c].fillna('NaN')
    for c in nums:
        df1[c] = df1[c].fillna(df1[c].mean())


    for c in cats:
        df2[c] = df2[c].fillna('NaN')
    for c in nums:
        df2[c] = df2[c].fillna(df2[c].mean())

    # label encoder
    if 'lable' in encoding:
        # train
        lbls = {}
        for c in cats:
            lbl = LabelEncoder()
            lbl.fit(df1[c])
            df1[c + '_lbl'] = lbl.transform(df1[c])
            lbls[c] = lbl

        # test
        for c in cats:
            lbl_map = {val: label for label, val in enumerate(lbls[c].classes_)}
            df2[c + '_lbl'] = df2[c].map(lbl_map)
            # fillna and convert to int
            df2[c + '_lbl'] = df2[c + '_lbl'].fillna(-1).astype(int)

        cats_lbl = [c for c in df1.columns if '_lbl' in c]
    else:
        cats_lbl = []

    # frequency encoding
    if 'frequency' in encoding:
        for c in cats:
            df1[c + '_freq'] = df1[c].map(df1[c].value_counts())

        for c in cats:
            df2[c + '_freq'] = df2[c].map(df1[c].value_counts())

        cats_freq = [c for c in df1.columns if '_freq' in c]
    else:
        cats_freq = []

    # k-fold target encoding
    if 'target' in encoding:
        kf =  StratifiedKFold(n_splits = nfold, random_state = 100, shuffle = False)
        for t, v in kf.split(df1.drop(target, axis = 1), df1[target]):
            train, valid = df1.iloc[t], df1.iloc[v]
            for c in cats:
                df1.loc[df1.index[v], c + '_mean'] = valid[c].map(train.groupby(c)[target].mean())

        for c in cats:
            df2.loc[:, c + '_mean'] = df2[c].map(df1.groupby(c)[target].mean())

        cats_mean = [c for c in df1.columns if '_mean' in c]
    else:
        cats_mean = []
        
    # one hot encoding for training set
    if 'dummy' in encoding:
        df1 = pd.get_dummies(df1, prefix_sep="__")
        cols_dummy = [col for col in df1 if "__" in col]
        cols = [i for i in list(df1.columns.values) if i != target]

        cats_dummy = [col for col in df1 if "__" in col]

        # one hot encoding for test set
        df2 = pd.get_dummies(df2, prefix_sep="__")

        # remove additional columns
        for col in df2.columns:
            if ("__" in col) and col not in cols_dummy:
                df2.drop(col, axis=1, inplace=True)

        # add missing columns
        for col in cols_dummy:
            if col not in df2.columns:
                df2[col] = 0

        df2 = df2[cols]
    else:
        cats_dummy = []
        
    if cats[0] in df1.columns:
        df1 = df1.drop(cats, axis = 1)
        df2 = df2.drop(cats, axis = 1)

    df1 = df1.fillna(df1.mean())
    df2 = df2.fillna(df2.mean())
    
    # utility function: gini index
    def gini(pred, actual):
        assert (len(actual) == len(pred))
        all = np.asarray(np.c_[actual, pred, np.arange(len(actual))], dtype=np.float)
        all = all[np.lexsort((all[:, 2], -1 * all[:, 1]))]
        totalLosses = all[:, 0].sum()
        giniSum = all[:, 0].cumsum().sum() / totalLosses

        giniSum -= (len(actual) + 1) / 2.
        return giniSum / len(actual)

    # utility function: normalized gini
    def gini_normalized(pred, actual):
        return gini(pred, actual) / gini(actual, actual)

    # gini index for lightgbm (Custom metric), return: eval_name, val, is_higher_better
    def gini_lgb(pred_y, valid_y):
        valid_y = valid_y.get_label()
        assert (len(valid_y) == len(pred_y))
        all = np.asarray(np.c_[valid_y, pred_y, np.arange(len(valid_y))], dtype=np.float)
        all = all[np.lexsort((all[:, 2], -1 * all[:, 1]))]
        totalLosses = all[:, 0].sum()
        giniSum = all[:, 0].cumsum().sum() / totalLosses

        giniSum -= (len(valid_y) + 1) / 2.
        return 'gini', giniSum / len(valid_y), True

    np.random.seed(100)
    feats_lgb = nums + cats_lbl + cats_freq + cats_mean + cats_dummy
    kf = StratifiedKFold(n_splits = nfold, random_state = 100, shuffle = False)

    # error correction for metric variable inputs
    metric = 'gini_lgb' if metric == 'gini' else metric
    
    def gbm_eval(
                learning_rate = 0.1, \
                num_leaves = 100, \
                feature_frac = 0.95, \
                bagging_frac = 0.95, \
                min_data_in_leaf = 1, \
                max_depth = -1, \
                max_bin = 255, \

                min_sum_hessian_in_leaf = 0.001, \
                min_gain_to_split = 0, \
                lambda_l1 = 0, \
                lambda_l2 = 0):
        params = {
                    'boosting': 'gbdt',
                    'objective': 'binary',
                    'metric': metric,
                    'learning_rate': 0.1,
                    'num_leaves': int(round(num_leaves)),
                    'feature_frac': feature_frac,
                    'bagging_frac': bagging_frac,
                    'min_data_in_leaf': int(round(min_data_in_leaf)),
                    'max_depth': int(round(max_depth)),
                    'max_bin': int(round(max_bin)),

                    'min_sum_hessian_in_leaf': min_sum_hessian_in_leaf,
                    'min_gain_to_split': int(round(min_gain_to_split)),
                    'lambda_l1': lambda_l1,
                    'lambda_l2': lambda_l2,
                    'is_unbalance': True
                }
        
        if metric == 'auc':
            gbm_cv = lgb.cv(params,
                            lgb.Dataset(df1[feats_lgb + [target]].drop(target, axis = 1), df1[target]),
                            folds = kf.split(df1[feats_lgb + [target]].drop(target, axis = 1), df1[target]),
                            num_boost_round = 1000,
                            early_stopping_rounds = 100)
        elif metric == 'gini_lgb':
            gbm_cv = lgb.cv(params,
                            lgb.Dataset(df1[feats_lgb + [target]].drop(target, axis = 1), df1[target]),
                            folds = kf.split(df1[feats_lgb + [target]].drop(target, axis = 1), df1[target]),
                            num_boost_round = 1000,
                            early_stopping_rounds = 100,
                            feval = gini_lgb)
        
        return max(gbm_cv['gini-mean' if metric == 'gini_lgb' else metric + '-mean'])

    optimizer = BayesianOptimization(gbm_eval, 
                                     {
                                        'num_leaves': (2, 120),
                                        'feature_frac': (0.01, 0.99),
                                        'bagging_frac': (0.01, 0.99),
                                        'min_data_in_leaf': (1,10),
                                        'max_depth': (-1.1, 7),
                                        'max_bin': (63,511)

#                                         'min_sum_hessian_in_leaf': (0.001, 0.01),
#                                         'min_gain_to_split': (0, 1),
#                                         'lambda_l1': (0, 1),
#                                         'lambda_l2': (0, 1)
                                    },
                                     random_state = 100)


    optimizer.maximize(init_points = init_points, n_iter = n_iter, acq = 'ei')

    params_bayes = {
                    'boosting': 'gbdt',
                    'objective': 'binary',
                    'metric': metric,
                    'learning_rate': 0.1,
                    'num_leaves': int(round(optimizer.max['params']['num_leaves'])),
                    'feature_frac': optimizer.max['params']['feature_frac'],
                    'bagging_frac': optimizer.max['params']['bagging_frac'],
                    'min_data_in_leaf': int(round(optimizer.max['params']['min_data_in_leaf'])),
                    'max_depth': int(round(optimizer.max['params']['max_depth'])),
                    'max_bin': int(round(optimizer.max['params']['max_bin'])),
                    'is_unbalance': True # deal with imbalaced data
                   }

    params = params_bayes

    np.random.seed(100)
    feats_lgb = nums + cats_lbl + cats_freq + cats_mean + cats_dummy

    pred_y = np.zeros(df1.shape[0])
    gbms = list()
    kf = StratifiedKFold(n_splits = nfold, random_state = 100, shuffle = False)
    res = []
    idx = []
    for t, v in kf.split(df1[feats_lgb + [target]].drop(target, axis = 1), df1[target]):
        train_X, train_y = df1[feats_lgb + [target]].drop(target, axis = 1).iloc[t], df1[target].iloc[t]
        valid_X, valid_y = df1[feats_lgb + [target]].drop(target, axis = 1).iloc[v], df1[target].iloc[v]
        train_lgb = lgb.Dataset(train_X, train_y)
        valid_lgb = lgb.Dataset(valid_X, valid_y, reference = train_lgb)
        if metric == 'auc':
            gbm = lgb.train(params,
                       train_lgb,
                       valid_sets = [train_lgb, valid_lgb],
                       num_boost_round = 1000,
                       early_stopping_rounds = 100)
        elif metric == 'gini_lgb':
            gbm = lgb.train(params,
                       train_lgb,
                       valid_sets = [train_lgb, valid_lgb],
                       num_boost_round = 1000,
                       early_stopping_rounds = 100,
                       feval = gini_lgb)
        pred_y[v] = gbm.predict(valid_X, num_iteration = gbm.best_iteration)
        if metric == 'auc':
            fpr, tpr, thresholds = roc_curve(df1[target][v], pred_y[v], pos_label=1)
            res.append(auc(fpr, tpr))
        elif metric == 'gini_lgb':
            res.append(gini(pred_y[v], df1[target][v]))
        idx.append(v)
        gbms.append(gbm)   
        
    fpr, tpr, thresholds = roc_curve(df1[target], pred_y, pos_label=1)

    print('GINI index CV is {0:.6f}'.format(gini(pred_y, df1[target])))

    print('Normalized GINI index CV is {0:.6f}'.format(gini_normalized(pred_y, df1[target])))

    print('AUC CV is {0:.6f}'.format(auc(fpr, tpr)))
        
    score_cv = {'auc': auc(fpr, tpr), 'gini': gini(pred_y, df1[target])}
        
        
    n_gbms = len(gbms)
    pred_y_sub = np.array([0.] * df2.shape[0])
    for gbm in gbms:
        pred_y_sub += gbm.predict(df2[feats_lgb], num_iteration = gbm.best_iteration) / n_gbms
#     filename = 'submission/subm_{}_{:.6f}_{}_{}.csv'.format('Gini', gini(pred_y, df1[target]), 'LGBM', dt.now().strftime('%Y-%m-%d-%H-%M'))

#     sub = pd.DataFrame({'RefId':df2['RefId'], target:pred_y_sub})
#     sub.to_csv(filename, index = False)
    sub = pd.DataFrame({target:pred_y_sub})
    
    return sub, score_cv, gbms, df1, df2


# In[ ]:




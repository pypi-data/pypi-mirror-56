import numpy as np
import pandas as pd
import catboost as cbt
from sklearn.metrics import accuracy_score, roc_auc_score,log_loss
import gc
import math
import time
from tqdm import tqdm
import datetime 
from sklearn.model_selection import KFold,StratifiedKFold
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import warnings
import os
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from lightgbm import LGBMClassifier
from catboost import Pool, CatBoostRegressor
from scipy import stats
import pickle
from sklearn.externals import joblib

from sklearn.metrics import mean_squared_error
import seaborn as sns

from sklearn.metrics import accuracy_score
import math
import copy as cp
from sklearn.decomposition import PCA
import sklearn.preprocessing as preprocessing
scaler = preprocessing.StandardScaler()
warnings.filterwarnings('ignore')
pd.options.display.max_columns = None
pd.options.display.max_rows = None


from catboost import Pool, CatBoostRegressor
import xgboost as xgb
import lightgbm as lgb
from pylab import rcParams


def rmsle(y, y_pred):
    return np.sqrt(mean_squared_error(y, y_pred))


def sum_model(c_model):
    if c_model == 'cat':            
        cbt_model = joblib.load("cbt_model.m")         
        oof = cbt_model.predict_proba(train_x_lgb)
        prediction = cbt_model.predict_proba(test_x_lgb)
        
    elif c_model == 'lgb':

        #######lightgbm
        params = {
        'boosting_type': 'gbdt',
        'objective': 'multiclass',
        'num_class': 4,  
        'metric': 'multi_error', 
        'num_leaves': 63,
        'learning_rate': 0.01,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.9,
        'bagging_seed':0,
        'bagging_freq': 1,
        'verbose': -1,
        'reg_alpha':1,
        'reg_lambda':2,
        'lambda_l1': 0,
        'lambda_l2': 1,
        'num_threads': 8,
        }
        lgb_train = lgb.Dataset(train_x1, train_y)
        print(type(lgb_train))
        gbm = lgb.train(params,
                        lgb_train,
                        num_boost_round=2800,#跑的轮数
                        valid_sets=[lgb_train],
                        valid_names=['train'],
                        verbose_eval=100,#每隔100次显示一次
                        )
        f=open("./lgb.csv","w")
        oof = gbm.predict(train_x1)
        prediction=gbm.predict(test_x1, num_iteration=1300)
    else:
        pass
    return oof,prediction

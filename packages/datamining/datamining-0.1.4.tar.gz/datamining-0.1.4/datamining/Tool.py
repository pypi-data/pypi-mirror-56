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


%matplotlib inline
plt.rcParams['figure.figsize'] = (12.0, 8.0) # 调整大小，可根据自实际情况进行设置
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'
plt.rcParams['font.sans-serif']=['SimHei']  # 下面这两个是设置乱码的
plt.rcParams['axes.unicode_minus']=False
plt.style.use('ggplot')  # 使用'ggplot'风格美化显示的图表

from pylab import rcParams ##matplotlib
rcParams['figure.figsize'] = 12, 8



train_sum = pd.read_csv('./first_round_training_data.csv')


# train['label'] = train['Quality_label'].map({
#     'Excellent':0,
#     'Good':1,
#     'Pass':2,
#     'Fail':3
# })

# train = pd.get_dummies(train, columns=['Quality_label'])

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
# train_sum['Parameter5'] = train_x1['Parameter5']
# train_sum['Parameter6'] = train_x1['Parameter6']
# train_sum['Parameter7'] = train_x1['Parameter7']
# train_sum['Parameter8'] = train_x1['Parameter8']
# train_sum['Parameter9'] = train_x1['Parameter9']
# train_sum['Parameter10'] = train_x1['Parameter10']
train_sum['label'] = train_sum['Quality_label'].map({
    'Excellent':0,
    'Good':1,
    'Pass':2,
    'Fail':3
})


train_sum['Attribute1'] = np.log(train_sum['Attribute1'])


train_x_lgb = pd.read_csv('./train_x_lgb.csv')
test_x_lgb = pd.read_csv('./test_x_lgb.csv')



train_x_lgb = train_x_lgb.iloc[:,2:]
test_x_lgb = test_x_lgb.iloc[:,2:]





def rmsle(y, y_pred):
    return np.sqrt(mean_squared_error(y, y_pred))


from catboost import Pool, CatBoostRegressor
import xgboost as xgb
import lightgbm as lgb
#CatBoostRegressor
train_pool = Pool(train_x_lgb, train_sum['Attribute1']) 
test_pool = Pool(test_x_lgb)
cbm0 = CatBoostRegressor(rsm=0.8, depth=7, learning_rate=0.5, eval_metric='RMSE')

#XGBRegressor
boost_params = {'eval_metric': 'rmse'}
xgb0 = xgb.XGBRegressor(
    max_depth=8,
    learning_rate=0.1,
    n_estimators=1000,
    objective='reg:linear',
    gamma=0,
    min_child_weight=1,
    subsample=1,
    colsample_bytree=1,
    scale_pos_weight=1,
    seed=27,
    **boost_params)

#LGBMRegressor
gbm0 = lgb.LGBMRegressor(
    objective='regression',
    num_leaves=60,
    learning_rate=0.1,
    n_estimators=1000)

print("Fitting CatBoostRegressor model...")
cbm0.fit(train_pool)

print("Finished fitting CatBoostRegressor model")

print("Fitting XGBRegressor model...")
xgb0.fit(train_x_lgb, train_sum['Attribute1'])

print("Finished fitting XGBRegressor model")

print("Fitting LGBMRegressor model...")
gbm0.fit(train_x_lgb, train_sum['Attribute1'], eval_metric='rmse')

print("Finished fitting LGBMRegressor model")


# s = pickle.dumps(cbm0)
# cbm1 = pickle.loads(s)
joblib.dump(cbm0, "cbm0.m")



# s1 = pickle.dumps(xgb0)
# xgb1 = pickle.loads(s1)
joblib.dump(xgb0, "xgb0.m")


# s2 = pickle.dumps(gbm0)
# gbm1 = pickle.loads(s2)
joblib.dump(gbm0, "gbm0.m")


# predict_train1 = gbm0.predict(train_x1)
# print(rmsle(train_sum['Attribute1'], predict_train1))


# predict_train2 = xgb0.predict(train_x1)
# print(rmsle(train_sum['Attribute1'], predict_train2))


# predict_train3 = cbm0.predict(train_pool)
# print(rmsle(train_sum['Attribute1'], predict_train3))


# predict_test1 = gbm0.predict(test_x1)
# predict_test2 = xgb0.predict(test_x1)

# predict_test3 = cbm0.predict(test_pool)
# predict_train11 = (predict_train1 + predict_train2 + predict_train3)/3
# predict_test11 = (predict_test1 + predict_test2 + predict_test3)/3

#保存模型


cbm0 = joblib.load("cbm0.m")
xgb0 = joblib.load("xgb0.m")
gbm0 = joblib.load("gbm0.m")


predict_train1 = gbm0.predict(train_x_lgb)
print(rmsle(train_sum['Attribute1'], predict_train1))


predict_train2 = xgb0.predict(train_x_lgb)
print(rmsle(train_sum['Attribute1'], predict_train2))


predict_train3 = cbm0.predict(train_pool)
print(rmsle(train_sum['Attribute1'], predict_train3))


predict_test1 = gbm0.predict(test_x_lgb)
predict_test2 = xgb0.predict(test_x_lgb)

predict_test3 = cbm0.predict(test_pool)
predict_train11 = (predict_train1 + predict_train2 + predict_train3)/3
predict_test11 = (predict_test1 + predict_test2 + predict_test3)/3


print("RMSE: %.2f"
      % math.sqrt(np.mean((predict_train11 - train_sum['Attribute1']) ** 2)))

# train_x1['Attribute3'] = predict_train13
# test_x1['Attribute3'] = predict_test113
train_x_lgb['Attribute1'] = predict_train11
test_x_lgb['Attribute1'] = predict_test11


train_y = train_sum['label']


submit = pd.read_csv('./submit_example.csv')
test = pd.read_csv('./first_round_testing_data.csv')

# rand_seed = range(20)

# temp = np.zeros((6000, 4))
def sum_model(c_model):
    
    if c_model == 'cat':


        cbt_model = cbt.CatBoostClassifier(iterations=6000,learning_rate=0.01,verbose=300,
        early_stopping_rounds=1000,task_type='GPU',
        loss_function='MultiClass')
#         train_x1_cat = train_x1.iloc[:,2:]
#         test_x1_cat = test_x1.iloc[:,2:]
        cbt_model.fit(train_x_lgb, train_y,eval_set=(train_x_lgb,train_y))

        # print_best_score(cbt_model,params)

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
        
        
#         lgb_mc_model = lgb.LGBMClassifier(
#          boosting_type="gbdt", num_leaves=63,
#          n_estimators=300, objective='multiclass',feature_fraction = 0.9,
#          bagging_fraction = 0.9,
#          bagging_seed = 0,
#          bagging_freq = 1,
#          verbose = -1,
#          reg_alpha=10,
#          reg_lambda=2,
#          lambda_l1 = 0,
#          lambda_l2 = 1,
#          num_threads = 8,
#          learning_rate=0.01,
#          random_state=42
#         )
#         eval_set = [(train_x1, train_y)]
#         lgb_mc_model.fit(train_x1, train_y, eval_set=eval_set,verbose=100)
        
#         oof = lgb_mc_model.predict_proba(train_x1)


#         prediction = lgb_mc_model.predict_proba(test_x1)




        
        
        


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
    

#############



oof,prediction = sum_model('cat')
    
gc.collect()
print(oof.shape)
print(train_y.shape)
print(pd.get_dummies(train_y).values)


print('logloss',log_loss(pd.get_dummies(train_y).values, oof))
print('ac',accuracy_score(train_y, np.argmax(oof,axis=1)))
# print('mae',1/(1 + np.sum(np.absolute(np.eye(4)[train_y] - oof))/480))




sub = test[['Group']]
prob_cols = [i for i in submit.columns if i not in ['Group']]
for i, f in enumerate(prob_cols):
    
    sub[f] = prediction[:, i]
for i in prob_cols:
    
    sub[i] = sub.groupby('Group')[i].transform('mean')
    
sub = sub.drop_duplicates()

sub.to_csv('./1submission_ning_prepa_a8.csv',index=False)



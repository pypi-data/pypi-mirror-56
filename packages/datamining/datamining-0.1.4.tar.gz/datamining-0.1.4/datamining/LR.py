import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as opt

def sigmoid(z):
    """
    func: 
        s形函数，将值转化到（0，1）之间
    args:
        z：等待转化的值（数值，矩阵皆可）
    return:
        转化后的值，类型和输入一致
    """
    return 1 / (1 + np.exp(-z))

def cost(theta, X, y):
    """
    func: 
        计算损失函数
    args:
        theta：参数数组
        X：特征数组
        y：标签数组
    return:
        损失函数的值，为一个数值
    """
    #将数组转化为矩阵
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    
    first = np.multiply(-y, np.log(sigmoid(X * theta.T)))    #对应损失函数y=1的部分
    second = np.multiply(-(1 - y), np.log(1 - sigmoid(X * theta.T)))    #对应损失函数y=0的部分
    return np.sum(first + second) / (len(X))    #将矩阵求和


def costReg(theta, X, y, lr):
    """
    func: 
        计算损失函数（正则化）
    args:
        theta：参数数组
        X：特征数组
        y：标签数组
        lr：正则化参数
    return:
        损失函数的值，为一个数值
    """
    
    #将数组转化为矩阵
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    
    #按照公式进行计算，无正则化时的损失
    first = np.multiply(-y, np.log(sigmoid(X * theta.T)))
    second = np.multiply(-(1 - y), np.log(1 - sigmoid(X * theta.T)))
    cost = np.sum(first + second) / len(X)    
    
    #正则化参数项，也就是高次项的乘法项
    reg = (lr / (2 * len(X))) * np.sum(np.power(theta[:, 1:theta.shape[1]], 2))    #因为x0=1不发生变化
                                                                                    #故theta0不需要正则化
    return (cost + reg)


def gradient(theta, X, y):
    """
    func: 
        单次梯度下降
    args:
        theta：参数数组
        X：特征数组
        y：标签数组
    return:
        一个梯度步长，以供后续的优化函数进行优化
    """
    #将数组转化为矩阵
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    
    #初始化参数和中间变量
    para = int(theta.ravel().shape[1])
    grad = np.zeros(para)
    
    #按照公式进行计算
    error = sigmoid(X * theta.T) - y    #每轮梯度下降中不变的部分
    for i in range(para):
        term = np.multiply(error, X[:, i])    #对应元素相乘
        grad[i] = sum(term) / len(X)
        
    return grad


def gradientReg(theta, X, y, lr):
    """
    func: 
        单次梯度下降（正则化）
    args:
        theta：参数数组
        X：特征数组
        y：标签数组
        lr：正则化参数
    return:
        一个梯度步长，以供后续的优化函数进行优化
    """
    #将数组转化为矩阵
    theta = np.matrix(theta)
    X = np.matrix(X)
    y = np.matrix(y)
    
    #初始化参数和中间变量
    parameters = int(theta.ravel().shape[1])
    grad = np.zeros(parameters)
    
    #按照公式进行计算
    error = sigmoid(X * theta.T) - y
    
    for i in range(parameters):
        term = np.multiply(error, X[:,i])
        
        if (i == 0):
            grad[i] = np.sum(term) / len(X)    #i=0时不需要正则化
        else:
            grad[i] = (np.sum(term) / len(X)) + ((lr / len(X)) * theta[:,i])
    
    return grad

def predict(theta, X):
    """
    func: 
        预测模型的准确率
    args:
        theta：参数数组
        X：特征数组
    return:
        准确率
    """
    #将数组转化为矩阵
    theta = np.matrix(theta)
    X = np.matrix(X)
    
    pro = sigmoid(X * theta.T)    #将特征作为输入得到结果
    return [1 if y >= 0.5 else 0 for y in pro]    #验证结果

file_path = 'ex2data1.txt'
data = pd.read_csv(file_path, header=None, names=['exam1', 'exam2', 'admitted'])
positive = data[data['admitted'].isin([1])]
negative = data[data['admitted'].isin([0])]

fig, ax = plt.subplots(figsize=(12,8))
ax.scatter(positive.exam1, positive.exam2, s=50, c='b', marker='o', label='Admitted')
ax.scatter(negative['exam1'], negative['exam2'], s=50, c='r', marker='x', label='Not Admitted')
ax.legend()
ax.set_xlabel('Exam 1 Score')
ax.set_ylabel('Exam 2 Score')
plt.show()

data.insert(0, 'ones', 1)    #为了使得公式简化，引入x0=1

#划分特征和标签
cols = data.shape[1]
X = data.iloc[:, :-1]
y = data.iloc[:, -1:]

#将所有数据转化为矩阵形式
# X = np.array(X.values)
X = X.values
y = y.values
theta = np.zeros(3)

#用SciPy's truncated newton（TNC）实现寻找最优参数。
import scipy.optimize as opt
result = opt.fmin_tnc(func=cost, x0=theta, fprime=gradient, args=(X,y))    #scipy.optimize.fmin_tnc的使用

theta_min = result[0]    
predictions = predict(theta_min, X)

correct = [1 if ((a == 0) and (b == 0)) or ((a == 1) and (b == 1)) else 0 for (a,b) in zip(predictions, y)]
acc = (sum(map(int, correct)) % len(correct))
print('accuracy = {0}%'.format(acc))


# path = 'ex2data2.txt'
# data2 = pd.read_csv(path, header=None, names=['test1', 'test2', 'accept'])
# positive = data2[data2['accept'].isin([1])]
# negative = data2[data2['accept'].isin([0])]

# fig, ax = plt.subplots(figsize=(12,8))
# ax.scatter(positive['test1'], positive['test2'], s=50, c='b', marker='o', label='Accepted')
# ax.scatter(negative['test1'], negative['test2'], s=50, c='r', marker='x', label='Rejected')
# ax.legend()
# ax.set_xlabel('Test 1 Score')
# ax.set_ylabel('Test 2 Score')
# plt.show()

# data2.insert(3, 'Ones', 1) 

# #创造多个高次项用来验证使用正则化避免过拟合
# degree = 4
# x1 = data2['test1']
# x2 = data2['test2']

# #创造高次项关键步骤，特征映射

# # for i in 1..i
# #   for p in 0..i:
# #     output x^(i-p) * y^p

# for i in range(1, degree):
#     for j in range(0, i+1):
#         data2['F' + str(i) + str(j)] = np.power(x1, i-j) * np.power(x2, j)

# data2.drop('test1', axis=1, inplace=True)    #将原始项丢弃
# data2.drop('test2', axis=1, inplace=True)

# #划分特征和标签
# cols = data2.shape[1]
# X2 = data2.iloc[:,1:cols]
# y2 = data2.iloc[:,0:1]

# X2 = np.array(X2.values)
# y2 = np.array(y2.values)
# theta2 = np.zeros(10)

# learningRate = 1    #正则化参数

# result2 = opt.fmin_tnc(func=costReg, x0=theta2, fprime=gradientReg, args=(X2, y2, learningRate))
# theta_min = np.matrix(result2[0])
# predictions = predict(theta_min, X2)
# correct = [1 if ((a == 1 and b == 1) or (a == 0 and b == 0)) else 0 for (a, b) in zip(predictions, y2)]
# accuracy = (sum(map(int, correct)) % len(correct))
# print ('accuracy = {0}%'.format(accuracy))

# #调用sklearn的线性回归包
# from sklearn import linear_model
# model = linear_model.LogisticRegression(penalty='l2', C=1.0)
# model.fit(X2, y2.ravel())
# model.predict(X2[:2])
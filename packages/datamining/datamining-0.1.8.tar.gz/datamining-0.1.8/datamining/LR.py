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

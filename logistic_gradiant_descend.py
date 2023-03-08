# -*- coding: GBK -*-
#������Ҫ�Ŀ�
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold




#��ȡcsv�ļ�����,header=0˵����һ����������

data = pd.read_csv('credit-overdue.csv',header=0)

data_array=np.array(data)

#��ȡ�Ա����������
X = data.iloc[:,:-1].values
y = data.iloc[:,-1].values.reshape(-1,1)

#��ӳ�����
X = np.insert(X,0,1,axis = 1)

#��ʼ������
theta = np.zeros((X.shape[1],1))
alpha = 0.01
epsilon = 1e-5 #������ֵ

#sigmoid����
def sigmoid(z):
    return 1/(1+np.exp(-z))

#������ʧ����
def cost_function(X,y,theta):
    m = len(y)
    h = sigmoid(np.dot(X,theta))
    #��������ʧ����,�ȼ�����Ȼ���෴���������ʸ���
    J = (-1/m)*np.sum(y*np.log(h)+(1-y)*np.log(1-h))
    return J
    
#�����ݶ��½�����    
def gradiant_descent(X,y,theta,alpha,epsilon):
    """
    X: ������������ÿ�д���һ��������ÿ�д���һ������
    y: �����ǩ��Ϊ0��1
    alpha: ѧϰ��
    theta: ϵ������
    epsilon: ������ֵ
    """
    m = len(y)
    cost = cost_function(X,y,theta)
    cost_old = cost + 5*epsilon #��cost_old��ʼ��,5�������ѡ��Ϊ��������ʼ
    num_iters = 0
    #��������ֹͣ�ݶ��½�
    while abs(cost_old - cost)>epsilon:
        cost_old = cost
        h = sigmoid(np.dot(X,theta))
        gradiant = np.dot(X.T,(h-y))/m
        theta = theta - alpha*gradiant
        cost = cost_function(X,y,theta)
        num_iters+=1
        if num_iters % 100 == 0:
            print(f'iteration {num_iters}, Cost function value: {cost}')
    return theta
      
    
#k�۽�����֤
k = 5
skf = StratifiedKFold(n_splits=k)
accuracies = []
confusion = np.zeros((2,2))
for train_index,test_index in skf.split(X,y):
    X_train,X_test = X[train_index],X[test_index]
    y_train,y_test = y[train_index],y[test_index]
    theta = np.zeros((X.shape[1],1))
    theta = gradiant_descent(X_train,y_train,theta,alpha,epsilon)
    #����0.5����Ϊ��1��С��0.5����Ϊ��0
    y_pred = np.round(sigmoid(np.dot(X_test,theta)))
    #confusion_matrix������binaryֵ���Բ���round��һ��Ԥ��ֵy_pred0
    y_pred0 = sigmoid(np.dot(X_test,theta))
    accuracy = np.mean(y_pred == y_test)
    accuracies.append(accuracy)

#�������
print('Theta: ',theta)
print('KFOLD accuracies(5 times):',accuracies)


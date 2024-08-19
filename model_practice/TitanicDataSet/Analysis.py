#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

### Loading dataset

data=pd.read_csv('titanic.csv')

# ### Handling missing values and droping not usefull columns 

#create copy of dataset
df=data.copy()

#Drop columns
df.drop(columns=['Ticket','Name','PassengerId','Cabin'],inplace=True)

#Filling null values

#Filling age with mean
df['Age']=df['Age'].fillna(df['Age'].mean())

#Filling Embarked with mode
df['Embarked']=df['Embarked'].fillna(df['Embarked'].mode()[0])

##converting objects into int

df['Sex']=data['Sex'].astype(str)


df['Sex']=pd.get_dummies(df['Sex'],drop_first=True).astype(int)



df['Age']=df['Age'].astype(int)
df['Embarked']=df['Embarked'].astype(str)


df['Embarked']=df['Embarked'].replace({'S':1,'C':2,'Q':3})

print(df.info())

df_cor=df.corr()

sns.heatmap(df_cor,annot=True)


x=df.drop(columns=['Survived'])


y=df['Survived']

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.10)


from sklearn.linear_model import LinearRegression


model=LinearRegression()
model.fit(x_train,y_train)

y_pre=model.predict(x_test)


from sklearn.metrics import r2_score
r2=r2_score(y_test,y_pre)

print("The r square of the algorithm is:"r2*100)

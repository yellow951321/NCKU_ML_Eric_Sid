# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:02:22 2019

@author: scream
"""
import math
import pickle
with open("arkanoid/log/2019-04-11_16-37-09.pickle", "rb") as f:
    data_list = pickle.load(f)

# save each information seperately
Frame=[]
Status=[]
Ballposition=[]
PlatformPosition=[]
Bricks=[]
for i in range(0,len(data_list)):
    Frame.append(data_list[i].frame)
    Status.append(data_list[i].status)
    Ballposition.append(data_list[i].ball)
    PlatformPosition.append(data_list[i].platform)
    Bricks.append(data_list[i].bricks)

#%% calculate instruction of each frame using platformposition
import numpy as np
PlatX=np.array(PlatformPosition)[:,0][:, np.newaxis]
PlatX_next=PlatX[1:,:]
instruct=(PlatX_next-PlatX[0:len(PlatX_next),0][:,np.newaxis])/5


# select some features to make x
Ballarray=np.array(Ballposition[:-1])

next_Ballarray = np.array(Ballposition[1:])

x=np.hstack((Ballarray, next_Ballarray, PlatX[0:-1,0][:,np.newaxis]))
#select intructions as y
y=instruct

# split the data into train and test
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state= 0)

#%% train your model here
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
# clf = svm.SVC(gamma=0.001, decision_function_shape='ovo')
# clf = KNeighborsClassifier(n_neighbors=3)
clf = RandomForestClassifier(random_state=5)

clf.fit(x_train,y_train)
pred = clf.predict(x_test)
# check the acc to see how well you've trained the model
from sklearn.metrics import accuracy_score
acc= accuracy_score(pred, y_test)
print(acc)


 #%% save model
import pickle

filename="clf_example0401.sav"
pickle.dump(clf, open(filename, 'wb'))

# load model
l_model=pickle.load(open(filename,'rb'))
yp_l=l_model.predict(x_test)
print("acc load: %f " % accuracy_score(yp_l, y_test))

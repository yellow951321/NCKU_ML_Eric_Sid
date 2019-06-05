# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:02:22 2019

@author: scream
"""
import math
import numpy as np
Ballarray = []
pre_Ballarray = []
PlatX = []
label = []
updes = 0
# select some features to make x

for i in range(0,201,5):
    for j in range(100,401,10):
        for k in range(0,181,5):
            cur_ball_center = (i + 2.5, j + 5)
            cur_platform_center = (k + 20 , 400)

            expect_pos = cur_ball_center[0]
            for direct in [1,-1]:
                # calculate the position will touch the position in line
                expect_pos = (400-cur_ball_center[1])/direct + cur_ball_center[0]
                while expect_pos > 200 or expect_pos < 0:
                    if expect_pos > 200:
                        expect_pos = 400 - expect_pos
                    elif expect_pos < 0:
                        expect_pos = -expect_pos
                
                if cur_platform_center[0] - expect_pos > 0:
                    des = -1 # go left
                elif cur_platform_center[0] - expect_pos < 0:
                    des = 1 # go right
                else:
                    des = 0
                Ballarray.append([i, j])
                pre_Ballarray.append([i - direct*5, j - 5])
                PlatX.append([k])
                label.append([des])

                # add updirection
                if k + 20 < 100:
                    updes = 1
                else:
                    updes = -1
                Ballarray.append([i, j])
                pre_Ballarray.append([i - direct*5, j + 5])
                PlatX.append([k])
                label.append([updes])

x=np.hstack((Ballarray, pre_Ballarray, PlatX))
#select intructions as y
y=label

# split the data into train and test
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state= 0)

#%% train your model here
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
# clf = svm.SVC(gamma=0.001, decision_function_shape='ovo')
# clf = KNeighborsClassifier(n_neighbors=3)
clf = RandomForestClassifier(random_state=10)

# clf.fit(x_train,y_train)
clf.fit(x,y)

pred = clf.predict(x_test)
# check the acc to see how well you've trained the model
from sklearn.metrics import accuracy_score
acc= accuracy_score(pred, y_test)
print(acc)


 #%% save model
import pickle

filename="arkanoid/ml/newpredict.sav"
pickle.dump(clf, open(filename, 'wb'))

# load model
# l_model=pickle.load(open(filename,'rb'))
# yp_l=l_model.predict(x_test)
# print("acc load: %f " % accuracy_score(yp_l, y_test))

#coding:utf-8

import tensorflow as tf
import numpy as np
import random as rd
#
BATCH_SIZE=8
seed=23455
#
qun_number=10
max_diedai=40
global max_guzhi
max_guzhi=0.0
global min_guzhi
min_guzhi=0.0
global xuanze_guzhi
xuanze_guzhi=0.0
global gailv_jiaocha
gailv_jiaocha=0.6
global gailv_bianyi
gailv_bianyi=1.0
max_guzhi_whole=0.0
dead=[0 for i in range(qun_number)]
buffer_whole=1.0
#
W1=[]
S1=[]
W2=[]
S2=[]
new1=[]
new2=[]
wloss=[0.0 for i in range(qun_number)]
#
def find_max():
    temp=0.0
    for i in range(qun_number):
        if(wloss[i]>temp):
            temp=wloss[i]
    return temp

def find_min():
    temp=1.0
    for i in range(qun_number):
        if(wloss[i]<temp):
            temp=wloss[i]
    return temp
def jiancha():
    count=0.0
    for i in range(qun_number):
        if(wloss[i]>xuanze_guzhi):
            count=count+1
    return (count/qun_number)
def swarm_xuanze():
    global max_guzhi
    global min_guzhi
    global xuanze_guzhi
    max_guzhi=find_max()
    min_guzhi=find_min()
    xuanze_guzhi=rd.uniform(min_guzhi,max_guzhi)
    ceshi=jiancha()
    while(ceshi<0.005 or ceshi>0.8):
        xuanze_guzhi=rd.uniform(min_guzhi,max_guzhi)
        ceshi=jiancha()
    for i in range(qun_number):
        if(wloss[i]>xuanze_guzhi):
            dead[i]=1
#
def fanzhi(fu,mu,i):
    new1[i]=W1[fu]
    new2[i]=W2[mu]

def newg():
    fu=0
    mu=0
    for i in range(qun_number):
        if(dead[i]==1):
            while(fu==mu):
                fu=int(rd.uniform(0,qun_number))
                while(dead[fu]==1):
                    fu=int(rd.uniform(0,qun_number))
                mu=int(rd.uniform(0,qun_number))
                while(dead[mu]==1):
                    mu=int(rd.uniform(0,qun_number))
            fanzhi(fu,mu,i)
            fu=0
            mu=0
    for i in range(qun_number):
        if(dead[i]==1):
            W1[i]=new1[i]
            W2[i]=new2[i]
            dead[i]=0
#

rng=np.random.RandomState(seed)

X=rng.rand(32,2)

Y=[[int(x0+x1<1)] for (x0,x1) in X]

print("X:\n",X)
print("Y:\n",Y)

x=tf.placeholder(tf.float32,shape=(None,2))
y_=tf.placeholder(tf.float32,shape=(None,1))

for i in range(1,qun_number+1):
    w1=tf.Variable(tf.random_normal([2,3],stddev=1,seed=i))
    w2=tf.Variable(tf.random_normal([3,1],stddev=1,seed=i))
    W1.append(w1)
    new1.append(w1)
    W2.append(w2)
    new2.append(w2)
   
a=[0 for i in range(qun_number)]
y=[0 for i in range(qun_number)]


for j in range(qun_number):
    #a[j]=tf.matmul(x,W1[j])
    #y[j]=tf.matmul(a[j],W2[j])
    a=tf.matmul(x,W1[j])
    y=tf.matmul(a,W2[j])
    if(j==0):
        print(W1[0])
    
    loss=tf.reduce_mean(tf.square(y-y_))
    train_step=tf.train.GradientDescentOptimizer(0.001).minimize(loss)
    
    with tf.Session() as sess:
        init_op=tf.global_variables_initializer()
        sess.run(init_op)
        print("w1:\n",sess.run(W1[j]))
        print("w2:\n",sess.run(W2[j]))
        print("\n")

        STEPS=3000
        for i in range(STEPS):
            start=(i*BATCH_SIZE)%32
            end=start+BATCH_SIZE
            sess.run(train_step,feed_dict={x:X[start:end],y_:Y[start:end]})
            if i%500==0:
                total_loss=sess.run(loss,feed_dict={x:X,y_:Y})
                print("After %d training step(s) , loss on all data is %g" %(i,total_loss))
            if(i==STEPS-1):
                total_loss=sess.run(loss,feed_dict={x:X,y_:Y})
                wloss[j]=total_loss
        print("\n")
        if(j==0):
            print(W1[0])
        print("w1:\n",sess.run(W1[j]))
        S1.append(sess.run(W1[j]))
        print("w2:\n",sess.run(W2[j]))
        S2.append(sess.run(W2[j]))
    print(wloss)
print(S1)
print(S2)

swarm_xuanze()
print(dead)
#print(W1)
#print(W2)
newg()
#print(W1)
#print(W2)
buffer=1.0
cishu=0
#a=tf.matmul(x,W1[j])
if(j==0):
    print(W1[0])
#y=tf.matmul(a,W2[j])
while(1):
    for j in range(qun_number):
        a=tf.matmul(x,W1[j])
        y=tf.matmul(a,W2[j])
        loss=tf.reduce_mean(tf.square(y-y_))
        train_step=tf.train.GradientDescentOptimizer(0.001).minimize(loss)
        with tf.Session() as sess:
            init_op=tf.global_variables_initializer()
            sess.run(init_op)
            print("w1:\n",sess.run(W1[j]))
            print("w2:\n",sess.run(W2[j]))
            print("\n")
    
            STEPS=3000
            for i in range(STEPS):
                start=(i*BATCH_SIZE)%32
                end=start+BATCH_SIZE
                sess.run(train_step,feed_dict={x:X[start:end],y_:Y[start:end]})
                if i%500==0:
                    total_loss=sess.run(loss,feed_dict={x:X,y_:Y})
                    print("After %d training step(s) , loss on all data is %g" %(i,total_loss))
                if(i==STEPS-1):
                    total_loss=sess.run(loss,feed_dict={x:X,y_:Y})
                    wloss[j]=total_loss
            print("\n")
            print("w1:\n",sess.run(W1[j]))
            print("w2:\n",sess.run(W2[j]))
        print(wloss)
    swarm_xuanze()
    print(dead)
#print(W1)
#print(W2)
    newg()
    for k in range(qun_number):
        if(wloss[k]<buffer):
            buffer=wloss[k]
    if(buffer-buffer_whole<0.0001 or buffer_whole-buffer>0.0001):
        cishu=cishu+1
    if(buffer<buffer_whole):
        buffer_whole=buffer
    print("$good loss is %f$" %buffer)
    buffer=1.0
    if(cishu==2):
        break;

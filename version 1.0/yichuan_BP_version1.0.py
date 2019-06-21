import numpy as np
import random as rd
import os
qun_number=100
length=10
max_diedai=400
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
newge=[[0 for i in range(length)] for i in range(qun_number)]
cities=[[0,0] for i in range(length)]
swarm=[[0 for i in range(length)] for i in range(qun_number)]
swarm_guzhi=[0.0 for i in range(qun_number)]
guancha=0.0
global cishu
cishu=0
failure=0

#cities=[[1,1],[2,2],[3,3],[1,3],[2,3],[5,6],[8,7],[9,4],[5,3],[4,7],[5,5],[4,9],[7,1],[6,7]]
cities=[[0,0],[12,32],[5,25],[8,45],[33,17],[25,7],[15,15],[15,25],[25,15],[41,12]]
def init():
    swarm[0]=[i for i in range(length)]
    for i in range(1,qun_number):
        for j in range(length):
            swarm[i][j]=swarm[0][j]
        temp=0
        left=0
        right=0
        for k in range(5):
            left=int(rd.uniform(0,length))
            right=int(rd.uniform(0,length))
            temp=swarm[i][left]
            swarm[i][left]=swarm[i][right]
            swarm[i][right]=temp

def oushijuli(a,b):
    result=0.0
    result=((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5
    return result

def guzhi(path):
    juli=0.0
    for i in range(length-1):
        juli=juli+oushijuli(cities[path[i]],cities[path[i+1]])
    juli=juli+oushijuli(cities[path[length-1]],cities[path[0]])
           
    juli=1/juli
    return juli
   


def find_max(swarm_guzhi):
    temp=0.0
    for i in range(qun_number):
        if(swarm_guzhi[i]>temp):
            temp=swarm_guzhi[i]
    return temp

def find_min(swarm_guzhi):
    temp=1.0
    for i in range(qun_number):
        if(swarm_guzhi[i]<temp):
            temp=swarm_guzhi[i]
    return temp

def jiancha():
    count=0.0
    for i in range(qun_number):
        if(swarm_guzhi[i]<xuanze_guzhi):
            count=count+1
    return float(count)/qun_number


def guzhi_xuanze():
    global cishu
    global max_guzhi
    global min_guzhi
    global xuanze_guzhi
    ceshi=0.0
    count=0
    max_guzhi=find_max(swarm_guzhi)
    min_guzhi=find_min(swarm_guzhi)
    xuanze_guzhi=rd.uniform(min_guzhi,max_guzhi)
    ceshi=jiancha()
    while(ceshi<0.01 or ceshi>0.8):
        xuanze_guzhi=rd.uniform(min_guzhi,max_guzhi)
        ceshi=jiancha()
        count=count+1
        if(count>10000):
            print("error\n")
            print("$%f\t" %max_guzhi)
            print("$%f\t" %min_guzhi)
            print("$%f\t" %ceshi)
            cishu=count
            print("%d\n" %count)
            if(count>11000):
                break;

def swarm_xuanze():
    guzhi_xuanze()
    for i in range(qun_number):
        if(swarm_guzhi[i]<xuanze_guzhi):
            dead[i]=1


def jiancha_new(mu,new_now):
    for i in range(length):
        if(i%2==0):
            if(mu==new_now[i]):
                return 0
    return 1
def zhengchang(fu,mu,new_now):
    for i in range(length):
        if(i%2==0):
            new_now[i]=fu[i]
    mu_zuobiao=0
    panduan=0
    for i in range(length):
        if(i%2!=0):
            while(1):
                if(jiancha_new(mu[mu_zuobiao],new_now)==1):
                    new_now[i]=mu[mu_zuobiao]
                    panduan=1
                mu_zuobiao=mu_zuobiao+1
                if(panduan==1):
                    break
            panduan=0
    mu_zuobiao=0

def chachong(one,zuobiao):
    count=0
    record1=0
    record2=0
    for i in range(length):
        for j in range(length):
            if(one[j]==i and count==1):
                record2=j
                count=count+1
            if(one[j]==i and count==0):
                record1=j
                count=count+1
            if(count==2):
                count=0
                zuobiao[record1]=1
                break
        count=0

def jiaocha(fu_now,mu_now):
    temp=0
    left=0
    zuobiao_fu=[0 for i in range(length)]
    zuobiao_mu=[0 for i in range(length)]
    right=length-1
    while((right-left>4) or (right-left<0)):
        left=int(rd.uniform(0,length))
        right=int(rd.uniform(0,length))

    for i in range(left,right+1):
        temp=fu_now[i]
        fu_now[i]=mu_now[i]
        mu_now[i]=temp
        temp=0

    chachong(fu_now,zuobiao_fu)
    chachong(mu_now,zuobiao_mu)
    mu_zuo=0
    panduan=0
    for i in range(length):
        if(zuobiao_fu[i]==1):
            while(1):
                if(zuobiao_mu[mu_zuo]==1):
                    temp=fu_now[i]
                    fu_now[i]=mu_now[mu_zuo]
                    mu_now[mu_zuo]=temp
                    panduan=1
                mu_zuo=mu_zuo+1
                if(panduan==1):
                    break;
            panduan=0


def bianyi(new_now):
    left=int(rd.uniform(0,length))
    right=int(rd.uniform(0,length))
    temp=0
    temp=new_now[left]
    new_now[left]=new_now[right]
    new_now[right]=temp

def fanzhi(fu,mu,new_now):
    global gailv_jiaocha
    global gailv_bianyi
    fu_now=[0 for i in range(length)]
    for i in range(length):
        fu_now[i]=fu[i]
    mu_now=[0 for i in range(length)]
    for i in range(length):
        mu_now[i]=mu[i]
    jiaocha_gailv_now=rd.uniform(0,1)
    bianyi_gailv_now=rd.uniform(0,1)
    #jiaocha_gailv_now=0
    #bianyi_gailv_now=0
    if(jiaocha_gailv_now<gailv_jiaocha):
        jiaocha(fu_now,mu_now)
        zhengchang(fu_now,mu_now,new_now)
    else:
        zhengchang(fu_now,mu_now,new_now)
    if(bianyi_gailv_now<gailv_bianyi):
        bianyi(new_now)

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
            fanzhi(swarm[fu],swarm[mu],newge[i]);
            fu=0
            mu=0
    for i in range(qun_number):
        if(dead[i]==1):
            for j in range(length):
                swarm[i][j]=newge[i][j]
                newge[i][j]=0
            dead[i]=0

times=0

#main()
init()
for i in range(qun_number):
    swarm_guzhi[i]=guzhi(swarm[i])
    print("\n$%f$\n" %swarm_guzhi[i])

swarm_xuanze()#
max_guzhi_whole=max_guzhi

count=0
dai=0
while(count<100):
    newg();
    for i in range(qun_number):
        swarm_guzhi[i]=guzhi(swarm[i])
    swarm_xuanze();
    print("%f" %xuanze_guzhi)
    if(max_guzhi_whole-max_guzhi<0.00001 and max_guzhi_whole-max_guzhi>-0.00001):
        count=count+1
        print("the %d dai is:\n:" %dai)
        print("the guzhi_now is %f the guzhi_whole is %f" %(max_guzhi,max_guzhi_whole))
        print("$%d$",count)
    if(max_guzhi>max_guzhi_whole):
        max_guzhi_whole=max_guzhi
    dai=dai+1
    if(dai>max_diedai):
        break

    for i in range(qun_number):
        for j in range(length):
            for k in range(length):
                if(swarm[i][k]==j):
                    times=times+1
            if(times!=1):
                print("error stop")
                print("the %d is worng" %i)
                for h in range(length):
                    print("$%d$" %swarm[i][h])
                os.system("pause")
            times=0
    if(cishu>9999):
        for i in range(qun_number):
            if(swarm_guzhi[i]==max_guzhi):
                for j in range(length):
                    print("%2d" %swarm[i][j])
        for i in range(qun_number):
            print("\t%f" %swarm_guzhi[i])
            if(i%8==0):
                print("\n")
        os.system("pause")


   # if(cishu>10000):
     #   cishu=0
       # failure++
print("%f" %xuanze_guzhi)
print("the max is :%f",max_guzhi_whole)
print("the failure times is %d" %failure)
for i in range(qun_number):
    if(swarm_guzhi[i]==max_guzhi):
        print("the path is")   
        for j in range(length):
            print("%2d",swarm[i][j])
        break;


#print(dead)
#for i in range(qun_number):
    #print(swarm_guzhi[i])
#print(swarm)
#print("\n")
#print(cities)

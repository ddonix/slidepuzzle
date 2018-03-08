#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import numpy as np 
import random

class spuzzle:
    def __init__(self,p, dis=None, prev=None):
        self.data = p
        
        if dis == None:
            self.distance = self.getdistance()
        else:
            self.distance = dis
        
        if prev == None:
            self.prevstep = None
        else:
            self.prevstep = prev 
    
    def getdistance(self):
        raise NotImplementedError
    
    def nextpuzzle(self, s, new):
        raise NotImplementedError

class spuzzle_4X4(spuzzle):
    weight = np.empty([15],dtype='int32')
    weight[11] = weight[14] = 3
    weight[10] = 9
    weight[13] =  27
    weight[9] =  81
    weight[12] =  243
    weight[8] =  729
    weight[7] =  729*3
    weight[6] =  729*9
    weight[5] =  729*27
    weight[4] =  729*81
    weight[3] = 729*243
    weight[2] =  729*729
    weight[1] =  729*729*3
    weight[0] =  729*729*9

    def __init__(self,p,dis, prev):
        spuzzle.__init__(self, p, dis, prev)
        self.data2 = np.empty([16], dtype='int32')
        for v in np.arange(16):
            i = self.data[v]
            self.data2[i] = v
    
    def getdistance(self):
        self.distance = 0
        for v in np.arange(15):
            p = self.data[v]
            i1 = v/4
            j1 = v%4
            i2 = p/4
            j2 = p%4
            self.distance += (abs(i2-i1)+abs(j2-j1))*spuzzle_4X4.weight[v]
        return self.distance 
    
    def getdistanceChange(self, v, p1, p2):
        i = v/4
        j = v%4
        i1 = p1/4
        j1 = p1%4
        i2 = p2/4
        j2 = p2%4
        d1 = (abs(i1-i)+abs(j1-j))*spuzzle_4X4.weight[v]
        d2 = (abs(i2-i)+abs(j2-j))*spuzzle_4X4.weight[v]
        return d2-d1


    def display(self):
        show = np.empty([4,4], dtype='int32')
        for i in [0,1,2,3]:
            for j in [0,1,2,3]:
                show[i][j] = (self.data2[i*4+j]+1)%16
        print(show)
        print("distance %d"%self.distance)
        print("................")

    def nextpuzzle(self, s, new):
        nextp = self 
        p = self.data[15]
        if s == 0:
            if p > 3:
                a = self.data2[p-4]
                b = self.getdistanceChange(a,p-4,p)
                
                if new == True:
                    tmp = np.array(self.data)
                    tmp[15] = p-4
                    tmp[a] = p
                    d = self.distance + b

                    nextp = spuzzle_4X4(tmp, dis=d, prev=s)
                else:
                    self.data[15] = p-4
                    self.data[a] = p
                    self.data2[p-4] = 15
                    self.data2[p] = a
                    self.distance += b
                    self.prevstep = s
        
        if s == 1:
            if p < 12:
                a = self.data2[p+4]
                b = self.getdistanceChange(a,p+4,p)
                
                if new == True:
                    tmp = np.array(self.data)
                    tmp[15] = p+4
                    tmp[a] = p
                    d = self.distance + b

                    nextp = spuzzle_4X4(tmp, dis=d, prev=s)
                else:
                    self.data[15] = p+4
                    self.data[a] = p
                    self.data2[p+4] = 15
                    self.data2[p] = a
                    self.distance += b
                    self.prevstep = s
        
        if s == 2:
            if p%4 > 0:
                a = self.data2[p-1]
                b = self.getdistanceChange(a,p-1,p)
                
                if new == True:
                    tmp = np.array(self.data)
                    tmp[15] = p-1
                    tmp[a] = p
                    d = self.distance + b

                    nextp = spuzzle_4X4(tmp, dis=d, prev=s)
                else:
                    self.data[15] = p-1
                    self.data[a] = p
                    self.data2[p-1] = 15
                    self.data2[p] = a
                    self.distance += b
                    self.prevstep = s
        
        if s == 3:
            if p%4 < 3:
                a = self.data2[p+1]
                b = self.getdistanceChange(a,p+1,p)
                
                if new == True:
                    tmp = np.array(self.data)
                    tmp[15] = p+1
                    tmp[a] = p
                    d = self.distance + b

                    nextp = spuzzle_4X4(tmp, dis=d, prev=s)
                else:
                    self.data[15] = p+1
                    self.data[a] = p
                    self.data2[p+1] = 15
                    self.data2[p] = a
                    self.distance += b
                    self.prevstep = s
        
        return nextp
            
Target = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
p = spuzzle_4X4(Target, dis=None, prev=None)
p.display()
p.nextpuzzle(0, False)
p.display()
p.nextpuzzle(0, False)
p.display()
p.nextpuzzle(1, False)
p.display()
p.nextpuzzle(1, False)
p.display()
p.nextpuzzle(2, False)
p.display()
p.nextpuzzle(2, False)
p.display()
p.nextpuzzle(0, False)
p.display()
p.nextpuzzle(0, False)
p.display()
p.nextpuzzle(3, False)
p.display()

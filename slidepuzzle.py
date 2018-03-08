#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import numpy as np 
import random
import cPickle as pickle
import os

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
    
    def display(self):
        raise NotImplementedError

    def getsteps(self):
        raise NotImplementedError
    
    def getdistance(self):
        raise NotImplementedError
    
    def newpuzzle(self, s):
        raise NotImplementedError

class spuzzleTree(spuzzle):
    initsearch = 8
    maxsearch  = 11

    def __init__(self,p,dis, prev):
        spuzzle.__init__(self, p, dis, prev)
        self.deep = 1
        self.child = []
        self.father = self
        self.min = self
        self.maxdeep = 1
        
    def optweight(self, parm):
        raise NotImplementedError

    def writeweight(self):
        raise NotImplementedError
    
    @classmethod
    def trainweight(cls, block, count):
        puzzle = cls.randompuzzle()
        puzzle.display()

    def printTree(self):#深度遍历
        self.display()
        print("deep %d"%self.deep)
        for c in self.child:
            c.printTree()

    def __addDeep(self):#增加一层遍历
        if self.child == []:
            steps = self.getsteps()
            for s in steps:
                c = self.newpuzzle(s)
                self.maxdeep = c.deep = self.deep + 1
                c.child = []
                c.father = self

                if c.distance < self.min.distance:
                    self.min = c
                
                self.child.append(c)
        else:
            for c in self.child:
                c.__addDeep()
                if c.min.distance < self.min.distance:
                    self.min = c.min
                if c.maxdeep > self.maxdeep:
                    self.maxdeep = c.maxdeep
    
    def addDeep(self, d):#增加一层遍历
        while d > 0:
            d -= 1
            self.__addDeep()
    

    def solvepuzzle(self):
        result = self
        
        while result.distance != 0:
            while True:
                result.addDeep(1)
                if result.maxdeep - result.deep < spuzzleTree.initsearch:
                    continue
                else:
                    break
                
            tmp = result.min
            
            if tmp.distance == result.distance:
                while True:
                    result.addDeep(1)
                    tmp = result.min
                    if tmp.distance < result.distance:
                        break
                    elif result.maxdeep - result.deep == spuzzleTree.maxsearch:
                        break
                    else:
                        continue

            if tmp.distance == result.distance:
                print("解谜失败")
                return
            else:
                result = tmp
                result.display()
        print("over")
        
class spuzzle_4X4(spuzzleTree):
    weight = np.empty([15],dtype='int32')
    if os.path.exists('./puzzleweight.txt'):
        f = open('./puzzleweight.txt', 'r')
        weight = pickle.load(f)
        f.close()
    else:
        for i in np.arange(15):
            weight[i] = 1
    print("spuzzle_4X4.weight")
    print(weight)

    def __init__(self,p,dis, prev):
        spuzzleTree.__init__(self, p, dis, prev)
        self.data2 = np.empty([16], dtype='int32')
        for v in np.arange(16):
            i = self.data[v]
            self.data2[i] = v
    
    @staticmethod
    def randompuzzle():
        Target = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        p = spuzzle_4X4(Target, dis=None, prev=4)
        p.ruffle(300)
        p.prevstep = 4
        return p

    def writeweight(self):
        f = open('./puzzleweight.txt', 'wb')
        pickle.dump(spuzzle_4X4.weight, f)
        f.close()
        return

    def display(self):
        show = np.empty([4,4], dtype='int32')
        for i in [0,1,2,3]:
            for j in [0,1,2,3]:
                show[i][j] = (self.data2[i*4+j]+1)%16
        print(show)
        print("deep %d distance %d prevstep %d"%(self.deep, self.distance, self.prevstep))
        print("................")

    def getsteps(self):
        p = self.data[15] 
        p0 = p/4
        p1 = p%4
        flag = [1,1,1,1]
        if p0 == 0:
            flag[0] = 0
        if p0 == 3:
            flag[1] = 0
        if p1 == 0:
            flag[2] = 0
        if p1 == 3:
            flag[3] = 0
        if self.prevstep == 0:
            flag[1] = 0
        if self.prevstep == 1:
            flag[0] = 0
        if self.prevstep == 2:
            flag[3] = 0
        if self.prevstep == 3:
            flag[2] = 0
        steps = []
        for i in [0,1,2,3]:
            if flag[i] == 1:
                steps.append(i)
        return steps
    
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

    def move(self, s):
        p = self.data[15]
        p2 = None
        if s == 0:
            if p > 3:
                p2 = p-4
        
        if s == 1:
            if p < 12:
                p2 = p+4
        
        if s == 2:
            if p%4 > 0:
                p2 = p-1

        if s == 3:
            if p%4 < 3:
                p2 = p+1

        if p2 != None:
            a = self.data2[p2]
            b = self.getdistanceChange(a,p2,p)
            self.data[15] = p2
            self.data[a] = p
            self.data2[p2] = 15
            self.data2[p] = a
            self.distance += b
            self.prevstep = s
    
    def newpuzzle(self, s):
        data = np.array(self.data)
        result = spuzzle_4X4(data, self.distance, self.prevstep)
        result.move(s)
        return result

    def ruffle(self, count):
        while(count > 0):
            p = self.data[15] 
            p0 = p/4
            p1 = p%4
            s = random.randint(0,3)
            if s == 0 and (self.prevstep == 1 or p0 == 0):
                continue
            if s == 1 and (self.prevstep  == 0 or p0 == 3):
                continue
            if s == 2 and (self.prevstep == 3 or p1 == 0):
                continue
            if s == 3 and (self.prevstep == 2 or p1 == 3):
                continue
            self.move(s)
            count -= 1

spuzzle_4X4.trainweight(10,10)

for i in np.arange(1):
    p = spuzzle_4X4.randompuzzle()
    p.prevstep = 4
    print("......迷宫......")
    p.display()
    print("开始解谜")
    p.solvepuzzle()

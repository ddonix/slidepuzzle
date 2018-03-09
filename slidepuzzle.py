#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import numpy as np 
import random
import cPickle as pickle
import os
import sys
import slidegui as sgui
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
    MaxDeep  = 200
    
    weight = None

    def __init__(self, fa, p, dis, prev):
        spuzzle.__init__(self, p, dis, prev)
        self.deep = 1
        self.child = []
        self.father = fa
        self.min = self
        self.maxdeep = 1
        
    def equal(self, t):
        return self.data == t.data
    
    def writeweight(self):
        raise NotImplementedError
    
    @classmethod
    def trainweight(cls, block, count):
        print("....学习weight...")
        while count > 0:
            count -= 1
            tmplist = []

            b = 0
            while b < block:
                while True:
                    puzzle = cls.randompuzzle()
                    puzzle.display()
                    tmp = puzzle.solvepuzzle()
                    if tmp == None:
                        continue
                    tmplist.append(tmp)
                    break
                b += 1
            puzzle.optweight(tmplist)
            puzzle.writeweight()
    
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
        
        f = self.father
        while f != None:
            if f.min.distance > self.min.distance:
                f.min = self.min
            f = f.father
    
    def addDeep(self, d):#增加一层遍历
        while d > 0:
            d -= 1
            self.__addDeep()

    def cutTree(self, ch):
        self.child.remove(ch)
        self.min = self
        for c in self.child:
            if self.min == None:
                self.min = c.min
            elif c.min.distance < self.min.distance:
                self.min = c.min
        
        fa = self.father
        while fa != None:
            fa.min = self.min
            fa = fa.father
    
    def solvepuzzle(self):
        result = self
        cutTrees  = []
        while result.distance != 0:
            if result.deep >= spuzzle_4X4.MaxDeep:
                break
            while True:
                result.addDeep(1)
                if result.maxdeep - result.deep < spuzzleTree.initsearch:
                    continue
                else:
                    break
                
            if result.min.distance == result.distance:
                while True:
                    result.addDeep(1)
                    if result.min.distance < result.distance:
                        break
                    elif result.maxdeep - result.deep == spuzzleTree.maxsearch:
                        break
                    continue
            
            fa = None
            if result.min.distance >= result.distance:
                fa = result.father
            for c in cutTrees:
                if c.equal(result.min) == True:
                    fa = result.father       
            if fa == None:
                result = result.min
                result.display()
            else:                
                print("back off.")
                fa.cutTree(result)
                cutTrees.append(result)
                result = fa
        
        if result.distance != 0:
            print("solve puzzle error")
            return result
        else:
            print("solve puzzle success")
            return None
        
class spuzzle_4X4(spuzzleTree):
    
    @staticmethod
    def readweight():
        spuzzle_4X4.weight = np.empty([15],dtype='int32')
        if os.path.exists('./puzzleweight.txt'):
            f = open('./puzzleweight.txt', 'r')
            spuzzle_4X4.weight = pickle.load(f)
            f.close()
        else:
            for i in np.arange(15):
                spuzzle_4X4.weight[i] = 1
            spuzzle_4X4.weight[11] = 3
            spuzzle_4X4.weight[14] = 3
            spuzzle_4X4.weight[10] = 9
            spuzzle_4X4.weight[13] = 27
            spuzzle_4X4.weight[9] = 81
            spuzzle_4X4.weight[12] = 243
            spuzzle_4X4.weight[8] = 729
            spuzzle_4X4.weight[7] = 729*3
            spuzzle_4X4.weight[6] = 729*9
            spuzzle_4X4.weight[5] = 729*27
            spuzzle_4X4.weight[4] = 729*81
            spuzzle_4X4.weight[3] = 729*243
            spuzzle_4X4.weight[2] = 729*729
            spuzzle_4X4.weight[1] = 729*729*3
            spuzzle_4X4.weight[0] = 729*729*9
            for i in np.arange(15):
                spuzzle_4X4.weight[i] = 1
    
    def __init__(self, fa, p, dis, prev):
        spuzzleTree.__init__(self, fa, p, dis, prev)
        self.data2 = np.empty([16], dtype='int32')
        for v in np.arange(16):
            i = self.data[v]
            self.data2[i] = v
    
    def equal(self, t):
        return (self.data == t.data).all()
    
    def optweight(self, parm):
        w = np.zeros(16, dtype='int32')
        for tmp in parm:
            for v in np.arange(16):
                if tmp.data[v] != v:
                    w[v] += 1
        print(w)
        
    @staticmethod
    def randompuzzle():
        Target = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        p = spuzzle_4X4(None, Target, dis=None, prev=4)
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
        result = spuzzle_4X4(self, data, self.distance, self.prevstep)
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

def main():
    if len(sys.argv) == 1:
        print("read")
        print("train")
        print("puzzle")
    elif sys.argv[1] == 'read':
        spuzzle_4X4.readweight()
        print(spuzzle_4X4.weight)
    elif sys.argv[1] == 'train':
        spuzzle_4X4.readweight()
        spuzzle_4X4.trainweight(50,1)
        spuzzle_4X4.readweight()
    elif sys.argv[1] == 'puzzle':
        spuzzle_4X4.readweight()
        print(spuzzle_4X4.weight)
        print("...解谜...")
        p = spuzzle_4X4.randompuzzle()
        p.prevstep = 4
        print("...迷宫...")
        p.display()
        p.solvepuzzle()
    else:
        spuzzle_4X4.readweight()
        p = spuzzle_4X4.randompuzzle()
        p.display()
        p.addDeep(10)
        p.min.display()
        p.min.addDeep(10)
        p.min.min.display()
        p.min.min.addDeep(10)
        p.min.min.min.display()
        p.min.display()       
        p.min.father.cutTree(p.min)
        p.min.display()       

main()

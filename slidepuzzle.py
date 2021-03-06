#!/usr/bin/python
# -*- coding:utf-8 -*- 
import numpy as np
import random

#Target[3][3][0:1]:0的位置;Target[3][3][2]:距离;Target[3][3][3]:上一步操作：4表示初始化和无操作
Target = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[3,3,0,4]])

#距离矩阵：表示0到15这16个数在[4][4]矩阵每一位距离正确位置的距离
DistanceMatrix = np.empty([16,4,4],dtype='int32')
for v in np.arange(16):
    for i in [0,1,2,3]:
        for j in [0,1,2,3]:
            i2 = v/4
            j2 = v%4
            DistanceMatrix[v][i][j] = abs(i2-i) + abs(j2-j)

weight = np.empty([16],dtype='int32')
weight[15] = 0
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

def disS(p0,p1,v):
	d = DistanceMatrix[v][p0][p1]*weight[v]
	return d

def dis(x):
    d = 0
    for p0 in [0,1,2,3]:
        for p1 in [0,1,2,3]:
            d += disS(p0,p1,x[p0][p1])
	return d

def show(x):
	print("%2d %2d %2d %2d"%(x[0][0],x[0][1],x[0][2],x[0][3]))

def show(x):
	print("%2d %2d %2d %2d"%(x[0][0],x[0][1],x[0][2],x[0][3]))
	print("%2d %2d %2d %2d"%(x[1][0],x[1][1],x[1][2],x[1][3]))
	print("%2d %2d %2d %2d"%(x[2][0],x[2][1],x[2][2],x[2][3]))
	print("%2d %2d %2d %2d"%(x[3][0],x[3][1],x[3][2],x[3][3]))
	return

#0:上 1:下 2:左 3:右 其他：不操作
def nextPuzzle(x,s,new):
    p0 = x[4][0]
    p1 = x[4][1]
    if new == True:
        newP = np.array(x)
    else:
        newP = x
    
    if s == 0:
        if p0 != 0:
            a = x[p0-1][p1]
            b = disS(p0,p1,a)+disS(p0-1,p1,15)-disS(p0,p1,15)-disS(p0-1,p1,a)
            
            newP[p0][p1] = a
            newP[p0-1][p1] = 15
            newP[4][0] = p0-1
            newP[4][1] = p1
            newP[4][2] = x[4][2]+b
            newP[4][3] = 0
        
    elif s == 1:
        if p0 != 3:
            a = x[p0+1][p1]
            b = disS(p0,p1,a)+disS(p0+1,p1,15)-disS(p0,p1,15)-disS(p0+1,p1,a)
            
            newP[p0][p1] = a
            newP[p0+1][p1] = 15
            newP[4][0] = p0+1
            newP[4][1] = p1
            newP[4][2] = x[4][2]+b
            newP[4][3] = 1
		
    elif s == 2:
        if p1 != 0:
            a = x[p0][p1-1]
            b = disS(p0,p1,a)+disS(p0,p1-1,15)-disS(p0,p1,15)-disS(p0,p1-1,a)
		
            newP[p0][p1] = a
            newP[p0][p1-1] = 15
            newP[4][0] = p0
            newP[4][1] = p1-1
            newP[4][2] = x[4][2]+b
            newP[4][3] = 2
    
    elif s == 3:
        if p1 != 3:
            a = x[p0][p1+1]
            b = disS(p0,p1,a)+disS(p0,p1+1,15)-disS(p0,p1,15)-disS(p0,p1+1,a)
            
            newP = np.array(x)
            newP[p0][p1] = a
            newP[p0][p1+1] = 15
            newP[4][0] = p0
            newP[4][1] = p1+1
            newP[4][2] = x[4][2]+b
            newP[4][3] = 2
    
    return newP

#rufflePuzzle:洗牌函数:d是次数
def rufflePuzzle(x,d):
    
    while(d > 0):
        d -= 1
        p0 = x[4][0]
        p1 = x[4][1]
        ps = x[4][3]
        
        while(True):
            s = random.randint(0,3)
            if s == 0 and (ps == 1 or p0 == 0):
                continue
            if s == 1 and (ps == 0 or p0 == 3):
                continue
            if s == 2 and (ps == 3 or p1 == 0):
                continue
            if s == 3 and (ps == 2 or p1 == 3):
                continue
            else:
                break
        nextPuzzle(x, s, False)

class Tree:
    def __init__(self,r):
        self.root = r
        self.deep = 1
        self.child = [None,None,None,None]

    def printTree(self):#深度遍历
        show(self.root)
        print(self.root[4])
        for i in [0,1,2,3]:
            if(self.child[i] != None):
                self.child[i].printTree()

    def getMinDis(self):
        if self.deep == 1:
            return self
        else:
            r = self
            for i in [0,1,2,3]:
                if self.child[i] != None:
                    rr = self.child[i].getMinDis()
                    if rr.root[4][2] < r.root[4][2]:
                        r = rr
                    elif rr.root[4][2] == r.root[4][2]:
                        r == rr
            return r


    def addDeep(self):#增加一层遍历
        if self.deep == 1:
            p0 = self.root[4][0]
            p1 = self.root[4][1]
            ps = self.root[4][3]
            c = [True,True,True,True]
            
            if ps == 0:
                c[1] = False
            elif ps == 1:
                c[0] = False
            elif ps == 2:
                c[3] = False
            elif ps == 3:
                c[2] = False

            if p0 == 0:
                c[0] = False
            if p0 == 3:
                c[1] = False
            if p1 == 0:
                c[2] = False
            if p1 == 3:
                c[3] = False
            for s in [0,1,2,3]:
                if c[s] == True:
                    ctmp = nextPuzzle(self.root, s, True)
                    self.child[s] = Tree(ctmp) 
            self.deep += 1
        else:
            for s in [0,1,2,3]:
                if self.child[s] != None:
                    self.child[s].addDeep()
            self.deep += 1

#puzzle = np.array([[5,0,15,3],[8,1,2,6],[4,12,13,11],[9,14,7,10]])
#puzzle = np.array(Target)
#distance = dis(puzzle)

newp = np.array(Target)
rufflePuzzle(newp, 500)
print(newp)

newp[4][3] = 44
m = Tree(newp)

while m.root[4][2] != 0:
    for i in np.arange(10):
        m.addDeep()
    m = m.getMinDis()
    print(m.root)
    m = Tree(m.root)

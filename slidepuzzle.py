#!/usr/bin/python
# -*- coding:utf-8 -*- 
import numpy as np
import random

#Target[3][3][0:1]:0的位置;Target[3][3][2]:距离;Target[3][3][3]:上一步操作：4表示初始化和无操作
Target = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0],[3,3,0,4]])

#距离矩阵：表示[4][4]矩阵每一位距离正确的数的距离
DistanceMatrix = np.empty([4,4,16],dtype='int32')


for i in [0,1,2,3]:
    for j in [0,1,2,3]:
        for k in np.arange(16):
            if k == 0:
                i2 = 3
                j2 = 3
            else:
                i2 = (k-1)/4
                j2 = (k-1)%4
            DistanceMatrix[i][j][k] = abs(i2-i) + abs(j2-j)

            

def show(x):
	print("%2d %2d %2d %2d"%(x[0][0],x[0][1],x[0][2],x[0][3]))
	print("%2d %2d %2d %2d"%(x[1][0],x[1][1],x[1][2],x[1][3]))
	print("%2d %2d %2d %2d"%(x[2][0],x[2][1],x[2][2],x[2][3]))
	print("%2d %2d %2d %2d"%(x[3][0],x[3][1],x[3][2],x[3][3]))
	return

def dis(x):
	d = 0
	for i in [0,1,2,3]:
		for j in [0,1,2,3]:
			d += DistanceMatrix[i][j][x[i][j]]
	return d

#0:上 1:下 2:左 3:右 其他：不操作
def nextPuzzle(x,s,new):
    p0 = x[4][0]
    p1 = x[4][1]
    newP = None
    if s == 0:
        if p0 != 0:
            a = x[p0-1][p1]
            b = DistanceMatrix[p0][p1][a]+DistanceMatrix[p0-1][p1][0]-DistanceMatrix[p0][p1][0]-DistanceMatrix[p0-1][p1][a]
            
            if new == True:
                newP = np.array(x)
                newP[p0][p1] = a
                newP[p0-1][p1] = 0
                newP[4][0] = p0-1
                newP[4][1] = p1
                newP[4][2] = x[4][2]+b
                newP[4][3] = 0
            else:
                x[p0][p1] = a
                x[p0-1][p1] = 0
                x[4][0] = p0-1
                x[4][1] = p1
                x[4][2] += b
                x[4][3] = 0
        
    elif s == 1:
        if p0 != 3:
            a = x[p0+1][p1]
            b = DistanceMatrix[p0][p1][a]+DistanceMatrix[p0+1][p1][0]-DistanceMatrix[p0][p1][0]-DistanceMatrix[p0+1][p1][a]
            
            if new == True:
                newP = np.array(x)
                newP[p0][p1] = a
                newP[p0+1][p1] = 0
                newP[4][0] = p0+1
                newP[4][1] = p1
                newP[4][2] = x[4][2]+b
                newP[4][3] = 1
            else:
                x[p0][p1] = a
                x[p0+1][p1] = 0
                x[4][0] = p0+1
                x[4][1] = p1
                x[4][2] += b
                x[4][3] = 1
		
    elif s == 2:
        if p1 != 0:
            a = x[p0][p1-1]
            b = DistanceMatrix[p0][p1][a]+DistanceMatrix[p0][p1-1][0]-DistanceMatrix[p0][p1][0]-DistanceMatrix[p0][p1-1][a]
		
            if new == True:
                newP = np.array(x)
                newP[p0][p1] = a
                newP[p0][p1-1] = 0
                newP[4][0] = p0
                newP[4][1] = p1-1
                newP[4][2] = x[4][2]+b
                newP[4][3] = 2
            else:
                x[p0][p1] = a
                x[p0][p1-1] = 0
                x[4][0] = p0
                x[4][1] = p1-1
                x[4][2] += b
                x[4][3] = 2
                
    elif s == 3:
        if p1 != 3:
            a = x[p0][p1+1]
            b = DistanceMatrix[p0][p1][a]+DistanceMatrix[p0][p1+1][0]-DistanceMatrix[p0][p1][0]-DistanceMatrix[p0][p1+1][a]
            
            if new == True:
                newP = np.array(x)
                newP[p0][p1] = a
                newP[p0][p1+1] = 0
                newP[4][0] = p0
                newP[4][1] = p1+1
                newP[4][2] = x[4][2]+b
                newP[4][3] = 2
            else:
                x[p0][p1] = a
                x[p0][p1+1] = 0
                x[4][0] = p0
                x[4][1] = p1+1
                x[4][2] += b
                x[4][3] = 2
    return newP

#rufflePuzzle:
def rufflePuzzle(x,d):
    
    while(x[4][2] < d):
        
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

    def getDeep(self):
        return self.deep

    def printTree(self):#深度遍历
        show(self.root)
        for i in [0,1,2,3]:
            if(self.child[i] != None):
                printTree(self)

    def addDeep(self):#增加一层遍历
        if(self.deep == 1):
            p0 = self.root[3][3][0]
            p1 = self.root[3][3][1]
            if(p0 == 0):
                self.child[0] = None
                
show(Target)
newp = np.array(Target)
rufflePuzzle(newp, 40)
print(newp)

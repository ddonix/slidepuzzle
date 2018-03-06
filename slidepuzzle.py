#!/usr/bin/python
# -*- coding:utf-8 -*- 
import numpy as np

def show(x):
	print("%2d %2d %2d %2d"%(x[0][0],x[0][1],x[0][2],x[0][3]))
	print("%2d %2d %2d %2d"%(x[1][0],x[1][1],x[1][2],x[1][3]))
	print("%2d %2d %2d %2d"%(x[2][0],x[2][1],x[2][2],x[2][3]))
	print("%2d %2d %2d %2d"%(x[3][0],x[3][1],x[3][2],x[3][3]))
	return

def step(x,t):
	tmp = np.array(x)
	show(tmp)
	return

p = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0],[3,3,0,0]]
X = np.array(p)

D = np.empty([4,4,16],dtype='int32')
for i in [0,1,2,3]:
	for j in [0,1,2,3]:
		for k in np.arange(16):
			if k == 0:
				i2 = 3
				j2 = 3
			else:
				i2 = (k-1)/4
				j2 = (k-1)%4
			D[i][j][k] = abs(i2-i) + abs(j2-j)


def dis(x):
	d = 0
	for i in [0,1,2,3]:
		for j in [0,1,2,3]:
			d += D[i][j][x[i][j]]
	return d

#0:上 1:下 2:左 3:右 其他：不操作
def tran(x,s):
	p0 = 0
	p1 = 0
	for i in s:
		p0 = x[4][0]
		p1 = x[4][1]
		if i == 0:
			if p0 == 0:
				continue
			a = x[p0-1][p1]
			b = D[p0][p1][a]+D[p0-1][p1][0]-D[p0][p1][0]-D[p0-1][p1][a]
			x[4][2] += b
			x[p0][p1] = a
			x[p0-1][p1] = 0
			x[4][0] = p0-1
			x[4][1] = p1
		elif i == 1:
			if p0 == 3:
				continue
			a = x[p0+1][p1]
			x[4][2] += D[p0][p1][a]+D[p0+1][p1][0]-D[p0][p1][0]-D[p0+1][p1][a]
			x[p0][p1] = a
			x[p0+1][p1] = 0
			x[4][0] = p0+1
			x[4][1] = p1
		elif i == 2:
			if p1 == 0:
				continue
			a = x[p0][p1-1]
			x[4][2] += D[p0][p1][a]+D[p0][p1-1][0]-D[p0][p1][0]-D[p0][p1-1][a]
			x[p0][p1] = a
			x[p0][p1-1] = 0
			x[4][0] = p0
			x[4][1] = p1-1
		elif i == 3:
			if p1 == 3:
				continue
			a = x[p0][p1+1]
			x[4][2] += D[p0][p1][a]+D[p0][p1+1][0]-D[p0][p1][0]-D[p0][p1+1][a]
			x[p0][p1] = a
			x[p0][p1+1] = 0
			x[4][0] = p0
			x[4][1] = p1+1
		else:
			continue
	return

print(D)
show(X)
t = np.random.randint(5,size=300)
print(t)
tran(X,t)
show(X)
print(X[4])

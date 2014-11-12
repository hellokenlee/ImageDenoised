# -*- coding: utf-8 -*-  
from PIL import Image
import copy
import random
import datetime,time
starttime = datetime.datetime.now()
im=Image.open("origin_hard.jpg")
#参数
h=0
B=1.05
u=2.1
dx=[0,0 ,1,1, 1,-1,-1,-1]
dy=[1,-1,0,1,-1, 1,-1, 0]
width=im.size[0]
height=im.size[1]
###比较两幅图片的不同像素###
def cmp(pic1,pic2):
	im1=Image.open(pic1)
	im2=Image.open(pic2)
	im1PixData=im1.load()
	im2PixData=im2.load()
	cnt=0
	for x in range(im1.size[0]):
		for y in range(im1.size[1]):
			if im1PixData[x,y]!=im2PixData[x,y]:
				cnt=cnt+1
	return cnt

###更改一个点后计算能量是否增加###
###因为每一个点取值为0 or 1，计算的时候都减0.5 变成-0.5 or 0.5###
def differEnergy(Z,A,x,y):
	ZpixData=Z.load()
	ApixData=A.load()
	E=0
	E=E+(ApixData[x,y]-0.5)*h
	E=E-(ZpixData[x,y]-0.5)*(ApixData[x,y]-0.5)*u
	for i in range(0,8):
		x1=x+dx[i]
		y1=y+dy[i]
		if x1>=0 and x1<A.size[0] and y1>=0 and y1<A.size[1]:
			E=E-(ApixData[x,y]-0.5)*(ApixData[x1,y1]-0.5)*B
	return E

###二值化原始图片并保存在bin-vlue.bmp 阀值固定250#### 
Lim=im.convert("L")
threshold = 250
table = []
for i in range(width):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
Bim=Lim.point(table, '1')
Bim.save("bin-value.bmp","BMP")

###生成噪声 10%的概率 pixData[x,y]=1为白色 0为黑色###
pixData=Bim.load()
for x in range(0,Bim.size[0]):
	for y in range(0,Bim.size[1]):
		tmp=random.uniform(0,10)
		if tmp<1:
			pixData[(x,y)]=not(pixData[(x,y)])
#Bim.show()
Bim.save("noised.bmp","BMP")




###随机生成选最优###
minEnergyIm=Bim.copy()
##优化##
MimpixData=minEnergyIm.load()
for x in range(width):
	for y in range(height):
		MimpixData[x,y]=not(MimpixData[x,y])
		if differEnergy(Bim,minEnergyIm,x,y)>0:
			MimpixData[x,y]=not(MimpixData[x,y])

minEnergyIm.save("predenoised.bmp","BMP")
maxBFSnum=400
BFSCounter=0;
depth=0
times=0
while(BFSCounter<maxBFSnum):
	minE=10000
	###随机BFS 5次选最优的一次##$
	for i in range(0,5):
		times=times+1
		Cim=minEnergyIm.copy()
		CimPixData=Cim.load()
		randx=int(random.uniform(0,width))
		randy=int(random.uniform(0,height))
		CimPixData[randx,randy]=not(CimPixData[randx,randy])
		E=differEnergy(Bim,Cim,randx,randy)
		if E<minE:
			#print "E:",E
			minE=E
			minIm=Cim.copy()
	#在5次中找到使能量降低的
	if minE<0:
		#print  "minE in 100 rounds:",minE
		minEnergyIm=minIm.copy()
		BFSCounter=0
		depth=depth+1
	else:
		BFSCounter=BFSCounter+1


##优化##
MimpixData=minEnergyIm.load()
for x in range(width):
	for y in range(height):
		MimpixData[x,y]=not(MimpixData[x,y])
		if differEnergy(Bim,minEnergyIm,x,y)>0:
			MimpixData[x,y]=not(MimpixData[x,y])

###输出并保存###
minEnergyIm.save("denoised.bmp","BMP")
print "circle times:",times
print "search depth:",depth
print "total time used:",
endtime = datetime.datetime.now()
print (endtime - starttime).seconds,"secs"
nP1=cmp("noised.bmp","bin-value.bmp")
nP2=cmp("denoised.bmp","bin-value.bmp")
print "differ(noised,bin-value):",nP1
print "differ(denoised,bin-value):",nP2
rate=(1-float(nP2)/float(nP1))*100
print "denoisedRate:",
print ('%.2f'%(rate)),"%"

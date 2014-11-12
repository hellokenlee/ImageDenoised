# -*- coding: utf-8 -*-  
from PIL import Image
import copy
import random
im=Image.open("origin.jpg")
#参数
h=4
B=4.1
u=1
def Energy(Z,A):
	ZpixData=Z.load()
	ApixData=A.load()
	E1=0
	for x in range(Z.size[0]):
		for y in range(Z.size[1]):
			E1=E1+ApixData[x,y]
	E1=E1*h
	E2=0
	for x in range(Z.size[0]-1):
		for y in range(Z.size[1]-1):
			E2=E2+ApixData[x,y]*ApixData[x+1,y]+ApixData[x,y]*ApixData[x,y+1]
	E2=E2*B
	E3=0
	for x in range(Z.size[0]-1):
		for y in range(Z.size[1]-1):
			E3=E3+ZpixData[x,y]*ApixData[x,y]
	E3=E3*u
	#print "E: ",E1,E2,E3
	return (E1-E2-E3)

###二值化原始图片并保存在bin-vlue.bmp 阀值固定250#### 
Lim=im.convert("L")
threshold = 250
table = []
for i in range(256):
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

##把0变成-1
for x in range(0,Bim.size[0]):
	for y in range(0,Bim.size[1]):
		if pixData[x,y]==0:
			pixData[x,y]=-1

###随机生成选最优###
maxEnery=Energy(Bim,Bim)
maxEneryIm=Bim.copy()
print "origin:",maxEnery
for i in range(0,100000):
	Cim=maxEneryIm.copy()
	CpixData=Cim.load()
	for j in range(0,1):
		ranx=int(random.uniform(0,256))
		rany=int(random.uniform(0,256))
		CpixData[ranx,rany]=not(CpixData[ranx,rany])
	E=Energy(Bim,Cim)
	if E<maxEnery:
		print E
		maxEnery=E
		maxEneryIm=Cim.copy()

###输出并保存###
mpixData=maxEneryIm.load()
for x in range(0,256):
	for y in range(0,256):
		if mpixData[x,y]==-1:
			mpixData[x,y]=0
maxEneryIm.save("denoised.bmp","BMP")
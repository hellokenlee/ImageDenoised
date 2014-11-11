# -*- coding: utf-8 -*-  
from PIL import Image
import random
im=Image.open("a.jpg")

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
			pixData[x,y]=~pixData[x,y]
Bim.show()
Bim.save("bin-value-noise.bmp","BMP")
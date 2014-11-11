# -*- coding: utf-8 -*-  
from PIL import Image
im1=Image.open("bin-value-noise.bmp")
im2=Image.open("denoised.bmp")
im1PixData=im1.load()
im2PixData=im2.load()
cnt=0
for x in range(im1.size[0]):
	for y in range(im1.size[1]):
		if im1PixData[x,y]!=im2PixData[x,y]:
			cnt=cnt+1
print cnt
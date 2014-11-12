# -*- coding: utf-8 -*-  
from PIL import Image
import  sys
im1=Image.open(sys.argv[1])
im2=Image.open(sys.argv[2])
im1PixData=im1.load()
im2PixData=im2.load()
cnt=0
for x in range(im1.size[0]):
	for y in range(im1.size[1]):
		if im1PixData[x,y]!=im2PixData[x,y]:
			cnt=cnt+1
print "diff("+sys.argv[1]+","+sys.argv[2]+"):",cnt
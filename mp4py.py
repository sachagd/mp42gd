from PIL import Image
from os import listdir
import os
import cv2
import numpy
import json
import timeit


for file in listdir(".\\img"):
    os.remove(".\\img\\"+file)

def compress(image,L,l,beg,end):
    img=[]
    for i in range(l):
        img.append([])
        for j in range(L):
            if beg[1]<=round(len(image)/l*i)<=end[1] and beg[0]<=round(len(image[i])/L*j)<=end[0]:
                img[-1].append(image[round(len(image)/l*i)][round(len(image[i])/L*j)])
        if img[-1]==[]:
            del img[-1]
    return numpy.array(img)

vidcap = cv2.VideoCapture(".\\video\\"+listdir(".\\video")[0])
success,image = vidcap.read()
count = 0
while success:
    image=compress(image,96,54,(0,0),(1920,1080))
    cv2.imwrite(".\\img\\%d.png" % count, image)
    success,image = vidcap.read()
    count += 1

def mp42info():
    info=[]
    for i in range(len(listdir(".\\img"))):
        print(str(i)+"/"+str(len(listdir(".\\img"))))
        img=Image.open(".\\img\\%d.png"%i)
        img=img.convert('HSV')
        info.append(png2info(1,img))
    for i in range(len(info)):
        j=0
        while j+1<len(info[i][0]):
            if len(info[i][0][j])==len(info[i][0][j+1])==1:
                info[i][0][j][0]+=1
                del info[i][0][j+1]
                if j+1==len(info[i][0]) or len(info[i][0][j+1])>1:
                    info[i][0][j]=info[i][0][j][0]-img.size[0]+1
                    j+=1
            else:
                j+=1
    n=0
    for i in range(len(info)):
        for j in range(len(info[i][0])):
            if type(info[i][0][j])==list:
                for k in range(len(info[i][0][j])):
                    if type(info[i][0][j][k])==list:
                        n+=len(info[i][0][j][k])//2
                        if type(info[i][0][j][k][-1])==str:
                            n+=1
                    elif type(info[i][0][j][k])==str:
                        n+=1
    print(n+2*len(info)+3)
    jsn=open("info.json","w")
    json.dump(info, jsn, indent = 6)
    jsn.close()

def png2info(fcg,img):
    l,hsvgc,obj_color,nb,gc2hsv=[],[],[],{},{}
    for i in range(img.size[1]):
        obj_color.append([])
        for j in range(img.size[0]):
            hsv=[round(img.getpixel((j,i))[0]*360/255),round(img.getpixel((j,i))[1]/255,2),round(img.getpixel((j,i))[2]/255-1)]
            if hsv in l:
                obj_color[i].append(hsvgc[l.index(hsv)][0])
                nb[hsvgc[l.index(hsv)][0]]+=1
            else:
                l.append(hsv)
                hsvgc.append([str(fcg+len(hsvgc))+"c",hsv])
                obj_color[i].append(str(fcg+len(hsvgc)-1)+"c")
                nb[str(fcg+len(hsvgc)-1)+"c"]=1
    nb=[[nb[i],i] for i in nb]
    nb.sort(reverse=True)
    for i in range(len(nb)):
        if nb[i][0]>1:
            for j in range(len(obj_color)):
                for k in range(len(obj_color[j])):
                    condition,condition2,n=False,False,0
                    while condition==False and n<min(img.size[1]-j,img.size[0]-k):
                        for l in range(n):
                            if obj_color[j+n][k+l]==1 or obj_color[j+l][k+n]==1:
                                condition=True
                            if type(obj_color[j+n][k+l])==list:
                                if obj_color[j+n][k+l][-1]==1:
                                    condition=True
                            if type(obj_color[j+l][k+n])==list:
                                if obj_color[j+l][k+n][-1]==1:
                                    condition=True
                        if obj_color[j+n][k+n]==1:
                            condition=True
                        elif type(obj_color[j+n][k+n])==list:
                            if obj_color[j+n][k+n][-1]==1:
                                condition=True
                        if condition2==False and condition==False:
                            for l in range(n):
                                if obj_color[j+n][k+l]==nb[i][1] or obj_color[j+l][k+n]==nb[i][1]:
                                    condition2=True
                                if type(obj_color[j+n][k+l])==list:
                                    if obj_color[j+n][k+l][-1]==nb[i][1]:
                                        condition2=True
                                if type(obj_color[j+l][k+n])==list:
                                    if obj_color[j+l][k+n][-1]==nb[i][1]:
                                        condition2=True
                            if obj_color[j+n][k+n]==nb[i][1]:
                                condition2=True
                            elif type(obj_color[j+n][k+n])==list:
                                if obj_color[j+n][k+n]==nb[i][1]:
                                    condition2=True
                        if condition==False:
                            n+=1
                    if n>1 and condition2==True:
                        for l in range(j,j+n):
                            for m in range(k,k+n):
                                if obj_color[l][m]==nb[i][1]:
                                    obj_color[l][m]=1
                                elif type(obj_color[l][m])==list:
                                    if obj_color[l][m][-1]==nb[i][1]:
                                        obj_color[l][m][-1]=1
                        if type(obj_color[j][k])==list:
                            obj_color[j][k]=[nb[i][1],n]+obj_color[j][k]
                        else:
                            obj_color[j][k]=[nb[i][1],n,obj_color[j][k]]
    nb=[i[1] for i in nb]
    for i in hsvgc:
        gc2hsv[i[0]]=i[1]+[nb.index(i[0])]
    for i in range(len(obj_color)):
        j=0
        while j+1<len(obj_color[i]):
            if type(obj_color[i][j])==int and obj_color[i][j+1]==1:
                obj_color[i][j]+=1
                del obj_color[i][j+1]
            else:
                j+=1
    return [obj_color,gc2hsv]

mp42info()
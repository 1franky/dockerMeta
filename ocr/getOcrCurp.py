from PIL import Image   
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pyocr
import pyocr.builders
import os
from shutil import copy, move
import re

def filtroImg0(imgPath, savePath):
    I = Image.open(imgPath)
    imgGray = I.convert('L')
    # print(np.array(imgGray).shape)
    a = np.array(imgGray)
    cv2.imwrite(savePath, a)
    return a

def filtroImg1(imgPath, savePath):
    I = Image.open(imgPath)
    imgGray = I.convert('L')
    # print(np.array(imgGray).shape)
    a = np.array(imgGray)
    for i, r in enumerate(a):
        for j, g in enumerate(r):
            a[i][j] = 0 if g <= 70 else 255
    cv2.imwrite(savePath, a)
    return a

def filtroImg2(imgPath, savePath):
    I = Image.open(imgPath)
    imgGray = I.convert('L')
    # print(np.array(imgGray).shape)
    a = np.array(imgGray)
    for i, r in enumerate(a):
        for j, g in enumerate(r):
            a[i][j] = 0 if g <= 100 else 255
    cv2.imwrite(savePath, a)
    return a

def filtroImg3(imgPath, savePath):
    I = Image.open(imgPath)
    imgGray = I.convert('L')
    # print(np.array(imgGray).shape)
    a = np.array(imgGray)
    for i, r in enumerate(a):
        for j, g in enumerate(r):
            if g < 128:
                a[i][j] = 0 if int(g/3) < 23 else int((g/3) * 3)
            else:
                a[i][j] = 255
    cv2.imwrite(savePath, a)
    return a

def filtroImg4(imgPath, savePath):
    I = Image.open(imgPath)
    imgGray = I.convert('L')
    # print(np.array(imgGray).shape)
    a = np.array(imgGray)
    for i, r in enumerate(a):
        for j, g in enumerate(r):
            if g < 50:
                a[i][j] = 0
            elif g < 100:
                a[i][j] = 10
            elif g < 120:
                a[i][j] = 120
            elif g < 200:
                a[i][j] = 255
            elif g <= 255:
                a[i][j] = 255
    cv2.imwrite(savePath, a)
    return a

def ocr(imgPath):
    tool = pyocr.get_available_tools()[0]
    lang = 'spa'
    text = tool.image_to_string(Image.open(imgPath), lang=lang, builder=pyocr.builders.TextBuilder())
    return text

def buscaCurp(text, savePath=""):
    tmp = text.replace("\n", " ", 999999)
    n = tmp.split(" ")
    curps = []
    for i in n:
        if len(i) == 18:
            curps.append(i)
    return curps

def corrigeCurp(texto):
    def replace(tex):
        x = tex
        x = x.replace("O", "0", 9)
        x = x.replace("Z", "2", 9)
        x = x.replace("S", "5", 9)
        x = x.replace("!", "1", 9)
        x = x.replace("G", "6", 9)
        x = x.replace("B", "8", 9)
        x = x.replace("T", "7", 9)
        x = x.replace("E", "6", 9)
        return x

    names = texto[:4]
    fecha = texto[4:10]
    codig = texto[10:16]
    digig = texto[16:18]
    valid = True

    fecha = replace(fecha)
    digig = replace(digig)

    try:
        tmp = int(fecha)
        tmp = int(digig)
    except:
        valid = False
    
    posibleCurp = "{}{}{}{}".format(names,fecha,codig,digig)
    # regex = re.compile(r'([A-Z&]|[a-z&]{1})([AEIOU]|[aeiou]{1})([A-Z&]|[a-z&]{1})([A-Z&]|[a-z&]{1})([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])([HM]|[hm]{1})([AS|as|BC|bc|BS|bs|CC|cc|CS|cs|CH|ch|CL|cl|CM|cm|DF|df|DG|dg|GT|gt|GR|gr|HG|hg|JC|jc|MC|mc|MN|mn|MS|ms|NT|nt|NL|nl|OC|oc|PL|pl|QT|qt|QR|qr|SP|sp|SL|sl|SR|sr|TC|tc|TS|ts|TL|tl|VZ|vz|YN|yn|ZS|zs|NE|ne]{2})([^A|a|E|e|I|i|O|o|U|u]{1})([^A|a|E|e|I|i|O|o|U|u]{1})([^A|a|E|e|I|i|O|o|U|u]{1})([0-9]{2})')
    regex = re.compile(r'^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$')
    curp  = regex.search(posibleCurp)
    # print(posibleCurp)
    # print(curp)
    if (curp != None):
        return True, posibleCurp
    else:
        return False, ""

def filtro(tipo):
    tipos = [".jpg", ".jpeg", ".png"]
    _, tmp = os.path.splitext(tipo)
    return True if tmp in tipos else False


def getOcr(nameCurp):
    images = "img"
    tmp = "filtro"
    
    here = os.getcwd()
    # pathImages = os.path.join(here, images)
    # pathTmp = os.path.join(here, tmp)
    pathImages = "img"
    pathTmp = "filtro"

    nameImage = nameCurp
    fullPathImg  = os.path.join("ocr", pathImages, nameImage)
    fullPathTmp  = os.path.join("ocr", pathTmp, nameImage)
    # fullPathImg = os.path.join(pathImages, nameImage)
    # fullPathTmp = os.path.join(pathTmp, nameImage)


    texto = ocr(fullPathImg)
    posiblesCurps = buscaCurp(texto)
    # print(posiblesCurps)

    encontrado = False
    flag = 0
    filtroImgs = False
    # while(not encontrado) and flag <= 5:

    Curps = set()
    while flag <= 5:
        for curp in posiblesCurps:
            encontradoX, newCurp = corrigeCurp(curp)
            if encontradoX:
                Curps.add(newCurp)
                encontrado = True
            # if encontrado:
            #     break
    
        # if not encontrado:
        flag+=1
        if flag == 1:
            x = filtroImg0(fullPathImg, fullPathTmp)
        elif flag == 2:
            x = filtroImg1(fullPathImg, fullPathTmp)
        elif flag == 3:
            x = filtroImg2(fullPathImg, fullPathTmp)
        elif flag == 4:
            x = filtroImg3(fullPathImg, fullPathTmp)
        elif flag == 4:
            x = filtroImg4(fullPathImg, fullPathTmp)

        texto = ocr(fullPathTmp)
        posiblesCurps =  buscaCurp(texto)
        # encontrado = False
        filtroImgs = True
    
    try:
        os.remove(fullPathImg)
        os.remove(fullPathTmp)
    except:
        pass
    print("\n\n\n\n{}\n\n\n\n".format(list(Curps)))
    if encontrado:
        return {
            "r" : True,
            "curp" : list(Curps)
        }
    else:
        return {
            "r" : False,
            "curp" : []
        }
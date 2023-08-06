#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 19:51:31 2019

@author: mikeronni
"""

from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.colors import HexColor

#Define functions=======================================================
def simplestring(c,x,y,string,fontc,font_w,fontsize):
    try:
        c.setFillColor(HexColor(fontc))
    except:
        c.setFillColor(fontc)
    c.setFont(font_w,fontsize,leading=None)
    c.drawString(x,y,string)
    
def simpleCentredstring(c,x,y,string,fontc,font_w,fontsize):
    try:
        c.setFillColor(HexColor(fontc))
    except:
        c.setFillColor(fontc)
    c.setFont(font_w,fontsize,leading=None)
    c.drawCentredString(x,y,string)

def complexCentredstring(c,xmid,y,strings,fontcs,font_ws,fontsizes):
    str_widths=[]
    for s,fw,fsz in zip(strings,font_ws,fontsizes):
        str_widths.append(stringWidth(s,fw,fsz)) #Get string widths
    x = xmid-(sum(str_widths)/2) #Define initial x location based on string widths
    for s,fw,fsz,fc,sw in zip(strings,font_ws,fontsizes,fontcs,str_widths):
        try:
            c.setFillColor(HexColor(fc))
        except:
            c.setFillColor(fc)
        c.setFont(fw,fsz,leading=None)
        c.drawString(x,y,s)
        x += sw + 1
#NEED TO CONVERT CHART DIMENSIONS TO INCHES (/INCHES OR /72) WHEN USING THESE...
def left_im_cntr(c,chartw,margin,centermrgn,pagew): #MARGIN SHOULD INCLUDE "BLEED" SPACE, IF APPLICABLE
    res1 = pagew/2 - centermrgn/2 #1. Get distance to center minus half the center margin
    res2 = res1 - chartw #2. Subtract width of chart
    res3 = res2 - margin #3. Subtract margin (with bleed)
    res4 = res3 / 2 #4. Divide result by 2
    res5 = res4 + margin #5. Add result to margin
    res6 = res5 + (chartw / 2)#6. Get center of chart x location to center title
    return res5, res6

def right_im_cntr(c,chartw,margin,centermrgn,pagew):
    res1 = pagew - margin #1. Get distance to edge minus margin
    res2 = res1 - chartw #2. Subtract width of chart
    res3 = res2 - (pagew/2+centermrgn/2) #assumes crop is already added to pagew
    #res3 = res2 - centermrgn #3. Subtract distance to right edge of center margin
    res4 = res3 / 2 #4. Divide result by 2
    res5 = res4 + pagew/2 + centermrgn/2 #5. Add result to right edge of center margin
    res6 = res5 + (chartw / 2)#6. Get center of chart x location to center title
    return res5, res6

def top_im_y(c,adj,pageh,charth,topmrgn): #assumes y = 0 is bottom of page
    res1 = pageh - topmrgn #1. get y location of bottom of top header
    res2 = res1 - charth #2. subtract height of image
    res3 = res2 - adj #3. shift down by adjusted amount (e.g. to make room for title)
    return res3

def under_im_y(c,adj,pageh,c_above_y,charth):
    res1 = c_above_y #1. get y location of bottom of chart above
    res2 = res1 - charth #2. subtract height of current chart
    res3 = res2 - adj #3. shift down by adjusted amount (e.g. to make room for title)
    return res3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 13:40:22 2022

@author: ab
"""
import numpy as np

def mq(r,c):
   f=np.sqrt(r**2+c**2)
   return f
def mq1d(r,c):
   f=r/np.sqrt(r**2+c**2)
   return f
def mq1dx(r,c):
   f=1/np.sqrt(r**2+c**2)
   return f
def mq2d(r,c):
   f=1/np.sqrt(r**2+c**2)-r**2/(r**2+c**2)**1.5
   return f
def mp(r,c):
   f=1/9.0*(4*c**2+r**2)*np.sqrt(r**2+c**2)-c**3/3*np.log(c+np.sqrt(r**2+c**2)) #MAPS MQ
   return f
def mp1d(r,c):
   f=r*(2/9.0*np.sqrt(r**2+c**2)+1.0/9.0*(4*c**2+r**2)/np.sqrt(r**2+c**2)-c**3/3/(c+np.sqrt(r**2+c**2))/np.sqrt(r**2+c**2))
   return f
def mp1dx(r,c):
   f=(2/9.0*np.sqrt(r**2+c**2)+1.0/9.0*(4*c**2+r**2)/np.sqrt(r**2+c**2)-c**3/3/(c+np.sqrt(r**2+c**2))/np.sqrt(r**2+c**2))
   return f
def mp2d(r,c):
   f=np.sqrt(r**2+c**2)
   return f
def tps(r,c):
    n=np.size(r)
    f=np.zeros(n)
    for i in range(n):
        if r[i]<1e-8:
            f[i]=0.
        else:
            f[i]=r[i]**2*np.log(r[i])
    return f

def imq(r,c):
   f=(r**2+c**2)**(-0.5)
   return f

def g(r,c):
   f=np.exp(-r/c)
   return f

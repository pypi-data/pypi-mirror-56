#!/usr/bin/env python
# coding: utf-8

# In[17]:


def autovalores(a, b, c, d):
    z=a*d-b*c
    r1=((a+d)+(((a+d)**2)-4*z)**(0.5))/2
    r2=((a+d)-(((a+d)**2)-4*z)**(0.5))/2
    
    if r1==r2:
        return r1
    
    return [r1, r2]

def determinante2(a, b, c, d):
    d=(a*d)-(b*c)
    return d

def determinante3(a, b, c, d, e, f, g, h, i):
    d=((a*e*i)+(b*f*g)+(c*d*h))-((g*e*c)+(h*f*a)+(i*d*b))
    return d


#competition.py

from scipy import integrate

ma = 0.1    #电枢质量
v0 = 0      #电枢初速度
z0 = 0      #电枢初位置

def F(t):
    pass

def a(t):
    return F(t)/ma

def v(t):
    return v0 + integrate.quad(a,0,t)[0]

def z(t):
    return z0 + integrate.quad(z,0,t)[0]


def compete():
    reason = {
        "Armature Run Time": 0 ,
        "Armature Speed" :   0 ,
        "Armature Ek":       0 ,
        "Armature Eta":      0
    }
    
    #后续编写：reason各量计算
    
    return reason
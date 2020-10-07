import sympy

#参数需要统一单位(SI)

#----------电枢参数----------
v0 = 0                  #初速度
z0 = 0                  #初始位置
Ma = 0.1                #电枢质量
m = int("9"*20)         #电枢分片数量

#----------电容器参数----------
U0 = 500                #电容器初始电压
Ra = 1                  #电容器内阻
La = 1                  #电容器内感

#----------电容器参数----------
Rd = 1                  #回路电阻
Ld = 1                  #回路电感
Rc = 1                  #驱动线圈等效电阻
Lc = 1                  #驱动线圈等效电感


def solvingEquation_7(Parameter_t):
    #求电枢轴向(z轴)电磁推力
    #应需要获取Parameter_Mcplj,Parameter_Ic以及Parameter_Ipj
    f = 0
    return f

def solvingEquation_8(Parameter_t):
    #求电枢在时刻t时的加速度
    #牛顿第二定律 F = ma
    a = solvingEquation_7(Parameter_t) / Ma
    return a

def solvingEquation_9(Parameter_t):
    #求电枢在时刻t时的速度
    t = sympy.symbols('t')
    v = sympy.integrate(solvingEquation_8(Parameter_t), (t, 0,Parameter_t))
    return v

def solvingEquation_10(Parameter_t):
    #求电枢在时刻t时的位移
    t = sympy.symbols('t')
    z = sympy.integrate(solvingEquation_9(Parameter_t), (t, 0,Parameter_t))
    return z
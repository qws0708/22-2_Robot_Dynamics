import numpy as np
import matplotlib.pyplot as plt
import math as m
from celluloid import Camera

#설정 값
fig = plt.figure()
ax = fig.subplots()

camera = Camera(fig)

pi =3.141592
a = pi/180

theta1 = 30*a          
theta2 = 60*a

L1 = 0.15               
L2 = 0.12

# 정기구학
T0_1 = np.array([[m.cos(theta1), -m.sin(theta1), 0, 0], [m.sin(theta1), m.cos(theta1), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])    	
T1_2 = np.array([[m.cos(theta2), -m.sin(theta2), 0, L1], [m.sin(theta2), m.cos(theta2), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
T2_3 = np.array([[1, 0, 0, L2], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

T0_2 = T0_1@T1_2
T0_3 = T0_1@T1_2@T2_3

Px1_1 = T0_2[0,3]
Py1_1 = T0_2[1,3]

Px1_2 = T0_3[0,3]
Py1_2 = T0_3[1,3]

totall_x = np.array([0, Px1_1, Px1_2])
totall_y = np.array([0, Py1_1, Py1_2])



#역기구학
i= ((0.1167)**2 + (0.1990)**2 - ((0.15)**2+(0.12)**2))/(2*L1*L2)
k= (1-(i**2))**(1/2)

theta2_1 = m.atan2(k,i)
theta1_1 = m.atan2(0.1990, 0.1167) -m.atan2(L2*k, L1+L2*i)


T_0_1 = np.array([[m.cos(theta1_1), -m.sin(theta1_1), 0, 0], [m.sin(theta1_1), m.cos(theta1_1), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])    	
T_1_2 = np.array([[m.cos(theta2_1), -m.sin(theta2_1), 0, L1], [m.sin(theta2_1), m.cos(theta2_1), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
T_2_3 = np.array([[1, 0, 0, L2], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

T_0_2 = T_0_1@T_1_2
T_0_3 = T_0_1@T_1_2@T_2_3

Px_1_1 = T_0_2[0,3]
Py_1_1 = T_0_2[1,3]

Px_1_2 = T_0_3[0,3]
Py_1_2 = T_0_3[1,3]

totall_x_1 = np.array([0, Px_1_1, Px_1_2])
totall_y_1 = np.array([0, Py_1_1, Py_1_2])


#자코비안
P1 = np.array([[L1*m.cos(theta1)+L2*m.cos(theta1+theta2)], [L1*m.sin(theta1)+L2*m.sin(theta1+theta2)]])      

jaco = np.array([[-L1*m.sin(theta1)-L2*m.sin(theta1+theta2), -L2*m.sin(theta1+theta2)], [L1*m.cos(theta1)+L2*m.cos(theta1+theta2), L2*m.cos(theta1+theta2)]])

d_theta = np.array([[2*a], [3*a]])

dP = jaco@d_theta

P2 = P1 + dP

px2=P2[0,0]             
py2=P2[1,0]

theta1_2 = theta1 + 2*a

px1 = L1*m.cos(theta1_2)
py1 = L1*m.sin(theta1_2)

totall_x_2 = np.array([0, px1, px2])
totall_y_2 = np.array([0, py1, py2])


#그래프 그리기
aa = Px1_1 - Px_1_1
bb = Py_1_1 - Py1_1

cc = Px1_2 - Px_1_2
dd = Py_1_2 - Py1_2

ee = aa/50
kk = cc/50

ff = bb/50
gg = dd/50


AA = Px1_1 - px1
BB = py1 - Py1_1

CC = Px1_2 - px2
DD = py2 - Py1_2

EE = AA/50
KK = CC/50

FF = BB/50
GG = DD/50


for i in range(50):
    plt.plot(totall_x,totall_y,'k')
    plt.text(Px1_2,Py1_2,'FK \n x: 0.12990385795292497 \ny: 0.19499998584935901')
    ax.plot( np.array([0, Px1_1 - ee*i, Px1_2 - kk*i]), np.array([0, Py1_1 + ff*i, Py1_2 + gg*i]),'b--')
    camera.snap()
    
for k in range(50):
    plt.plot(totall_x,totall_y,'k')
    plt.plot(totall_x_1,totall_y_1,'b')
    plt.text(Px1_2,Py1_2,'FK \n x: 0.12990385795292497 \ny: 0.19499998584935901')
    plt.text(Px_1_2,Py_1_2+0.01,'IK \n x:0.11669999999999997 \ny:0.199')
    ax.plot( np.array([0, Px1_1 - EE*k, Px1_2 - KK*k]), np.array([0, Py1_1 + FF*k, Py1_2 + GG*k]),'r--')
    camera.snap()

for i in range(100):
    plt.plot(totall_x,totall_y,'k')
    plt.plot(totall_x_1,totall_y_1,'b')  
    plt.plot(totall_x_2,totall_y_2,'r')
    plt.text(Px1_2,Py1_2,'FK \n x: 0.12990385795292497 \ny: 0.19499998584935901')
    plt.text(Px_1_2,Py_1_2+0.01,'IK \n x:0.11669999999999997 \ny:0.199')
    plt.text(px2 - 0.01,py2 - 0.01,'Jaco\n x:0.1168138917802091 \ny:0.19953448702393864')
    camera.snap()
    
animation = camera.animate()
plt.show()




    

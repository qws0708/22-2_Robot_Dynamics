import numpy as np
import matplotlib.pyplot as plt
import math as m
from celluloid import Camera
from time import sleep
import matplotlib.animation as animation


#설정 값
fig = plt.figure()
ax = fig.subplots()

camera = Camera(fig)

theta1 = 0.4028          
theta2 = 1.8755

L1 = 5               
L2 = 4

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

totall_x = np.array([0, Px1_1, 2.0])
totall_y = np.array([0, Py1_1, 5.0])

print(totall_x)
print(totall_y)


#역기구학
i= ((4.5)**2 + (6.5)**2 - ((5)**2+(4)**2))/(2*5*4) #cos2
k= (1-(i**2))**(1/2)    #sin2

theta2_1 = m.atan2(k,i) #theta2
theta1_1 = m.atan2(6.5, 4.5) -m.atan2(L2*k, L1+L2*i)    #theta1


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

print(totall_x_1)
print(totall_y_1)


#그래프 그리기
aa = Px1_1 - Px_1_1
bb = Py_1_1 - Py1_1

cc = Px1_2 - Px_1_2
dd = Py_1_2 - Py1_2

ee = aa/10
kk = cc/10

ff = bb/10
gg = dd/10

col = ['g','r','c','m','y','k','violet','limegreen','dodgerblue','b']

x = [2.0, 4.5]
y=  [5.0, 6.5]




for i in range(10):
    plt.plot(totall_x,totall_y,'b')
    plt.plot(np.array([0, Px1_1 - ee*(i+1), Px1_2 - kk*(i+1)]), np.array([0, Py1_1 + ff*(i+1), Py1_2 + gg*(i+1)]),color = col[i])
    plt.plot(x,y,'k')
    camera.snap()

animation = camera.animate(interval=1000, repeat=False)

plt.show(block=False)
plt.pause(11)
plt.close()

for i in range(10):
    plt.plot(totall_x,totall_y,'b')
    plt.plot(np.array([0, Px1_1 - ee*(i+1), Px1_2 - kk*(i+1)]), np.array([0, Py1_1 + ff*(i+1), Py1_2 + gg*(i+1)]),color = col[i])
    plt.plot(x,y,'k')

plt.show()

# LSPB 궤적 계획법
# 최대 속도값의 80%까지만 고려
# 초기 위치에서 목표위치까지 도달하는데 걸리는 시간 10초
# 링크1의 초기 위치 x=4.6 , y=2.0 // 목표 위치 x=4.3 , y=2.5
# 링크2의 초기 위치 x=2.0 , y=5.0 // 목표 위치 x=4.5 , y=6.5

time_sec = 10   #걸린시간
 
first_1 = 0.4028  #theta1 초기
first_2 = 0.5245  #theta1 최종

second_1 = 1.0033  #theta2 초기
second_2 = 1.8755  #theta2 최종

#링크 1 위치 그래프
velocity_1 = (2*(first_2 - first_1)/time_sec)*0.8    #이동속도
time_b = (first_1 - first_2 + (velocity_1*10))/velocity_1 #tb시간
ac_b = (velocity_1)**2/(first_1 - first_2 + velocity_1*10) #가속도
a = 4*(first_2 - first_1)/100 #가속도 제한 조건

print('속도 = ', velocity_1)
print('tb = ',time_b)
print('가속도 = ', ac_b)
print('가속도 제한 값 = ', a)


plt.subplot(331)
plt.title("Link1 Location Graph")
first_x = np.array(np.arange(0, time_b, 0.01))
plt.plot(first_x, first_1 + 0.5*ac_b*first_x**2, 'b')
plt.subplot(332)
plt.title("Link1 Velocity Graph")
plt.plot(first_x, ac_b*first_x, 'r')
apple = np.zeros(375) + ac_b
plt.subplot(333)
plt.title("Link1 Acceleration Graph")
plt.plot(first_x, apple, 'g')
x = [time_b, time_b]
y=  [ac_b, 0]
plt.plot(x, y, 'g')


plt.subplot(331)
second_x = np.array(np.arange(time_b, 10 - time_b, 0.01))
plt.plot(second_x, first_1 + ac_b*time_b*(second_x-0.5*time_b),'b')
plt.subplot(332)
apple2 = np.zeros(251) + ac_b * time_b
apple3 = np.zeros(251)
plt.plot(second_x, apple2 ,'r')
plt.subplot(333)
plt.plot(second_x, apple3, 'g')



plt.subplot(331)
third_x = np.array(np.arange(10 - time_b, 10, 0.01))
plt.plot(third_x, first_2 - 0.5*ac_b*((10 - third_x)**2), 'b')
plt.subplot(332)
plt.plot(third_x, ac_b*10 - ac_b*third_x, 'r')
apple4 = np.zeros(375) + ac_b
plt.subplot(333)
plt.plot(third_x, apple4, 'g')
x_1 = [10 - time_b,10 - time_b]
y_1 = [0, ac_b]
plt.plot(x_1, y_1, 'g')




#링크 2 위치 그래프
velocity_1 = (2*(second_2 - second_1)/time_sec)*0.8    #이동속도
time_b = (second_1 - second_2 + (velocity_1*10))/velocity_1 #tb시간
ac_b = (velocity_1)**2/(second_1 - second_2 + velocity_1*10) #가속도
a = 4*(second_2 - second_1)/100 #가속도 제한 조건

print('속도 = ', velocity_1)
print('tb = ',time_b)
print('가속도 = ', ac_b)
print('가속도 제한 값 = ', a)


plt.subplot(334)
plt.title("Link2 Location Graph")
first_x = np.array(np.arange(0, time_b, 0.01))
plt.plot(first_x, second_1 + 0.5*ac_b*first_x**2, 'b')
plt.subplot(335)
plt.title("Link2 Velocity Graph")
plt.plot(first_x, ac_b*first_x, 'r')
apple = np.zeros(376) + ac_b
plt.subplot(336)
plt.title("Link2 Acceleration Graph")
plt.plot(first_x, apple, 'g')
x = [time_b, time_b]
y=  [ac_b, 0]
plt.plot(x, y, 'g')


plt.subplot(334)
second_x = np.array(np.arange(time_b, 10 - time_b, 0.01))
plt.plot(second_x, second_1 + ac_b*time_b*(second_x-0.5*time_b),'b')
plt.subplot(335)
apple2 = np.zeros(250) + ac_b * time_b
apple3 = np.zeros(250)
plt.plot(second_x, apple2 ,'r')
plt.subplot(336)
plt.plot(second_x, apple3, 'g')



plt.subplot(334)
third_x = np.array(np.arange(10 - time_b, 10, 0.01))
plt.plot(third_x, second_2 - 0.5*ac_b*((10 - third_x)**2), 'b')
plt.subplot(335)
plt.plot(third_x, ac_b*10 - ac_b*third_x, 'r')
apple4 = np.zeros(375) + ac_b
plt.subplot(336)
plt.plot(third_x, apple4, 'g')
x_1 = [10 - time_b,10 - time_b]
y_1 = [0, ac_b]
plt.plot(x_1, y_1, 'g')

plt.show()



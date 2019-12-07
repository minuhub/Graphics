#########################################
'''

Computer Graphics Assignment2 
   -use at least 3-level of hierarchy

Student ID : 
Name : 
Date : 20180410

Hierarchy 3-level : 몸통, 허벅지, 정강이 


'''
#########################################

from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
import glfw

gCamAng = np.radians(30)

rotate_thigh_max = 30.0
rotate_thigh_min = -30.0
leftThigh_up = 1
rotate_thigh_angle = 0.0
rotate_shin_angle = 0.0
leftArm_up = 1
body_angle = 0
body_turn_clock = True
#size
headsize = 0.1
bodySize = (0.5, .1, .2)
thighSize = (.3, .06, .06) #허벅지,종아리 사이즈같은값 사용
armSize = (.5, .06, .06)

def drawFrame():
   glBegin(GL_LINES)
   glColor3ub(255, 0, 0)
   glVertex3fv(np.array([0.,0.,0.]))
   glVertex3fv(np.array([1.,0.,0.]))
   glColor3ub(0, 255, 0)
   glVertex3fv(np.array([0.,0.,0.]))
   glVertex3fv(np.array([0.,1.,0.]))
   glColor3ub(0, 0, 255)
   glVertex3fv(np.array([0.,0.,0]))
   glVertex3fv(np.array([0.,0.,1.]))
   glEnd()

def drawBox():
   glBegin(GL_QUADS)
   glVertex3fv(np.array([1,1,0.]))
   glVertex3fv(np.array([-1,1,0.]))
   glVertex3fv(np.array([-1,-1,0.]))
   glVertex3fv(np.array([1,-1,0.]))
   glEnd()

def drawSphere (numLats=12, numLongs=12):
    global bodySize, thighSize
    for i in range(0, numLats + 1):
      lat0 = np.pi*(-0.5 + float(float(i-1) / float(numLats)))
      z0 = np.sin(lat0)
      zr0 = np.cos(lat0)
      labodySize = np.pi*(-0.5 + float(float(i) / float(numLats)))
      z1 = np.sin(labodySize)
      zr1 = np.cos(labodySize)

      glBegin(GL_QUAD_STRIP)      
      glColor3ub(20+i*15, 20+i*15, 0)
      for j in range(0, numLongs + 1):
         lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
         x = np.cos(lng)
         y = np.sin(lng)
         glVertex3f(headsize*(x * zr0) + 0.1, 
            headsize*(y * zr0) - 0.5*bodySize[1],
            headsize*(z0)- 0.5*bodySize[2])
         glVertex3f(headsize*(x * zr1) + 0.1 , 
            headsize*(y * zr1) - 0.5*bodySize[1], 
            headsize*(z1) - 0.5*bodySize[2])    
      glEnd()

def drawCube(colorR,colorG,colorB):

   glColor3f(colorR,colorG,colorB)
   glBegin(GL_POLYGON)
   glVertex3f(0.0, 0.0, 0.0) # top face
   glVertex3f(0.0, 0.0, -1.0)
   glVertex3f(-1.0, 0.0, -1.0)
   glVertex3f(-1.0, 0.0, 0.0)
 
   glVertex3f(0.0, 0.0, 0.0); # front face
   glVertex3f(-1.0, 0.0, 0.0)
   glVertex3f(-1.0, -1.0, 0.0)
   glVertex3f(0.0, -1.0, 0.0)
 
   glVertex3f(0.0, 0.0, 0.0) # right face
   glVertex3f(0.0, -1.0, 0.0)
   glVertex3f(0.0, -1.0, -1.0)
   glVertex3f(0.0, 0.0, -1.0)

   glVertex3f(-1.0, 0.0, 0.0); # left face
   glVertex3f(-1.0, 0.0, -1.0)
   glVertex3f(-1.0, -1.0, -1.0)
   glVertex3f(-1.0, -1.0, 0.0)
 
   glVertex3f(0.0, -1.0, 0.0) # bottom face
   glVertex3f(0.0, -1.0, -1.0)
   glVertex3f(-1.0, -1.0, -1.0)
   glVertex3f(-1.0, -1.0, 0.0)
 
   glVertex3f(0.0, 0.0, -1.0); # back face
   glVertex3f(-1.0, 0.0, -1.0)
   glVertex3f(-1.0, -1.0, -1.0)
   glVertex3f(0.0, -1.0, -1.0)
 
   glEnd()


def render(camAng, count):
   glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
   global leftThigh_up, rotate_thigh_angle, leftArm_up
   global body_turn_clock,body_angle
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glEnable(GL_DEPTH_TEST) #뒤에그린 도형이 보이도록하는것.
   glLoadIdentity()
   glOrtho(-1.5,1.5, -1.5,1.5, -1,1)
   gluLookAt(.1*np.sin(camAng),0.1,.1*np.cos(camAng),
         0,0,0,
         0,1,0)

   #######################################
   #drawFrame()
   #몸통이동
   glTranslatef(-.5+(count%720)*.003, 0, 0)
   glRotatef(body_angle,1,0,0)#몸통좌우로 흔들
   glTranslatef(0,0.5*bodySize[1],0.5*bodySize[2])
   glPushMatrix()
   #몸통
   drawSphere()
   glScalef(bodySize[0],bodySize[1],bodySize[2])
   drawCube(0,0,255)
 
   #왼쪽허벅지+정강이
   glPopMatrix()
   glPushMatrix()
   glTranslatef(-bodySize[0], -0.5*bodySize[1], -bodySize[2])
   glRotatef(rotate_thigh_angle, 0, 0, 1)
   glTranslatef(0, 0.5*thighSize[1], 0)#다리회전움직임을 사각형의 중심으로 하기위해
   #왼쪽허벅지
   glPushMatrix()
   glScalef(thighSize[0], thighSize[1], thighSize[2])
   drawCube(255,0,0)
   #왼쪽정강이
   glPopMatrix()
   glTranslatef(-thighSize[0],0.,0.)
   if rotate_thigh_angle <= 0:
      glRotatef(2*rotate_thigh_angle,0,0,1)   
   glScalef(thighSize[0], thighSize[1], thighSize[2])
   drawCube(255,0,0)

   #오른쪽허벅지+정강이
   glPopMatrix()
   glPushMatrix()
   glTranslatef(-bodySize[0], -0.5*bodySize[1], thighSize[2])
   glRotatef(-rotate_thigh_angle, 0, 0, 1)
   glTranslatef(0, 0.5*thighSize[1], 0)
   #오른쪽허벅지
   glPushMatrix()
   glScalef(thighSize[0], thighSize[1], thighSize[2])
   drawCube(255,0,0)
   #오른쪽정강이
   glPopMatrix()
   glTranslatef(-thighSize[0],0.,0.)
   if -rotate_thigh_angle <= 0:
      glRotatef(-2*rotate_thigh_angle,0,0,1)   
   glScalef(thighSize[0], thighSize[1], thighSize[2])
   drawCube(255,0,0)

   #왼쪽팔
   glPopMatrix()
   glPushMatrix()
   glTranslatef(-0.2*bodySize[0], -0.5*bodySize[1], -bodySize[2])
   glRotatef(180, 0, 0, 1) #default가 앞으로 팔 뻗은 상태이기 위해서
   
   if leftArm_up == 1:
      glRotatef(-5*count%360, 0, 0, 1)
   glTranslatef(0, 0.5*armSize[1], 0)
   glPushMatrix()
   glScalef(armSize[0], armSize[1], armSize[2])
   drawCube(255,0,0)  
   glPopMatrix()


   #오른쪽팔
   glPopMatrix()
   glPushMatrix()
   glTranslatef(-0.2*bodySize[0], -0.5*bodySize[1], armSize[2])
   glRotatef(180, 0, 0, 1) #default가 앞으로 팔 뻗은 상태이기 위해서 
   
   if leftArm_up == 0:
      glRotatef(-5*count%360, 0, 0, 1)
   glTranslatef(0, 0.5*armSize[1], 0)
   glTranslatef(0, 0.5*armSize[1], 0)
   glPushMatrix()
   glScalef(armSize[0], armSize[1], armSize[2])
   drawCube(255,0,0)  
   glPopMatrix()
   glPopMatrix()


   ##################################################
   #30도마다 다리의 움직임 방향이 반대가 되도록함. 
   #print(rotate_thigh_angle)
   if rotate_thigh_angle >= rotate_thigh_max:
      leftThigh_up = 0
   elif rotate_thigh_angle <= rotate_thigh_min:
      leftThigh_up = 1
   #한번에 움직이는 다리각도 설정
   if leftThigh_up == 0:
      rotate_thigh_angle -= 2
   elif leftThigh_up == 1:
      rotate_thigh_angle += 2
   #팔 한번 돌릴때마다 팔 바꿔줌
   if 5*count%360 == 0:
      if leftArm_up ==1:
         leftArm_up =0
      elif leftArm_up == 0:
         leftArm_up =1 
   
   #body_turn
   if (5*(count+180)%360) == 0:
      if (body_turn_clock == True):
         body_turn_clock = False
      else:
         body_turn_clock = True

   if body_turn_clock == True:
      body_angle += 0.8
   elif body_turn_clock == False:
      body_angle -= 0.8
   #################################################
def key_callback(window, key, scancode, action, mods):
   global gCamAng
   # rotate the camera when 1 or 3 key is pressed or repeated
   if action==glfw.PRESS or action==glfw.REPEAT:
      if key==glfw.KEY_1:
         gCamAng += np.radians(-10)
      elif key==glfw.KEY_3:
         gCamAng += np.radians(10)

def main():
   if not glfw.init():
      return
   window = glfw.create_window(700,700,'2014004293', None,None)
   if not window:
      glfw.terminate()
      return
   glfw.make_context_current(window)
   glfw.set_key_callback(window, key_callback)
   glfw.swap_interval(1)

   count = 0
   while not glfw.window_should_close(window):
      glfw.poll_events()
      render(gCamAng, count)
      glfw.swap_buffers(window)
      count += 1

   glfw.terminate()
   
if __name__ == "__main__":
   main()

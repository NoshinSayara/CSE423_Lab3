from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math, random

W_Width, W_Height = 500,500


bx = by = 0
size_of_ball = 2
final = False
speed = 0.01

class point:
    def __init__(self):
        self.x=0
        self.y=0
        self.z=0


def crossProduct(a, b):
    result=point()
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x

    return result

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

def draw_points(x, y, s):
    glPointSize(s) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()



def specialKeyListener(key, x, y):
    global speed, frozen
    if frozen != True:
        if key==GLUT_KEY_UP:
            speed *= 2
            #print("Speed Increased")
        if key== GLUT_KEY_DOWN:		#// up arrow key
            speed /= 2
            #print("Speed Decreased")
    glutPostRedisplay()


balls = []
ballsclr= []
result= False

def mouseListener(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
    global bx, by, final, result, balls, ballsclr, frozen
    if frozen != True:
        if button==GLUT_LEFT_BUTTON:
            if(state == GLUT_DOWN):    # 		// 2 times?? in ONE click? -- solution is checking DOWN or UP
                for i in balls:
                    i[2] = [0,0,0]
            if (state == GLUT_UP):
                for i in range(len(balls)):
                    balls[i][2] = ballsclr[i]
        if button==GLUT_RIGHT_BUTTON:
            if state == GLUT_DOWN:
                result = True	
                bx, by = convert_coordinate(x,y)
                if bx >= 0 and bx <= 180 and by >= 0 and by <= 180:
                    ballcolor = [random.random(), random.random(), random.random()]
                    ballsclr += [ballcolor]
                    direction = [random.choice('+-'), random.choice('+-')]
                    balls += [[bx, by, ballcolor, direction]]
                
    # case GLUT_MIDDLE_BUTTON:
    #     //........

    glutPostRedisplay()

frozen = False
def keyboardListener(key, x, y):

    global size_of_ball, frozen
    #if frozen != True:

    if key==b' ':
        if frozen == True:
            frozen = False
        else:
            frozen = True
 

    glutPostRedisplay()

def display():
  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	#//color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  
    glMatrixMode(GL_MODELVIEW)
   
    glLoadIdentity()
 
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)


    global bx, by, size_of_ball, balls
    for i in balls:
        glColor3f(i[2][0], i[2][1], i[2][2])
        draw_points(i[0], i[1], size_of_ball)
        


    glLineWidth(4)
    glColor3f(0.71, 0.49, 0.86)
    glBegin(GL_LINES)
    
    glVertex2d(200,0)
    glVertex2d(200,200)

    glVertex2d(200,200)
    glVertex2d(0,200)

    glVertex2d(0,200)
    glVertex2d(0,0)

    glVertex2d(0,0)
    glVertex2d(200,0)

    glEnd()

    if(final):
        m,n = final
        glBegin(GL_POINTS)
        glColor3f(0.7, 0.8, 0.6)
        glVertex2f(m,n)
        glEnd()
    glutSwapBuffers()

sign=['+','-']
def animate():
    #//codes for any changes in Models, Camera
    glutPostRedisplay()
    global balls, speed
    for i in range(len(balls)):
        
        if balls[i][0] >= 200 and balls[i][1] < 200:
            balls[i][3][0] = '-'
        if balls[i][0] > 0 and balls[i][1] <= 0:
            balls[i][3][1] = '+'
        if balls[i][0] < 200 and balls[i][1] >= 200:
            balls[i][3][1] = '-'
        if balls[i][0] <= 0 and balls[i][1] > 0:
            balls[i][3][0] = '+'
        if balls[i][0] <= 0 and balls[i][1] <= 0:
            balls[i][3][0] = '+'
            balls[i][3][1] = '+'
        if balls[i][0] >= 200 and balls[i][1] >= 200:
            balls[i][3][0] = '-'
            balls[i][3][1] = '-'
       
        if balls[i][0] >= 200 and balls[i][1] <= 0:
            balls[i][3][0] = '-'
            balls[i][3][1] = '+'
        if balls[i][0] <= 0 and balls[i][1] >= 200:
            balls[i][3][0] = '+'
            balls[i][3][1] = '-'
        
        if frozen != True:
            if balls[i][3][0] == '+':
                balls[i][0] += speed
            else: 
                balls[i][0] -= speed
            if balls[i][3][1] == '+':
                balls[i][1] += speed
            else:
                balls[i][1] -= speed


    



def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(104,	1,	1,	1000.0)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"OpenGL Coding Practice")
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()		#The main loop of OpenGL
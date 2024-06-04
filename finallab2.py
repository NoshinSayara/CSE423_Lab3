from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

W_Width, W_Height = 400,500
speed=1
def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

def draw_points(x, y,s):
    glPointSize(s) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def MidPointLineAlgo(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    d  = 2*dy - dx
    incE  = 2*dy
    incNE = 2*dy - 2*dx
    x = x1
    y = y1
    for i in range(x, x2+1):
        points += [[i, y]]
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
    return points

def ZoneFinder(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx>0 and dy>=0:
        if abs(dx) > abs(dy):
            return 0
        else:
            return 1
    elif dx<=0 and dy>=0:
        if abs(dx) > abs(dy):
            return 3
        else:
            return 2
    elif dx<0 and dy<0:
        if abs(dx) > abs(dy):
            return 4
        else:
            return 5
    elif dx>=0 and dy<0:
        if abs(dx) > abs(dy):
            return 7
        else:
            return 6
        
def convertToZoneZero(zone, x1, y1, x2, y2):
    if zone == 1:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    elif zone == 2:
        x1, y1 = y1, -x1
        x2, y2 = y2, -x2
    elif zone == 3:
        x1, y1 = -x1, y1
        x2, y2 = -x2, y2
    elif zone == 4:
        x1, y1 = -x1, -y1
        x2, y2 = -x2, -y2
    elif zone == 5:
        x1, y1 = -y1, -x1
        x2, y2 = -y2, -x2
    elif zone == 6:
        x1, y1 = -y1, x1
        x2, y2 = -y2, x2
    elif zone == 7:
        x1, y1 = x1, -y1
        x2, y2 = x2, -y2
    return x1, y1, x2, y2


def convertToZoneM(color, zone, points):
    s = 2
    glColor3f(color[0], color[1], color[2])
    if zone ==0:
        for x, y in points:
            draw_points(x, y, s)
    elif zone == 1:
        for x, y in points:
            draw_points(y, x, s)
    elif zone == 2:
        for x, y in points:
            draw_points(-y, x, s)
    elif zone == 3:
        for x, y in points:
            draw_points(-x, y, s)
    elif zone == 4:
        for x, y in points:
            draw_points(-x, -y, s)
    elif zone == 5:
        for x, y in points:
            draw_points(-y, -x, s)
    elif zone == 6:
        for x, y in points:
            draw_points(y, -x, s)
    elif zone == 7:
        for x, y in points:
            draw_points(x, -y, s)

def drawLines(color, x1, y1, x2, y2):
    zone = ZoneFinder(x1, y1, x2, y2)
    x1, y1, x2, y2 = convertToZoneZero(zone, x1, y1, x2, y2)
    points = MidPointLineAlgo(x1, y1, x2, y2)
    convertToZoneM(color, zone, points)

import random 
ran_x1 = 50
y_start = 210
cat_p1 = [-70, -235, 70, -235]
cat_p2 = [-50, -250, 50, -250]
cat_p3 = [-50, -250, -70, -235]
cat_p4 = [ 50, -250, 70, -235]
pause = False
cat_color = [1, 1, 1]

d_color = [random.random(), random.random(), random.random()]
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    #======================================================================================
    #Drawing the catcher
    global cat_p1, cat_p2, cat_p3, cat_p4, cat_color, d_color
    drawLines(cat_color, cat_p1[0], cat_p1[1], cat_p1[2], cat_p1[3])
    drawLines(cat_color, cat_p2[0], cat_p2[1], cat_p2[2], cat_p2[3])
    drawLines(cat_color, cat_p3[0], cat_p3[1], cat_p3[2], cat_p3[3])
    drawLines(cat_color, cat_p4[0], cat_p4[1], cat_p4[2], cat_p4[3])
    
    #pause
    color = [1, 0.984, 0]
    if pause == False:
        drawLines(color, 5, 210, 5, 240)
        drawLines(color, -5, 210, -5, 240)
    else:
        drawLines(color, -15, 210, -15, 240)
        drawLines(color, -15, 240, 20, 225)
        drawLines(color, -15, 210, 20, 225)

    #exit
    color = [1,0,0]
    drawLines(color, 240, 240, 210, 210)
    drawLines(color, 240, 210, 210, 240)

    #restart
    color = [0,0,1]
    drawLines(color, -200, 225, -240, 225)
    drawLines(color, -218, 240, -240, 225)
    drawLines(color, -218, 210, -240, 225)
    #diamond
    color = [0,0,0]
    a = 20
    b = 26
    global ran_x1, y_start
    drawLines(color, ran_x1, y_start, ran_x1+a, y_start)
    drawLines(color, ran_x1, y_start-b, ran_x1+a, y_start-b)
    drawLines(color, ran_x1, y_start-b, ran_x1, y_start)
    drawLines(color, ran_x1+a, y_start-b, ran_x1+a, y_start)

    d_p1 = [int((ran_x1+ran_x1+a)/2), y_start]
    d_p2 = [ran_x1+a, int((y_start+y_start-b)/2)]
    d_p3 = [d_p1[0], y_start-b]
    d_p4 = [ran_x1, d_p2[1]]
    color = [0.941, 0.922, 0.541]
    drawLines(d_color, d_p1[0], d_p1[1], d_p2[0], d_p2[1])
    drawLines(d_color, d_p2[0], d_p2[1], d_p3[0], d_p3[1])
    drawLines(d_color, d_p3[0], d_p3[1], d_p4[0], d_p4[1])
    drawLines(d_color, d_p4[0], d_p4[1], d_p1[0], d_p1[1])
    glutSwapBuffers()

def specialKeyListener(key, x, y):
    global cat_p1, cat_p2, cat_p3, cat_p4

    s = 20
    if key==GLUT_KEY_LEFT:
        if cat_p1[0] <= -250:
            pass
        else:
            if pause == False:
                cat_p1[0]-=s
                cat_p1[2]-=s
                cat_p2[0]-=s
                cat_p2[2]-=s
                cat_p3[0]-=s
                cat_p3[2]-=s
                cat_p4[0]-=s
                cat_p4[2]-=s

    if key== GLUT_KEY_RIGHT:
        if cat_p1[2] >= 250:
            pass
        else:
            if pause == False:
                cat_p1[0]+=s
                cat_p1[2]+=s
                cat_p2[0]+=s
                cat_p2[2]+=s
                cat_p3[0]+=s
                cat_p3[2]+=s
                cat_p4[0]+=s
                cat_p4[2]+=s
    #print(cat_p1)
    glutPostRedisplay()

def mouseListener(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
    global bx, by, create_new, y_start, point, pause, cat_color
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):    # 		// 2 times?? in ONE click? -- solution is checking DOWN or UP
            #print(x,y)
            #exit
            if x >= 360 and x <= 390 and y >= 15 and y <= 45:
                glutLeaveMainLoop()
            #pause
            elif x >= 170 and x <= 220 and y >= 10 and y <= 45:
                if pause == False:
                    pause = True
                else:
                    pause = False
            #restart
            elif x >= 6 and x <= 50 and y >= 10 and y <= 45:
                y_start = 210
                #print('Starting Over!')
                point = 0
                pause = False
                cat_color = [1,1,1]
                
                

    #if button==GLUT_RIGHT_BUTTON:
        #if state == GLUT_DOWN: 	
            #create_new = convert_coordinate(x,y)
    # case GLUT_MIDDLE_BUTTON:
    #     //........
    glutPostRedisplay()



def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    
'''
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here
    draw_points(250, 250)
    MidPointLineAlgo(20,20,300,300)
    glutSwapBuffers()
   
'''

point = 0
def animate():
    #//codes for any changes in Models, Camera
    glutPostRedisplay()
    global ran_x1, y_start, cat_p1, point, pause, cat_color, d_color
    if y_start == -214:
        if cat_p1[0] < ran_x1+20 and cat_p1[2] > ran_x1:
            y_start = 210
            ran_x1 = random.randint(-250,230)
            point += 1
            d_color = [random.random(), random.random(), random.random()]
            print(f'Score: {point}')
            
        else:
            cat_color = [1,0,0]
            print(f'Game Over! Score: {point}')
    if pause == True:
        y_start=y_start
    else:
        y_start=(y_start-speed)
    #print(ran_x1, y_start)
    




def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)
    

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(500, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color
# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"Catch The Diamond")
init()
glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)
#glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()		#The main loop of OpenGL



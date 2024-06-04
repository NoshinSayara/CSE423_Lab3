from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

W_Width, W_Height = 400, 500
speed = 0.5
circle_radius = 10
shooter_radius = 15
score = 0
pause = False
shooter_x = 0
shooter_y = -200
shooter_color = [1, 1, 0]
circle_colors = [[1, 1, 0] for _ in range(5)]
circle_positions = [[random.randint(-200, 200), random.randint(0, 200)] for _ in range(5)]
circle_status = [True] * 5
bullets = []
bullet_radius = 5
bullet_speed = 2

def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a, b

def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
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
    if dx > 0 and dy >= 0:
        if abs(dx) > abs(dy):
            return 0
        else:
            return 1
    elif dx <= 0 and dy >= 0:
        if abs(dx) > abs(dy):
            return 3
        else:
            return 2
    elif dx < 0 and dy < 0:
        if abs(dx) > abs(dy):
            return 4
        else:
            return 5
    elif dx >= 0 and dy < 0:
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
    if zone == 0:
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


def MidPointCircleAlgo(xc, yc, r):
    points = []
    x = 0
    y = r
    d = 1 - r
    MidPointCirclePlotPoints(xc, yc, x, y, points)
    while y > x:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        MidPointCirclePlotPoints(xc, yc, x, y, points)
    return points

def MidPointCirclePlotPoints(xc, yc, x, y, points):
    points.append([xc + x, yc + y])
    points.append([xc - x, yc + y])
    points.append([xc + x, yc - y])
    points.append([xc - x, yc - y])
    points.append([xc + y, yc + x])
    points.append([xc - y, yc + x])
    points.append([xc + y, yc - x])
    points.append([xc - y, yc - x])

def drawCircle(color, xc, yc, r):
    points = MidPointCircleAlgo(xc, yc, r)
    glColor3f(color[0], color[1], color[2])
    for x, y in points:
        draw_points(x, y, 2)

def drawShooter(color, xc, yc, r):
    drawCircle(color, xc, yc, r)

def drawBullet(color, xc, yc, r):
    drawCircle(color, xc, yc, r)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    global circle_positions, circle_radius, shooter_x, shooter_y, shooter_radius, shooter_color, score, pause

    # Drawing shooter circle
    drawShooter(shooter_color, shooter_x, shooter_y, shooter_radius)

    # Drawing mini circles
    for i in range(len(circle_positions)):
        if circle_status[i]:
            drawCircle(circle_colors[i], circle_positions[i][0], circle_positions[i][1], circle_radius)

    # Drawing bullets
    for bullet in bullets:
        drawBullet([1, 1, 0], bullet[0], bullet[1], bullet_radius)



    # Drawing exit button
    color = [1, 0, 0]
    drawLines(color, 240, 240, 210, 210)
    drawLines(color, 240, 210, 210, 240)
    #Drawing pause button
    if pause==False:
        color=[1,1,0]
        drawLines(color, 5, 210, 5, 240)
        drawLines(color, -5, 210, -5, 240)
    else:
        color=[0,1,0]
        drawLines(color, -15, 210, -15, 240)
        drawLines(color, -15, 240, 20, 225)
        drawLines(color, -15, 210, 20, 225)

    # Drawing restart button
    color = [0, 0, 1]
    drawLines(color, -200, 225, -240, 225)
    drawLines(color, -218, 240, -240, 225)
    drawLines(color, -218, 210, -240, 225)

    glutSwapBuffers()


def mouseListener(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
    global pause, score, shooter_color
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):    # 		// 2 times?? in ONE click? -- solution is checking DOWN or UP
            #print(x,y)
            #exit
            if x >= 360 and x <= 390 and y >= 15 and y <= 45:
                print('GoodBye')
                glutLeaveMainLoop()
            #pause
            elif x >= 170 and x <= 220 and y >= 10 and y <= 45:
                if pause == False:
                    pause = True
                else:
                    pause = False
            #restart
            elif x >= 6 and x <= 50 and y >= 10 and y <= 45:
                
            # Reset all game variables to their initial values
                score = 0
                pause = False
                shooter_color = [1, 1, 0]
                resetGame()
                print('Starting over')

def resetGame():
    global bullets, circle_positions, circle_status
    bullets = []
    circle_positions = [[random.randint(-200, 200), random.randint(0, 200)] for _ in range(5)]
    circle_status = [True] * 5

def keyboardListener(key, x, y):
    global shooter_x, shooter_y, pause

    if key == b'a':
        if shooter_x - shooter_radius >= -200 and not pause:
            shooter_x -= 10
    elif key == b'd':
        if shooter_x + shooter_radius <= 200 and not pause:
            shooter_x += 10

    elif key == b' ':  # Space bar
        if not pause:
            shoot()

    glutPostRedisplay()


def checkCollision(circle_x, circle_y):
    global shooter_x, shooter_y, shooter_radius, score, circle_status, pause

    distance = math.sqrt((circle_x - shooter_x) ** 2 + (circle_y - shooter_y) ** 2)
    if distance <= shooter_radius + circle_radius:
        pause = True  # Pause the game
        print("Game Over. Your score:", score)
        return True
    return False

def checkBulletCollision(circle_x, circle_y):
    global bullets, score, circle_status

    for bullet in bullets:
        distance = math.sqrt((circle_x - bullet[0]) ** 2 + (circle_y - bullet[1]) ** 2)
        if distance <= bullet_radius + circle_radius:
            bullets.remove(bullet)
            score += 1
            circle_status[circle_positions.index([circle_x, circle_y])] = False  #  circle ke hit korle
            print("Score:", score)  # Print the updated score
            return True
    return False


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
missed_circles = 0
def animate():
    glutPostRedisplay()
    global circle_positions, circle_status, pause, bullets, missed_circles

    if not pause:
        # Update position of circles
        for i in range(len(circle_positions)):
            if circle_positions[i][1] > -250 and circle_status[i]:
                circle_positions[i][1] -= speed
            else:
                if circle_status[i]:
                    missed_circles += 1
                circle_positions[i] = [random.randint(-200, 200), 200]
                circle_status[i] = True

        # Check if missed circles exceed the threshold
        if missed_circles >= 3:
            pause = True
            print("Game Over. Your score:", score)

        # Check for collision with shooter circle
        for i in range(len(circle_positions)):
            if circle_status[i]:
                if checkCollision(circle_positions[i][0], circle_positions[i][1]):
                    circle_status[i] = False
                    missed_circles = 0  # Reset missed circles counter

        # Move bullets
        for bullet in bullets:
            if bullet[1] < W_Height:
                bullet[1] += bullet_speed
            else:
                bullets.remove(bullet)

        # Check for collision with bullets
        for i in range(len(circle_positions)):
            if circle_status[i]:
                if checkBulletCollision(circle_positions[i][0], circle_positions[i][1]):
                    circle_status[i] = False
                    missed_circles = 0  # Reset missed circles counter



def shoot(): #eta hocche bullet er jonne
    global shooter_x, shooter_y, bullets
    bullets.append([shooter_x, shooter_y])


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(500, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) # Depth, Double buffer, RGB color
wind = glutCreateWindow(b"Shoot the Circles")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
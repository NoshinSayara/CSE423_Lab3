from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random  # Add this line to import the random module

# Declare raindrops as a global variable
raindrops = []
background_color = [1.0, 1.0, 1.0]  # Initial background color (white)

def init():
    glClearColor(*background_color, 0.0)  # Set initial background color
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0.0, 500.0, 0.0, 500.0)

def draw_shapes():
    global raindrops, background_color  # Declare raindrops as a global variable
    glClear(GL_COLOR_BUFFER_BIT)  # Clear display window

    # Set color to black
    glColor3f(0.0, 0.0, 0.0)
    # Adjust the point size
    glPointSize(5.0)

    # Set color to black
    glColor3f(0.0, 0.0, 0.0)

    # Draw an outlined triangle with wider lines
    glLineWidth(6.0)  # Set the line width to 6.0
    glBegin(GL_LINES)
    glVertex2i(100, 200)
    glVertex2i(100, 0)

    glVertex2i(100, 0)
    glVertex2i(300, 0)

    glVertex2i(300, 0)
    glVertex2i(300, 200)

    glVertex2i(300, 200)
    glVertex2i(100, 200)
    glEnd()

    # Change color to black and draw the rectangle
    glBegin(GL_LINES)
    glVertex2i(200, 300)
    glVertex2i(100, 200)

    glVertex2i(300, 200)
    glVertex2i(200, 300)
    glEnd()

    # Set the line width back to the default value (1.0)
    glLineWidth(1.0)

    # Draw a door
    glColor3f(0.0, 0.0, 0.0)  # Set color to black for the door
    glBegin(GL_LINES)
    glVertex2i(180, 0)
    glVertex2i(180, 120)

    glVertex2i(130, 0)
    glVertex2i(130, 120)

    glVertex2i(180, 120)
    glVertex2i(130, 120)
    glEnd()

    # Draw a square door 2
    glBegin(GL_LINES)
    glVertex2i(230, 50)
    glVertex2i(230, 120)

    glVertex2i(270, 50)
    glVertex2i(270, 120)

    glVertex2i(230, 120)
    glVertex2i(270, 120)

    glVertex2i(230, 50)
    glVertex2i(270, 50)

    glVertex2i(250,50)
    glVertex2i(250,120)

    glVertex2i(230,80)
    glVertex2i(270,80)
    glEnd()

    # Draw raindrops using random positions
    for drop in raindrops:
        glBegin(GL_LINES)
        glVertex2i(drop[0], drop[1])
        glVertex2i(drop[0], drop[1] - 5)  # Adjust the length of raindrops as needed
        glEnd()

    glFlush()  # Process all OpenGL routines
def specialKeyListener(key, x, y):
    global raindrops

    
    if key == GLUT_KEY_RIGHT:
        for drop in raindrops:
            drop[0] += 2
    elif key == GLUT_KEY_LEFT:
        for drop in raindrops:
            drop[0] -= 2
        

        
    glutPostRedisplay()
def keyboard_callback(key, x, y):
    global raindrops, background_color
    if key == b'\x1b':  # ESC key to exit
        sys.exit()
    elif key == b'r' or key == b'R':  # Change rain direction
        for drop in raindrops:
            drop[0] += random.randint(-5, 5)
            #drop[1] += random.randint(-5, 5)
    elif key == b'd' or key == b'D':  # Day mode, change background to light blue
        background_color = [0.7, 0.9, 1.0]
    elif key == b'n' or key == b'N':  # Night mode, change background to dark blue
        background_color = [0.0, 0.0, 0.2]
    
    elif key == b'z' or key == b'Z':  # Day mode, change background to white
        background_color = [1.0, 1.0, 1.0]

    glClearColor(*background_color, 0.0)  # Set background color
    glutPostRedisplay()  # Request a redraw

def main():
    global raindrops, background_color  # Declare raindrops as a global variable
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowPosition(50, 100)
    glutInitWindowSize(400, 400)
    glutCreateWindow(b"An Example OpenGL Program")

    init()

    # Initialize random raindrop positions
    for i in range(50):
        raindrops.append([random.randint(50, 400), random.randint(50, 400)])

    glutDisplayFunc(draw_shapes)
    glutIdleFunc(draw_shapes)  # Add idle function for animation
    glutKeyboardFunc(keyboard_callback)  # Set keyboard callback function
    glutSpecialFunc(specialKeyListener)
    glutMainLoop()

if __name__ == "__main__":
    main()
#glutMainLoop()	
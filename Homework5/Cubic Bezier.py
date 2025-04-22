import pygame
from sys import exit

width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Cubic Bezier Drawing")

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def drawPoint(pt, color=GREEN, thick=3):
    pygame.draw.circle(screen, color, pt, thick)

def drawPolylines(pts, color=GREEN, thick=3):
    if len(pts) < 2:
        return
    for i in range(len(pts) - 1):
        pygame.draw.line(screen, color, pts[i], pts[i+1], thick)

def cubic_bezier(t, p0, p1, p2, p3):
    p0 = tuple(p0)
    p1 = tuple(p1)
    p2 = tuple(p2)
    p3 = tuple(p3)
    x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
    y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
    return (int(round(x)), int(round(y)))

def drawCubicBezier(pts, color=RED, thick=2, steps=100):
    if len(pts) < 4:
        return
    prev = cubic_bezier(0, pts[0], pts[1], pts[2], pts[3])
    for i in range(1, steps+1):
        t = i / steps
        curr = cubic_bezier(t, pts[0], pts[1], pts[2], pts[3])
        pygame.draw.line(screen, color, prev, curr, thick)
        prev = curr

clock = pygame.time.Clock()
pts = []
drawing_done = False
margin = 6
pressed = 0
old_pressed = 0
old_button1 = 0

while True:
    time_passed = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()
        else:
            pressed = 0

    button1, _, _ = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = (x, y)

    # 점 추가 및 상태 관리
    if not drawing_done:
        if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
            if len(pts) < 4:
                pts.append(pt)
            if len(pts) == 4:
                drawing_done = True
    else:
        # 곡선이 그려진 후 클릭하면 초기화
        if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
            pts = []
            drawing_done = False
            screen.fill(WHITE)

    # 화면 그리기
    screen.fill(WHITE)
    for p in pts:
        drawPoint(p, GREEN, 4)
    drawPolylines(pts, GREEN, 1)
    if len(pts) == 4:
        drawCubicBezier(pts, RED, 2, 100)

    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed
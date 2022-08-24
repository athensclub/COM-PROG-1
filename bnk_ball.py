# Lab_BNK48 
import pygame as pg
import math
DENSITY = 1

hitting = []

def is_hitting(i, j):
    global hitting
    for h in hitting:
        if (h[0] == i and h[1] == j) or (h[0] == j or h[1] == i):
            return True
    return False

def pop(i, j):
    global hitting
    index = -1
    for i in range(len(hitting)):
        h = hitting[i]
        if (h[0] == i and h[1] == j) or (h[0] == j or h[1] == i):
            index = i
    hitting.pop(index)

def get_mass(r):
    return math.pi * r * r * DENSITY

def get_radius(rect):
    return (rect.right - rect.left) / 2
    
def get_center(rect):
    return (rect.left + rect.right) / 2, (rect.top + rect.bottom) / 2

def solve_binomial(m1, u1, m2, u2):
    A = 2*m1
    B = -2*(m1*m1*u1 + m1*m2*u2)
    C = -(m1*u1*u1 + m2*u2*u2 - (m1*u1+m2*u2)*(m1*u1+m2*u2))
    v1 = (-B+math.sqrt(B*B-4*A*C))/2*A
    v2 = (m1*u1+m2*u2-m1*v1)/m2
    return v1, v2

def intersect(rect1, rect2):
    x1, y1 = get_center(rect1)
    r1 = get_radius(rect1)
    x2, y2 = get_center(rect2)
    r2 = get_radius(rect2)
    
    dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return dist < r1 + r2

def get_new_speed(rect1, rect2, speed1, speed2):
    r1 = get_radius(rect1)
    r2 = get_radius(rect2)
    
    if not intersect(rect1, rect2):
        return False, speed1, speed2

    m1 = get_mass(r1)
    m2 = get_mass(r2)
    
    vx1, vx2 = solve_binomial(m1, speed1[0], m2, speed2[0])
    vy1, vy2 = solve_binomial(m1, speed1[1], m2, speed2[1])
    return True, [vx1, vy1], [vx2, vy2]

width = 1000
height = 600
FPS = 60

pink = (197,142,195)
white = (255,255,255)

pg.init()
clock = pg.time.Clock()
running = True

screen = pg.display.set_mode((width,height))

pg.mixer.init()
pg.mixer.music.load("source/sound.mp3")
pg.mixer.music.play(-1, 0.0)

soundeffect = pg.mixer.Sound("source/effect.wav")

ball_info = [["source/BNK48/Wee_cc.png", (150,150), (500,250)], \
             ["source/BNK48/Wee_cc.png", (100,100), (250,120)], \
             ["source/BNK48/Wee_cc.png", (120,120), (800,400)] \
            ]
n = len(ball_info)
ball_speed = [[2,2], [-3,4], [3,-2]]
ball_img = []
ball_rect = []
for i in range(n):
    ball_img.append(pg.transform.scale(pg.image.load(ball_info[i][0]).convert_alpha(), ball_info[i][1]))
    ball_rect.append(ball_img[i].get_rect(center=ball_info[i][2]))

while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running=False
            pg.quit()

    if running:
        screen.fill(pink)

        for i in range(n):
            ball_rect[i] = ball_rect[i].move(ball_speed[i])
        
        # TODO 11 : วาด text คำว่า "Heavy Collision" [size : 150 , center :(width/2 , height/3), สีขาว]
        font_name = pg.font.match_font('arial')  # กำหนดชื่อ Font
        font = pg.font.Font(font_name, 100)  # กำหนดขนาด font
        text_surface = font.render("Heavy Collision", True, white)
        text_rect = text_surface.get_rect() # แปลง Surface เป็น object
        text_rect.midtop = (width/2, height/3) # ระบุตำแหน่งของ text
        screen.blit(text_surface, text_rect)
        
        # TODO 12 : วาด text รหัสนิสิต ลงไป ข้างใต้คำว่า "Heavy Collision" [size : 100 ,center :(width/2 , height/1.5), สีขาว]
        # [ขนาดและตำแหน่งสามารถปรับได้ตามความเหมาะสม]
        font = pg.font.Font(font_name, 50)
        text_surface = font.render("6532011921 6532026321", True, white)
        text_rect = text_surface.get_rect() # แปลง Surface เป็น object
        text_rect.midtop = (width/2, height/1.5) # ระบุตำแหน่งของ text
        screen.blit(text_surface, text_rect)

        # TODO 13 : เขียนเงื่อนไขไม่ให้ตกกรอบทุกด้านให้กับ member ทั้ง 3 คน
        for i in range(n):
            if ball_rect[i].left < 0 or ball_rect[i].right > width:
                ball_speed[i][0] = -ball_speed[i][0]
            if ball_rect[i].top < 0 or ball_rect[i].bottom > height:
                ball_speed[i][1] = -ball_speed[i][1]

        # Special point ทำให้ลูกบอลชนกันแล้วเด้งในทิศตรงกันข้าม
        for i in range(n):
            for j in range(i+1, n):
                if intersect(ball_rect[i], ball_rect[j]):
                    soundeffect.play()
                    ball_speed[i][0] = -ball_speed[i][0]
                    ball_speed[i][1] = -ball_speed[i][1]
                    ball_speed[j][0] = -ball_speed[j][0]
                    ball_speed[j][1] = -ball_speed[j][1]
                    
                # if is_hitting(i, j):
                #     if not intersect(ball_rect[i], ball_rect[j]):
                #         pop(i, j)
                #     continue

                # hit, speed1, speed2 = get_new_speed(ball_rect[i], ball_rect[j], ball_speed[i], ball_speed[j])
                # if hit:
                #     hitting.append([i, j])
                # ball_speed[i] = speed1
                # ball_speed[j] = speed2

        ################################################
        for i in range(n):
            screen.blit(ball_img[i], ball_rect[i])

        ##########################################################

        pg.display.flip()

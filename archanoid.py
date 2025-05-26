import pygame
import time
pygame.init()
window = pygame.display.set_mode((500,500))
window.fill((0,250,154))
clock = pygame.time.Clock()
game_over=False

class Area:
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = (0,250,154)
        if color:
            self.fill_color = color
    def color(self, new_color):
        self.fill_color = new_color
    def fill(self):
        pygame.draw.rect(window,self.fill_color,self.rect)
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)
    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (width, height))
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Label(Area):
    def set_text(self, text, fsize = 12, text_color=(0,0,0)):
        self.text = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.text, (self.rect.x+shift_x, self.rect.y+shift_y))

start_x = 5
start_y = 5
count = 9
monsters = []
for j in range(3):
    y = start_y + (55 * j)
    x = start_x + (27.5 * j)
    for i in range(count):
        monster = Picture('D:\download\images_16_-removebg-preview.png', x, y, 50, 50)
        monsters.append(monster)
        x = x + 55
    count = count - 1

ball = Picture("D:\download\image_1_-removebg-preview.png", 160, 200, 50, 50)
platform = Picture('D:\download\image-removebg-preview.png', 200, 330, 100, 30)
move_right = False
move_left = False

speed_x = 3
speed_y = 3

while not game_over:
    ball.fill()
    platform.fill()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False  

    if move_right:
        platform.rect.x += 3
    if move_left:
        platform.rect.x -= 3

    ball.rect.x += speed_x
    ball.rect.y += speed_y

    if ball.rect.y < 0:
        speed_y *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        speed_x *= -1
    if ball.rect.colliderect(platform.rect):
        speed_y *= -1

    if ball.rect.y > 350:
        speed_x = 0
        speed_y = 0
        over = Label(135, 175, 50, 50, (0,250,154))
        over.set_text('Гру закінчено', 30)
        over.draw(10, 10)
    if len(monsters) == 0:
        speed_x = 0
        speed_y = 0
        win = Label(135, 175, 50, 50, (0,250,154))
        win.set_text('Ви виграли', 30)
        win.draw(10, 10)

    for monster in monsters:
        monster.draw()
        if monster.rect.colliderect(ball.rect):
            monsters.remove(monster)
            monster.fill()
            speed_y *= -1

    platform.draw()
    ball.draw()

    pygame.display.update()

    clock.tick(40)

from pygame import *
from random import choice, randint

window = display.set_mode((700, 500))
display.set_caption('Змейка')

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Snake(GameSprite):
    def __init__(self, img, x, y, w, h, t):
        super().__init__(img, x, y, w, h)
        # 0 - голова, 1 - тело, 2 - хвост
        self.type = t
        self.speed = 25
        self.direction = "0"
        self.cur_image = self.image
        self.wait = 1

    def update(self):
        if self.direction == 'l':
            self.rect.x -= self.speed
        elif self.direction == 'r':
            self.rect.x += self.speed
        elif self.direction == 'u':
            self.rect.y -= self.speed
        elif self.direction == 'd':
            self.rect.y += self.speed    

        keys = key.get_pressed()
        if keys[K_LEFT] and self.direction!='r':
            self.direction = 'l'
            self.image = transform.rotate(self.cur_image, -90)
        elif keys[K_RIGHT] and self.direction!='l':
            self.direction = 'r'
            self.image = transform.rotate(self.cur_image, 90)
        elif keys[K_UP] and self.direction!='d':
            self.direction = 'u'
            self.image = transform.rotate(self.cur_image, 180)
        elif keys[K_DOWN] and self.direction!='u':
            self.direction = 'd'
            self.image = transform.rotate(self.cur_image, 0)

    def set_direct(self):
        if self.direction == 'l':
            self.image = transform.rotate(self.cur_image, -90)
        elif self.direction == 'r':
            self.image = transform.rotate(self.cur_image, 90)
        elif self.direction == 'u':
            self.image = transform.rotate(self.cur_image, 180)
        elif self.direction == 'd':
            self.image = transform.rotate(self.cur_image, 0)

    def eat(self, food):
        global speed
        speed +=1
        food.position()



class Food(GameSprite):
    def __init__(self, imgs, x,y, w,h):
        super().__init__(imgs[0], x,y, w,h)
        self.costumes = []
        self.costumes.append(self.image)
        for i in range(len(imgs)-1):
            self.image = transform.scale(image.load(imgs[i+1]),(w,h))
            self.costumes.append(self.image)

    def set_costume(self, n):
        self.image = self.costumes[n]

    def rand_costume(self):
        self.image = choice(self.costumes)

    def position(self):
        self.rect.x = randint(0, 700-self.rect.width)
        self.rect.y = randint(0, 500-self.rect.height)
        self.rand_costume()




head = Snake('1.png', 350, 250, 25,25, 0)
tail = Snake('3.png', 335, 225, 25,25, 0)
snake = [head,tail]
food = Food(['4.png', '5.png', '6.png', '7.png'],
             -100, -100, 25, 25)
food.position()

game = True
clock = time.Clock()
fps = 10
speed = 1

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill((180,200,180))
    head.update()
    head.reset()
    food.reset()
    if head.rect.colliderect(food):
        head.eat(food)
    for e in range(1, len(snake)):
        snake[e].reset()
        snake[e].direction = snake[e-1].direction
        snake[e].rect.x = snake[e-1].rect.x
        snake[e].rect.y = snake[e-1].rect.y
        snake[e].set_direct()

    clock.tick(fps)
    display.update()

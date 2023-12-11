import pygame
from sys import exit
from pygame import mixer


# layout set up
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('cow')
clock = pygame.time.Clock()
grass_surface = pygame.image.load('src/grass.jpg')
milk_surface = pygame.image.load('src/milk.png')

# text set up
pygame.font.init() 
my_font = pygame.font.SysFont('rockwell', 30)
text_surface = my_font.render('COW IS HUNGRY! FEED THE COW!', False, (0, 0, 0))

# sound set up
mixer.init()
mixer.music.load("src/muu.mp3")
mixer.music.set_volume(0.7)


class Cow:
    def __init__(self) -> None:
        self.x = 0
        self.y = 200
        self.hungry = True
        self.milk_availability = False
        self._draw()
    
    def _draw(self, state='src/cow.png'):
        screen.blit(grass_surface, (0,0))
        screen.blit(pygame.image.load(state), (self.x, self.y))

    def move_forward(self):
        self.x = self.x - 15
        print('moving forward...')
        self._draw()

    def move_backward(self):
        self.x = self.x + 15
        print('moving backward...')
        self._draw()

    def eat(self):
        self.hungry = False
        self.milk_availability = True
        self._draw(state='src/cow_eat.png')

    def speak(self):
        mixer.music.play()
    
    def milk(self):
        if not self.hungry:
            screen.blit(milk_surface, (self.x + 150, 300))
            self.milk_availability = False
            self.hungry = True
        else:
            screen.blit(text_surface, (20, 20))



my_cow = Cow()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                my_cow.move_forward()
            if event.key == pygame.K_RIGHT:
                my_cow.move_backward()
            if event.key == pygame.K_DOWN:
                my_cow.eat()
            if event.key == pygame.K_UP:
                my_cow.speak()
            if event.key == pygame.K_m:
                my_cow.milk()

                



    pygame.display.update()
    clock.tick(60)
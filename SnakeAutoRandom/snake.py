import pygame
import random
import numpy as np 
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('Snake\SnakeAutoRandom\Arialn.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4



Point = namedtuple('Point', 'x, y')
BLOCK_SIZE = 20

class SnakeGame:
    def __init__(self, width=200, height=200, fps=20):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('SnakeV1')
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.head = Point(self.width/2, (self.height/2)+BLOCK_SIZE)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y), Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.food = None
        self.score = 0
        self.numberSetps = 0
        self._place_food()

        self.direction = Direction.RIGHT

    def _place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
    
    def _update_ui(self):
        self.screen.fill((0, 0, 0))


        snake_size = len(self.snake)
        i=0
        for pt in self.snake:
            pygame.draw.rect(self.screen, (50,0+np.ceil((i*255)/snake_size),255-np.ceil((i*255)/snake_size)), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            i+=1

        if(self.direction == Direction.RIGHT):
            pygame.draw.rect(self.screen, (255, 255,0), pygame.Rect(self.snake[0].x+15, self.snake[0].y+5, 3, 3))
            pygame.draw.rect(self.screen, (255, 255,0), pygame.Rect(self.snake[0].x+15, self.snake[0].y+15, 3, 3))
        if self.direction == Direction.LEFT:
            pygame.draw.rect(self.screen, (255, 255,0), pygame.Rect(self.snake[0].x+5, self.snake[0].y+5, 3, 3))
            pygame.draw.rect(self.screen, (255, 255,0), pygame.Rect(self.snake[0].x+5, self.snake[0].y+15, 3, 3))
        if self.direction == Direction.UP:
            pygame.draw.rect(self.screen, (255, 255,0), pygame.Rect(self.snake[0].x+5, self.snake[0].y+5, 3, 3))
            pygame.draw.rect(self.screen, (255, 255,0), pygame.Rect(self.snake[0].x+15, self.snake[0].y+5, 3, 3))
        if self.direction == Direction.DOWN:
            pygame.draw.rect(self.screen, (255, 255,0), pygame.Rect(self.snake[0].x+5, self.snake[0].y+15, 3, 3))
            pygame.draw.rect(self.screen, (255, 255,0), pygame.Rect(self.snake[0].x+15, self.snake[0].y+15, 3, 3))


        pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, (255,255,255))
        text2 = font.render("Steps: " + str(self.numberSetps), True, (255,255,255))
        self.screen.blit(text, [0,0])
        self.screen.blit(text2, [0,20])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
            return True

        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False
    
    def _check_collision(self, direction): #check if the snake will hit something in the next step
        # hits boundary
        if(direction == Direction.RIGHT):
            if self.head.x + BLOCK_SIZE >= self.width:
                return True
            # hits itself
            if Point(self.head.x + BLOCK_SIZE, self.head.y) in self.snake[1:]:
                return True
        elif(direction == Direction.LEFT):
            if self.head.x - BLOCK_SIZE < 0:
                return True
            # hits itself
            if Point(self.head.x - BLOCK_SIZE, self.head.y) in self.snake[1:]:
                return True
        elif(direction == Direction.DOWN):
            if self.head.y + BLOCK_SIZE >= self.height:
                return True
            # hits itself
            if Point(self.head.x, self.head.y + BLOCK_SIZE) in self.snake[1:]:
                return True
        elif(direction == Direction.UP):
            if self.head.y - BLOCK_SIZE < 0:
                return True
            # hits itself
            if Point(self.head.x, self.head.y - BLOCK_SIZE) in self.snake[1:]:
                return True

        return False
            
    def play_step(self):
        # USER INPUT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        #CONTOLO AUTO-PLAY
        #linha par coluna par
        if(self.head.y%40 == 0 and self.head.x%40 == 0):
            flip = random.randint(0, 1)
            if(flip == 0):
                self.direction = Direction.LEFT
                if(self._check_collision( self.direction )):
                    self.direction = Direction.DOWN
            elif(flip == 1):
                self.direction = Direction.DOWN
                if(self._check_collision( self.direction )):
                    self.direction = Direction.LEFT
        #linha impar coluna par
        elif(self.head.y%40 == 20 and self.head.x%40 == 0):
            flip = random.randint(0, 1)
            if(flip == 0):
                self.direction = Direction.RIGHT
                if(self._check_collision( self.direction )):
                    self.direction = Direction.DOWN
            elif(flip == 1):
                self.direction = Direction.DOWN
                if(self._check_collision( self.direction )):
                    self.direction = Direction.RIGHT
        
        #linha par coluna impar
        elif(self.head.y%40 == 0 and self.head.x%40 == 20):
            flip = random.randint(0, 1)
            if(flip == 0):
                self.direction = Direction.LEFT
                if(self._check_collision( self.direction )):
                    self.direction = Direction.UP
            elif(flip == 1):
                self.direction = Direction.UP
                if(self._check_collision( self.direction )):
                    self.direction = Direction.LEFT
                
        #linha impar coluna impar
        elif(self.head.y%40 == 20 and self.head.x%40 == 20):
            flip = random.randint(0, 1)
            if(flip == 0):
                self.direction = Direction.RIGHT
                if(self._check_collision( self.direction )):
                    self.direction = Direction.UP
            elif(flip == 1):
                self.direction = Direction.UP
                if(self._check_collision( self.direction )):
                    self.direction = Direction.RIGHT


        
        # MOVEMENT
        self._move(self.direction)
        self.snake.insert(0, self.head)
        self.numberSetps += 1

        # GAME OVER CONDITIONS
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # PLACE NEW FOOD OR JUST MOVE
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # UI
        self._update_ui()
        self.clock.tick(self.fps)

        
        return game_over, self.score


if __name__ == '__main__':
    game = SnakeGame()


    while True:
        game_over, score = game.play_step()
        if game_over == True:
            break

    print('Final Score: ', score)
    pygame.quit()
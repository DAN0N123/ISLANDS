import pygame
import random
import sys


pygame.init()

white = (255, 255, 255)
green = (83,141,78)
blue = (89, 201, 250)
red = (255,0,0)
black = (0,0,0)
yellow = (181,159,60)
gray = (80,80,80)
end_color = (246,246,246)

window_width = 800
window_height = 900

screen = pygame.display.set_mode((window_width, window_height))

is_end_screen = False

score = 0
last_score = 0
high_score = 0

island_sprite = pygame.image.load("islandyopng.png")
island_with_mark_sprite = pygame.image.load("markpng.png")
player_sprite = pygame.image.load("nobackgroundluffysprite.png")

end_screen_image_temp = pygame.image.load("endluffy.png")
end_screen_image = pygame.transform.scale(end_screen_image_temp, (250,250))


pygame.display.set_caption("ISLANDS")

class game_object():
    def __init__(self, x,y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.position = pygame.Rect(self.x, self.y, self.width, self.height)
    
class Player(game_object):
    def __init__(self, x,y, width, height):
        super().__init__(x, y, width, height)
        self.surface = pygame.Surface((width, height))
    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x > 0 and mouse_x < 800:
            self.x = mouse_x - 15
        if mouse_y >= 550 and mouse_y < 900: 
            self.y = mouse_y - 15
        elif mouse_y > 0 and mouse_y < 900:
            self.y = 550
        
        screen.blit(player_sprite,(self.x, self.y))

class scoreboard(game_object):
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.label = str(score).zfill(4)
        self.font = pygame.font.Font('arialbd.ttf', 43)
        self.outline = pygame.Rect(x - 3, y - 3, width + 6, height + 6)

    def update_score(self):
        global score
        self.label = str(score).zfill(4)
    def draw_label(self, screen):
        text_surface = self.font.render(self.label, True, black)

        text_rect = text_surface.get_rect()
        text_rect.center = self.position.center  
        text_rect.centery = self.position.centery
        pygame.draw.rect(screen, black, self.outline)
        pygame.draw.rect(screen,blue, self.position)
        pygame.draw.rect(screen, blue, text_rect)
        screen.blit(text_surface, text_rect)

class Islands(game_object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width , height)
        self.clicked = False
        self.current_islands = []
        self.keeping_track = 0
        for i in range(1,6):
            self.keeping_track += 1
            x = random.randint(90,710)
            value = 150
            y = value*i
            islandtemp = pygame.Rect(x, y, 80, 80)
            self.current_islands.append(islandtemp)

    def create_island(self):
        self.keeping_track += 1
        self.x = random.randint(90,710)
        self.y = 0
        print(self.keeping_track)
        if self.keeping_track % 25 == 0:
            islandtemp = pygame.Rect(self.x, self.y, 81, 80)
        else:
            islandtemp = pygame.Rect(self.x, self.y, 80, 80)
        self.current_islands.append(islandtemp) 

    def draw_islands(self,screen):
        for i in self.current_islands:
            x = i.x
            y = i.y
            i.topleft = (x,y)
            pygame.draw.rect(screen, blue, i) 
            if i.width == 81:
                screen.blit(island_with_mark_sprite, i)
            else:
                screen.blit(island_sprite, i)
                
    def check_if_out_of_screen(self, a_scoreboard: scoreboard):
        for i in self.current_islands:
            if i.y > 900 and i.height == 81:
                indx = self.current_islands.index(i)
                self.current_islands.pop(indx)
                self.create_island()
            elif i.y > 900 and i.height == 80:
                global is_end_screen
                global score
                global last_score
                global high_score
                last_score = score
                if last_score > high_score:
                    high_score = last_score
                is_end_screen = True

    def check_if_collided(self, mouse_position, islandlist):
        global score
        for i in islandlist:
            if i.collidepoint(mouse_position) and i.height == 80:
                i.height += 1
                score += 1
                if i.width == 81:
                    score += 4


def end_screen(x,y,width,height, islands_current: Islands):
    global last_score

    screen.fill(blue)
    end_font = pygame.font.Font('arialbd.ttf', 30)

    end_rect = pygame.Rect(x,y,width,height)
    end_rect_outline = pygame.Rect(x - 3, y - 3, width + 6, height + 6)
    pygame.draw.rect(screen, black, end_rect_outline)
    pygame.draw.rect(screen, end_color, end_rect)
    last_score_label = end_font.render(f"Score: {str(last_score)}", True, black)
    (label_x , label_y) = end_rect.topleft 
    high_score_label = end_font.render(f"Highscore: {str(high_score)}", True, black)
    screen.blit(high_score_label, (label_x + 80, label_y + 70))
    screen.blit(last_score_label, (label_x + 115, label_y + 30))

    restart_button = pygame.Rect(x + 82, y + 210, 180,40)
    restart_button_outline = pygame.Rect(x + 79, y + 207, 186,46)
    pygame.draw.rect(screen,black,restart_button_outline)
    pygame.draw.rect(screen,white, restart_button)
    try_again = end_font.render(f"TRY AGAIN", True, black)
    (againx,againy) = restart_button.topleft
    screen.blit(try_again, (againx + 8, againy + 3))
    if restart_button.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
        global is_end_screen
        global islands
        global my_player
        global my_scoreboard
        global score
        global scroll_speed
        islands = Islands(385, 700, 80, 80) 
        my_player = Player(385, 700, 30, 30)        
        my_scoreboard = scoreboard(272, 50, 250, 50)
        score = 0
        scroll_speed = 1
        is_end_screen = False




def update_objects(list):
    for i in list:
        i.y += scroll_speed

islands = Islands(385, 700, 80, 80) 
my_player = Player(385, 700, 30, 30)        
my_scoreboard = scoreboard(272, 50, 250, 50)
running = True
scroll_speed = 1
clock = pygame.time.Clock()
last_action_time = 0  


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not is_end_screen:
        screen.fill((89, 201, 250)) 
        current_time = pygame.time.get_ticks()
        update_objects(islands.current_islands) 
        

        

        if current_time - last_action_time >= 300:
            scroll_speed += 0.01
            last_action_time = current_time


        
        islands.check_if_collided(pygame.mouse.get_pos(), islands.current_islands)
        my_scoreboard.update_score()

        islands.check_if_out_of_screen(my_scoreboard)
        islands.draw_islands(screen)
        my_player.draw(screen)

        my_scoreboard.draw_label(screen)

    else:
        end_screen(225, 250, 350, 400, islands)
    

    clock.tick(144)
    pygame.display.flip()

    
    

pygame.quit()
sys.exit()
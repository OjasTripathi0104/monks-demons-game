import pygame
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60

#creating game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monks & Demons Game")
clock = pygame.time.Clock()

#loading images
background_img = pygame.image.load("background.png")
monk_img = pygame.image.load("monk.png")
demon_img = pygame.image.load("demon.png")
boat_img = pygame.image.load("boat.png")

#resizing images
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
monk_img = pygame.transform.scale(monk_img, (50, 50))
demon_img = pygame.transform.scale(demon_img, (50, 50))
boat_img = pygame.transform.scale(boat_img, (150, 90))

#initial positions of the boat, monk and demon
boat_x, boat_y = 50, 410
left_bank_monks = [("monk", 30, 310), ("monk", 55, 280), ("monk", 80, 250)]
left_bank_demons = [("demon", 100, 310), ("demon", 130, 280), ("demon", 160, 250)]
right_bank_monks = []
right_bank_demons = []
boat_on_left = True
boat_passengers = []

button_rect = pygame.Rect(320, 10, 160, 50)
font = pygame.font.Font(None, 36)

def show_popup(message):
    popup_font = pygame.font.Font(None, 72)
    text_surface = popup_font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(40, 20))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)

def is_valid_state():
    #count monks and demons on left bank
    monks_left = len(left_bank_monks)
    demons_left = len(left_bank_demons)
    
    #count monks and demons on right bank
    monks_right = len(right_bank_monks)
    demons_right = len(right_bank_demons)
    
    #add boat passengers to the correct side
    if boat_on_left:
        monks_left += len([c for c, _, _ in boat_passengers if c == "monk"])
        demons_left += len([c for c, _, _ in boat_passengers if c == "demon"])
    else:
        monks_right += len([c for c, _, _ in boat_passengers if c == "monk"])
        demons_right += len([c for c, _, _ in boat_passengers if c == "demon"])
    
    #check if demons outnumber monks on either side (only when monks are present)
    if (monks_left > 0 and demons_left > monks_left) or (monks_right > 0 and demons_right > monks_right):
        return False
    return True

def check_victory():
    #game is won when all monks and demons are on the right bank
    monks_on_right = len(right_bank_monks)
    demons_on_right = len(right_bank_demons)
    
    #if boat is on right, add its passengers too
    if not boat_on_left:
        monks_on_right += len([c for c, _, _ in boat_passengers if c == "monk"])
        demons_on_right += len([c for c, _, _ in boat_passengers if c == "demon"])
    
    #victory condition should be 3 monks and 3 demons on right bank
    return monks_on_right == 3 and demons_on_right == 3

def draw_button():
    pygame.draw.rect(screen, (0, 128, 255), button_rect, border_radius=15)
    text = font.render("Move Boat", True, (255, 255, 255))
    screen.blit(text, (button_rect.x + 20, button_rect.y + 10))

def draw_sprites():
    #drawing boat
    screen.blit(boat_img, (boat_x, boat_y))
    
    #drawing monks and demons on left bank
    for char_type, x, y in left_bank_monks + left_bank_demons:
        screen.blit(monk_img if char_type == "monk" else demon_img, (x, y))
    
    #drawing monks and demons on right bank
    for char_type, x, y in right_bank_monks + right_bank_demons:
        screen.blit(monk_img if char_type == "monk" else demon_img, (x, y))
    
    #drawing boat passengers
    for char_type, x, y in boat_passengers:
        screen.blit(monk_img if char_type == "monk" else demon_img, (x, y))

def animate_boat(target_x):
    global boat_x, boat_on_left
    step = 5 if target_x > boat_x else -5
    
    while boat_x != target_x:
        boat_x += step
        for i in range(len(boat_passengers)):
            char_type, x, y = boat_passengers[i]
            boat_passengers[i] = (char_type, x + step, y)
        
        screen.blit(background_img, (0, 0))
        draw_button()
        draw_sprites()
        pygame.display.update()
        clock.tick(FPS)
    
    #updating boat position flag
    boat_on_left = not boat_on_left
    
    #checking game state after moving
    if not is_valid_state():
        show_popup("YOU FAILED!")
        pygame.time.delay(1000)
        pygame.quit()
        exit()
    
    #checking for victory condition
    if check_victory():
        show_popup("YOU WON!")
        pygame.time.delay(1000)
        pygame.quit()
        exit()

def move_character_to_boat(char_type, index, from_left):
    global boat_passengers
    
    #boat cannot move if it's on the other side
    if from_left != boat_on_left:
        return
    
    #maximum of 2 passengers in the boat
    if len(boat_passengers) >= 2:
        return
    
    #get correct bank list
    if from_left:
        bank_list = left_bank_monks if char_type == "monk" else left_bank_demons
    else:
        bank_list = right_bank_monks if char_type == "monk" else right_bank_demons
    
    #moving character from bank to boat
    if index < len(bank_list):
        char = bank_list.pop(index)
        boat_passengers.append((char[0], boat_x + 30 + len(boat_passengers) * 40, boat_y + 15))

def move_character_from_boat(index):
    global boat_passengers
    
    if index >= len(boat_passengers):
        return
    
    char_type, _, _ = boat_passengers.pop(index)
    
    #adding character to the correct bank
    if boat_on_left:
        #adding to left bank
        target_list = left_bank_monks if char_type == "monk" else left_bank_demons
        x_pos = 30 + len(target_list) * 25 if char_type == "monk" else 100 + len(target_list) * 30
        target_list.append((char_type, x_pos, 310 - len(target_list) * 30))
    else:
        #adding to right bank
        target_list = right_bank_monks if char_type == "monk" else right_bank_demons
        x_pos = 600 + len(target_list) * 25 if char_type == "monk" else 670 + len(target_list) * 30
        target_list.append((char_type, x_pos, 310 - len(target_list) * 30))

# Game loop
running = True
while running:
    screen.blit(background_img, (0, 0))
    draw_button()
    draw_sprites()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            #when move boat button is clicked
            if button_rect.collidepoint(x, y) and len(boat_passengers) > 0:
                target_x = 500 if boat_on_left else 50
                animate_boat(target_x)
            
            #when clicking on left bank monks
            for i, (_, mx, my) in enumerate(left_bank_monks):
                if mx <= x <= mx + 50 and my <= y <= my + 50:
                    move_character_to_boat("monk", i, True)
                    break
            
            #when clicking on left bank demons
            for i, (_, dx, dy) in enumerate(left_bank_demons):
                if dx <= x <= dx + 50 and dy <= y <= dy + 50:
                    move_character_to_boat("demon", i, True)
                    break
            
            #when clicking on right bank monks
            for i, (_, mx, my) in enumerate(right_bank_monks):
                if mx <= x <= mx + 50 and my <= y <= my + 50:
                    move_character_to_boat("monk", i, False)
                    break
            
            #when clicking on right bank demons
            for i, (_, dx, dy) in enumerate(right_bank_demons):
                if dx <= x <= dx + 50 and dy <= y <= dy + 50:
                    move_character_to_boat("demon", i, False)
                    break
            
            #when clicking on boat passengers
            for i, (_, px, py) in enumerate(boat_passengers):
                if px <= x <= px + 50 and py <= y <= py + 50:
                    move_character_from_boat(i)
                    break
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
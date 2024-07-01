import pygame
import random
import sys
import math

pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_width = 30
player_height = 55
player_accel = 0.7
player_friction = -0.04

# Enemy settings
enemy_width = 50
enemy_height = 50
enemy_speed = 5

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space mission")

# Font for score
font = pygame.font.SysFont("Arial", 20)

# Font for menu
menu_font = pygame.font.SysFont("Arial", 50)
text_font = pygame.font.SysFont("Arial", 30)

# Load explosion image
explosion_image = pygame.image.load("D:/Joaquin/Downloads/pixelArts/explosion2.png")

# Load and play background music
pygame.mixer.music.load("D:/Joaquin/Downloads/Python/deadspace.mp3")  
pygame.mixer.music.play(-1) 

# Function to display main menu
def main_menu():
    menu_running = True
    while menu_running:
        background_image = pygame.image.load("D:/Joaquin/Downloads/Python/FondoEspacio.png")
        screen.blit(background_image, (0, 0))
        title_text = menu_font.render("SPACE MISSION", True, GREEN)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        
        start_text = text_font.render("Press 'SPACE' to Start", True, GREEN)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 350))
        
        quit_text = text_font.render("Press 'Q' to Quit", True, GREEN)
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 420))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_running = False  
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("D:/Joaquin/Downloads/pixelArts/nave3.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.pos = pygame.math.Vector2(self.rect.centerx, self.rect.bottom)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
    
    def update(self):
        self.acc = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -player_accel
        if keys[pygame.K_RIGHT]:
            self.acc.x = player_accel
        if keys[pygame.K_DOWN]:
            self.acc.y = player_accel
        if keys[pygame.K_UP]:
            self.acc.y = -player_accel

        # Apply friction
        self.acc += self.vel * player_friction

        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Limit player's position within screen boundaries
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > SCREEN_WIDTH - self.rect.width:
            self.pos.x = SCREEN_WIDTH - self.rect.width
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > SCREEN_HEIGHT - self.rect.height:
            self.pos.y = SCREEN_HEIGHT - self.rect.height

        # Update rect position
        self.rect.topleft = self.pos

    def get_center(self):
        return self.rect.center


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([enemy_width, enemy_height])
        self.image = pygame.image.load("D:/Joaquin/Downloads/pixelArts/meteor2.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - enemy_width)
        self.rect.y = random.randint(-150, 50)
        self.radius = enemy_width // 2
    
    def update(self):
        self.rect.y += enemy_speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
    
    def get_center(self):
        return (self.rect.x + self.radius, self.rect.y + self.radius)

# Function to detect collision between two circles
def detect_collision(center1, radius1, center2, radius2):
    distance = math.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)
    return distance < (radius1 + radius2)

# Function to show explosion
def show_explosion(player_rect):
    explosion_rect = explosion_image.get_rect(center=player_rect.center)
    screen.blit(explosion_image, explosion_rect)
    pygame.display.flip()
    pygame.time.delay(500)  

# Función para mostrar la pantalla de Game Over
def show_game_over_screen():
    screen.fill(BLACK)
    game_over_text = menu_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 250))

    restart_text = text_font.render("Press 'R' to Restart", True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))

    quit_text = text_font.render("Press 'Q' to Quit", True, WHITE)
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 400))

    pygame.display.update()

    # Esperar la entrada del usuario para reiniciar o salir
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game()  # Reiniciar el juego
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

#Game
def main_game():
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Create the player object
    player = Player()
    all_sprites.add(player)

    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    # Variable para determinar si se mostró la pantalla de Game Over
    game_over_shown = False

    # Variable for score
    score = 0
    start_ticks = pygame.time.get_ticks()
    
    #run
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update score based on time survived
        seconds = (pygame.time.get_ticks() - start_ticks) / 500  
        score = int(seconds)
                
        #Spawn rate
        def spawn_rate():
            if score < 50:
                return 15
            elif score < 100:
                return 10
            elif score < 150:
                return 5
            else:
                return 2
        
        # Spawning enemies    
        if random.randint(1, spawn_rate()) == 1:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
    
        all_sprites.update()

        # Check for collisions
        for enemy in enemies:
            if detect_collision(player.get_center(), player_width // 2, enemy.get_center(), enemy.radius):
                running = False
                show_explosion(player.rect)
                player.kill()
                show_game_over_screen()  
                game_over_shown = True
                break
        
        # Si se muestra la pantalla de Game Over, salir del bucle principal
        if game_over_shown:
            break
        
        # Imagen de fondo
        background_image = pygame.image.load("D:/Joaquin/Downloads/Python/FondoEspacio.png")
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
    
        # Display score
        score_text = font.render(f"SCORE: {score}", True, GREEN)
        screen.blit(score_text, (5, 5))

        pygame.display.update()
        FramePerSec.tick(FPS)
            
    pygame.quit()
    sys.exit()

# Start the main menu
main_menu()
main_game()
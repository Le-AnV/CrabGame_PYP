import pygame
import random

# Khởi tạo pygame
pygame.init()

# Cấu hình màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crab Dodge Game")

# Màu sắc
WHITE = (255, 255, 255)

# Load hình ảnh
background = pygame.image.load("Game/image/background_bien.png")  # Hình nền phù hợp
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

crab_img = pygame.image.load("Game/image/crab.png")  # Hình con cua
crab_width, crab_height = 80, 60
crab_img = pygame.transform.scale(crab_img, (crab_width, crab_height))

# Load nhiều loại chướng ngại vật
obstacle_images = [
    pygame.transform.scale(pygame.image.load("Game/image/garbage-bag.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("Game/image/biohazard.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("Game/image/shell.png"), (50, 50))
]

# Vị trí cua
crab_x = WIDTH // 2 - crab_width // 2
crab_y = HEIGHT - 100
crab_speed = 10

# Danh sách chướng ngại vật
obstacles = []
obstacle_speed = 5

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 36)
score = 0
lives = 3  # Số mạng sống

# Trạng thái game
running = True
paused = False

def reset_game():
    global crab_x, crab_y, obstacles, score, lives, running, paused
    crab_x = WIDTH // 2 - crab_width // 2
    crab_y = HEIGHT - 100
    obstacles = []
    score = 0
    lives = 3
    running = True
    paused = False

while running:
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_r:
                reset_game()
            if event.key == pygame.K_p:
                paused = not paused
    
    if paused:
        pause_text = font.render("Paused - Press P to Resume", True, (0, 0, 0))
        screen.blit(pause_text, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        continue
    
    # Điều khiển cua
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and crab_x > 0:
        crab_x -= crab_speed
    if keys[pygame.K_RIGHT] and crab_x < WIDTH - crab_width:
        crab_x += crab_speed
    if keys[pygame.K_UP] and crab_y > 0:
        crab_y -= crab_speed
    if keys[pygame.K_DOWN] and crab_y < HEIGHT - crab_height:
        crab_y += crab_speed
    
    # Sinh chướng ngại vật
    if random.randint(1, 30) == 1:
        obstacle_x = random.randint(0, WIDTH - 50)
        obstacle_type = random.choice(obstacle_images)
        obstacles.append([obstacle_x, 0, obstacle_type])
    
    # Di chuyển chướng ngại vật
    for obstacle in obstacles[:]:
        obstacle[1] += obstacle_speed
        if obstacle[1] > HEIGHT:
            obstacles.remove(obstacle)
            score += 1
    
    # Va chạm
    for obstacle in obstacles[:]:
        if (crab_x < obstacle[0] < crab_x + crab_width or crab_x < obstacle[0] + 50 < crab_x + crab_width) and \
           (crab_y < obstacle[1] + 50 < crab_y + crab_height):
            obstacles.remove(obstacle)
            lives -= 1
            if lives == 0:
                running = False  # Game over
    
    # Vẽ cua và chướng ngại vật
    screen.blit(crab_img, (crab_x, crab_y))
    for obstacle in obstacles:
        screen.blit(obstacle[2], (obstacle[0], obstacle[1]))
    
    # Hiển thị điểm số
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    # Hiển thị mạng sống
    lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
    screen.blit(lives_text, (WIDTH - 100, 10))
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
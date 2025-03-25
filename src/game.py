import pygame
import random
import time
from database import save_score


class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Crab Dodge Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.lives = 3
        self.level = 1
        self.level_threshold = 70  # Điểm cần đạt để lên level
        self.obstacle_speed = 5
        self.crab_speed = 10
        self.speed_boost_active = False
        self.speed_boost_end_time = 0

        # Load hình ảnh
        self.crab = pygame.image.load("Game/image/crab.png")
        self.crab = pygame.transform.scale(self.crab, (80, 60))

        # Vị trí con cua
        self.crab_x = self.WIDTH // 2 - 40
        self.crab_y = self.HEIGHT - 100

        # Background cho từng level
        self.backgrounds = [
            pygame.image.load("Game/image/beach1.jpg"),
            pygame.image.load("Game/image/beach2.jpg"),
            pygame.image.load("Game/image/beach3.jpg"),
        ]

        # Resize background
        for i in range(len(self.backgrounds)):
            self.backgrounds[i] = pygame.transform.scale(
                self.backgrounds[i], (self.WIDTH, self.HEIGHT)
            )

        # Load hình ảnh cho các vật thể
        self.obstacle_bad1 = pygame.image.load(
            "Game/image/bad1.png"
        )  # vật thể trừ 1 mạng
        self.obstacle_bad2 = pygame.image.load(
            "Game/image/bad2.png"
        )  # vật thể trừ 2 mạng
        self.item_boost = pygame.image.load(
            "Game/image/boost.png"
        )  # vật thể tăng tốc độ
        self.item_point = pygame.image.load("Game/image/point.png")  # vật thể tăng điểm

        # Resize các vật thể
        self.obstacle_bad1 = pygame.transform.scale(self.obstacle_bad1, (50, 50))
        self.obstacle_bad2 = pygame.transform.scale(self.obstacle_bad2, (50, 50))
        self.item_boost = pygame.transform.scale(self.item_boost, (50, 50))
        self.item_point = pygame.transform.scale(self.item_point, (50, 50))

        # Danh sách các vật thể: [x, y, type]
        # type: 1 = bad1, 2 = bad2, 3 = boost, 4 = point
        self.obstacles = []

        # Font cho hiển thị thông tin
        self.font = pygame.font.Font(None, 36)

        # Thời gian hiệu lực của boost tốc độ (5 giây)
        self.boost_duration = 5

        # Thời gian cuối cùng spawn vật thể
        self.last_spawn_time = time.time()

    def run(self):
        self.running = True
        while self.running:
            current_time = time.time()

            # Check speed boost expiration
            if self.speed_boost_active and current_time > self.speed_boost_end_time:
                self.speed_boost_active = False
                self.crab_speed = 10

            # Fill background theo level
            bg_index = (self.level - 1) % len(self.backgrounds)
            self.screen.blit(self.backgrounds[bg_index], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.crab_x -= self.crab_speed
            if keys[pygame.K_RIGHT]:
                self.crab_x += self.crab_speed

            # Teleport when crossing screen boundaries
            if self.crab_x < 0:
                self.crab_x = self.WIDTH - 80
            elif self.crab_x > self.WIDTH - 80:
                self.crab_x = 0

            self.spawn_obstacles()
            self.move_obstacles()
            self.check_collisions()

            # Draw crab
            self.screen.blit(self.crab, (self.crab_x, self.crab_y))

            # Display score, lives, and level
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
            level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))

            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            self.screen.blit(level_text, (10, 90))

            # Display boost indicator if active
            if self.speed_boost_active:
                boost_text = self.font.render("SPEED BOOST!", True, (255, 255, 0))
                self.screen.blit(boost_text, (self.WIDTH - 200, 10))

            pygame.display.flip()
            self.clock.tick(30)

        # Save score when game ends
        player_name = self.get_player_name()
        save_score(player_name, self.score)

    def get_player_name(self):
        # Simplified function to get player name
        # In real implementation, you'd want to create an input box
        return "Player"  # Placeholder

    def spawn_obstacles(self):
        current_time = time.time()
        spawn_delay = max(0.5, 1 - (self.level * 0.1))  # Spawn faster in higher levels

        if current_time - self.last_spawn_time >= spawn_delay:
            self.last_spawn_time = current_time
            x = random.randint(0, self.WIDTH - 50)

            # Choose obstacle type based on probabilities that change with level
            rand = random.random()

            # Base probabilities
            bad1_prob = 0.4
            bad2_prob = 0.1 + (self.level * 0.03)  # More bad2 in higher levels
            boost_prob = 0.15
            point_prob = 0.35 - (
                self.level * 0.02
            )  # Slightly fewer points in higher levels

            # Ensure probabilities sum to 1
            total = bad1_prob + bad2_prob + boost_prob + point_prob
            bad1_prob /= total
            bad2_prob /= total

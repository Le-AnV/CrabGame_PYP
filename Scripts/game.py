import pygame
import random
import time
import json
from database import save_score

# Load các cấu hình từ file JSON
with open("config/assets_config.json", "r") as assets_file:
    assets_config = json.load(assets_file)

with open("config/game_config.json", "r") as game_file:
    game_config = json.load(game_file)

# Gán các cấu hình vào các biến toàn cục
IMAGES = assets_config["IMAGES"]
SOUNDS = assets_config["SOUNDS"]
GAME_SETTINGS = game_config["GAME_SETTINGS"]
OBJECT_PROPERTIES = game_config["OBJECT_PROPERTIES"]
SPAWN_PROBABILITIES = game_config["SPAWN_PROBABILITIES"]


class Game:
    def __init__(self):
        # Khởi tạo các thông số cơ bản của game
        self.WIDTH, self.HEIGHT = GAME_SETTINGS["width"], GAME_SETTINGS["height"]
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Crab Dodge Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = GAME_SETTINGS["initial_score"]  # Điểm ban đầu
        self.lives = GAME_SETTINGS["initial_lives"]  # Số mạng ban đầu
        self.level = 1  # Cấp độ ban đầu
        self.level_threshold = GAME_SETTINGS["level_threshold"]  # Điểm cần để lên cấp
        self.obstacle_speed = GAME_SETTINGS["obstacle_speed"]  # Tốc độ vật cản
        self.crab_speed = GAME_SETTINGS["crab_speed"]  # Tốc độ cua
        self.speed_boost_active = False  # Trạng thái tăng tốc
        self.speed_boost_end_time = 0  # Thời gian kết thúc tăng tốc

        # Vị trí ban đầu của con cua
        self.crab_x = (self.WIDTH - OBJECT_PROPERTIES["crab_size"]["width"]) // 2
        self.crab_y = self.HEIGHT - OBJECT_PROPERTIES["crab_size"]["height"] - 10

        # Load hình ảnh cho các đối tượng trong game
        self.crab = pygame.image.load(IMAGES["crab"])
        self.crab = pygame.transform.scale(
            self.crab,
            (
                OBJECT_PROPERTIES["crab_size"]["width"],
                OBJECT_PROPERTIES["crab_size"]["height"],
            ),
        )
        # Load hình nền theo cấp độ
        self.backgrounds = [
            pygame.transform.scale(pygame.image.load(bg), (self.WIDTH, self.HEIGHT))
            for bg in IMAGES["backgrounds"]
        ]
        # Load các vật cản và vật phẩm
        self.obstacle_bad1 = pygame.transform.scale(
            pygame.image.load(IMAGES["obstacles"]["bad1"]),
            (
                OBJECT_PROPERTIES["obstacle_sizes"]["width"],
                OBJECT_PROPERTIES["obstacle_sizes"]["height"],
            ),
        )
        self.obstacle_bad2 = pygame.transform.scale(
            pygame.image.load(IMAGES["obstacles"]["bad2"]),
            (
                OBJECT_PROPERTIES["obstacle_sizes"]["width"],
                OBJECT_PROPERTIES["obstacle_sizes"]["height"],
            ),
        )
        self.item_boost = pygame.transform.scale(
            pygame.image.load(IMAGES["obstacles"]["boost"]),
            (
                OBJECT_PROPERTIES["item_sizes"]["width"],
                OBJECT_PROPERTIES["item_sizes"]["height"],
            ),
        )
        self.item_point = pygame.transform.scale(
            pygame.image.load(IMAGES["obstacles"]["point"]),
            (
                OBJECT_PROPERTIES["item_sizes"]["width"],
                OBJECT_PROPERTIES["item_sizes"]["height"],
            ),
        )
        # Load hình ảnh trái tim (biểu tượng mạng sống)
        self.heart_img = pygame.transform.scale(
            pygame.image.load(IMAGES["heart"]),
            (
                OBJECT_PROPERTIES["heart_size"]["width"],
                OBJECT_PROPERTIES["heart_size"]["height"],
            ),
        )

        # Load âm thanh cho game
        self.background_music = pygame.mixer.Sound(SOUNDS["background_music"])
        self.background_music.set_volume(0.5)  # Giảm âm lượng nhạc nền
        self.game_over_sound = pygame.mixer.Sound(SOUNDS["game_over"])
        self.getCoin_sound = pygame.mixer.Sound(SOUNDS["get_coin"])
        self.upSpeed_sound = pygame.mixer.Sound(SOUNDS["speed_boost"])
        self.badObj_sound = pygame.mixer.Sound(SOUNDS["bad_object"])

        # Thuộc tính thanh máu
        self.health_bar_width = 200
        self.health_bar_height = 20
        self.health_bar_x = 10
        self.health_bar_y = 130

        # Danh sách các vật thể trong game (tọa độ x, y, loại vật thể)
        self.obstacles = []

        # Font chữ để hiển thị thông tin
        self.font = pygame.font.Font(None, 36)

        # Thời gian hiệu lực của tăng tốc (5 giây)
        self.boost_duration = GAME_SETTINGS["boost_duration"]

        # Thời gian cuối cùng sinh vật thể
        self.last_spawn_time = time.time()

    def run(self):
        # Hàm chính để chạy game
        self.running = True
        self.background_music.play(-1)  # Phát nhạc nền lặp lại
        while self.running:
            current_time = time.time()

            # Kiểm tra nếu tăng tốc đã hết hiệu lực
            if self.speed_boost_active and current_time > self.speed_boost_end_time:
                self.speed_boost_active = False
                self.crab_speed = GAME_SETTINGS["crab_speed"]

            # Hiển thị hình nền theo cấp độ
            bg_index = (self.level - 1) % len(self.backgrounds)
            self.screen.blit(self.backgrounds[bg_index], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Thoát game nếu nhấn nút đóng cửa sổ
                    self.running = False

            # Kiểm tra phím bấm để di chuyển con cua
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.crab_x -= self.crab_speed  # Di chuyển cua sang trái
            if keys[pygame.K_RIGHT]:
                self.crab_x += self.crab_speed  # Di chuyển cua sang phải

            # Thêm logic dịch chuyển cua khi vượt giới hạn màn hình
            if self.crab_x < 0:
                self.crab_x = self.WIDTH - OBJECT_PROPERTIES["crab_size"]["width"]
            elif self.crab_x > self.WIDTH - OBJECT_PROPERTIES["crab_size"]["width"]:
                self.crab_x = 0

            self.spawn_obstacles()
            self.check_collisions()

            # Vẽ con cua
            self.screen.blit(self.crab, (self.crab_x, self.crab_y))

            # Hiển thị điểm số, số mạng và cấp độ
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
            level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))

            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            self.screen.blit(level_text, (10, 90))

            # Vẽ biểu tượng trái tim để hiển thị số mạng còn lại
            self.draw_health_icon()

            # Vẽ các vật thể
            for obstacle in self.obstacles:
                if obstacle[2] == 1:  # bad1
                    self.screen.blit(self.obstacle_bad1, (obstacle[0], obstacle[1]))
                elif obstacle[2] == 2:  # bad2
                    self.screen.blit(self.obstacle_bad2, (obstacle[0], obstacle[1]))
                elif obstacle[2] == 3:  # boost
                    self.screen.blit(self.item_boost, (obstacle[0], obstacle[1]))
                elif obstacle[2] == 4:  # point
                    self.screen.blit(self.item_point, (obstacle[0], obstacle[1]))

            # Hiển thị thông báo tăng tốc nếu đang kích hoạt
            if self.speed_boost_active:
                boost_text = self.font.render("SPEED BOOST!", True, (255, 255, 0))
                self.screen.blit(boost_text, (self.WIDTH - 200, 10))

            pygame.display.flip()
            self.clock.tick(30)

        # Dừng nhạc nền khi game kết thúc
        self.background_music.stop()

        # Lưu điểm số khi game kết thúc
        player_name = self.get_player_name()
        save_score(player_name, self.score)

    def get_player_name(self):
        # Hàm lấy tên người chơi (hiện tại là giá trị mặc định)
        return "Player"  # Placeholder

    def spawn_obstacles(self):
        # Hàm sinh các vật thể trong game
        current_time = time.time()
        spawn_delay = max(0.5, 1 - (self.level * 0.1))

        if current_time - self.last_spawn_time >= spawn_delay:
            self.last_spawn_time = current_time
            x = random.randint(
                0, self.WIDTH - OBJECT_PROPERTIES["obstacle_sizes"]["width"]
            )

            # Điều chỉnh xác suất sinh vật thể theo cấp độ
            bad2_prob = max(0, SPAWN_PROBABILITIES["bad2"] + (self.level * 0.03))
            point_prob = max(0, SPAWN_PROBABILITIES["point"] - (self.level * 0.02))
            total = (
                SPAWN_PROBABILITIES["bad1"]
                + bad2_prob
                + SPAWN_PROBABILITIES["boost"]
                + point_prob
            )
            probabilities = {
                "bad1": SPAWN_PROBABILITIES["bad1"] / total,
                "bad2": bad2_prob / total,
                "boost": SPAWN_PROBABILITIES["boost"] / total,
                "point": point_prob / total,
            }

            rand = random.random()
            if rand < probabilities["bad1"]:
                self.obstacles.append([x, 0, 1])
            elif rand < probabilities["bad1"] + probabilities["bad2"]:
                self.obstacles.append([x, 0, 2])
            elif (
                rand
                < probabilities["bad1"] + probabilities["bad2"] + probabilities["boost"]
            ):
                self.obstacles.append([x, 0, 3])
            else:
                self.obstacles.append([x, 0, 4])

    def check_collisions(self):
        # Hàm kiểm tra va chạm giữa con cua và các vật thể
        for obstacle in self.obstacles[:]:
            obstacle[1] += self.obstacle_speed

            # Kiểm tra va chạm giữa con cua và vật thể
            if (
                self.crab_x < obstacle[0] + OBJECT_PROPERTIES["obstacle_sizes"]["width"]
                and self.crab_x + OBJECT_PROPERTIES["crab_size"]["width"] > obstacle[0]
                and self.crab_y
                < obstacle[1] + OBJECT_PROPERTIES["obstacle_sizes"]["height"]
                and self.crab_y + OBJECT_PROPERTIES["crab_size"]["height"] > obstacle[1]
            ):
                if obstacle[2] == 1:  # bad1
                    self.lives -= 1
                    self.badObj_sound.play()
                elif obstacle[2] == 2:  # bad2
                    self.lives -= 2
                    self.badObj_sound.play()
                elif obstacle[2] == 3:  # boost
                    self.speed_boost_active = True
                    self.upSpeed_sound.play()
                    self.crab_speed = GAME_SETTINGS["boosted_crab_speed"]
                    self.speed_boost_end_time = time.time() + self.boost_duration
                elif obstacle[2] == 4:  # point
                    self.getCoin_sound.play()
                    self.score += GAME_SETTINGS["point_value"]

                # Xóa vật thể sau khi xử lý va chạm
                self.obstacles.remove(obstacle)

            # Xóa vật thể nếu nó ra khỏi màn hình
            if obstacle[1] > self.HEIGHT:
                self.obstacles.remove(obstacle)

        # Kiểm tra nếu game kết thúc
        if self.lives <= 0:
            self.game_over_sound.play()
            self.running = False

        # Tăng cấp độ nếu đạt điểm yêu cầu
        if self.score >= self.level * self.level_threshold:
            self.level += 1
            self.obstacle_speed += GAME_SETTINGS["speed_increment"]

    def draw_health_icon(self):
        # Vẽ biểu tượng trái tim để hiển thị số mạng còn lại
        for i in range(self.lives):
            self.screen.blit(
                self.heart_img,
                (
                    self.health_bar_x + i * OBJECT_PROPERTIES["heart_spacing"],
                    self.health_bar_y,
                ),
            )

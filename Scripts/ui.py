import pygame
import json
from game import Game
from database import get_high_scores

# Tải cấu hình từ file JSON
with open("config/assets_config.json", "r") as assets_file:
    assets_config = json.load(assets_file)

# Lấy danh sách hình ảnh từ cấu hình
IMAGES = assets_config["IMAGES"]


# Lớp InputBox để tạo hộp nhập liệu
class InputBox:
    def __init__(self, x, y, w, h, text=""):
        # Khởi tạo hộp nhập liệu với vị trí, kích thước và văn bản mặc định
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color("lightskyblue3")  # Màu mặc định
        self.text = text
        self.font = pygame.font.Font(None, 32)  # Font chữ
        self.txt_surface = self.font.render(
            text, True, pygame.Color("red")
        )  # Bề mặt văn bản
        self.active = False  # Trạng thái hoạt động của hộp nhập liệu

    def handle_event(self, event):
        # Xử lý sự kiện chuột và bàn phím cho hộp nhập liệu
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra nếu nhấp chuột vào hộp nhập liệu
            if self.rect.collidepoint(event.pos):
                self.active = not self.active  # Đổi trạng thái hoạt động
            else:
                self.active = False
            # Thay đổi màu sắc khi hộp nhập liệu được kích hoạt
            self.color = (
                pygame.Color("orange") if self.active else pygame.Color("lightskyblue3")
            )
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:  # Nhấn Enter để trả về văn bản
                    return self.text.strip()
                elif event.key == pygame.K_BACKSPACE:  # Xóa ký tự cuối cùng
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode  # Thêm ký tự mới
                # Cập nhật bề mặt văn bản
                self.txt_surface = self.font.render(self.text, True, self.color)
        return None

    def update(self):
        # Điều chỉnh chiều rộng của hộp nhập liệu dựa trên độ dài văn bản
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Vẽ hộp nhập liệu và văn bản lên màn hình
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


# Hàm hiển thị menu chính
def main_menu():
    WIDTH, HEIGHT = 800, 600  # Kích thước cửa sổ
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Tạo cửa sổ
    pygame.display.set_caption("Crab Dodge Game")  # Tiêu đề cửa sổ

    # Tải và thay đổi kích thước hình nền menu
    bg_image = pygame.image.load(IMAGES["menu_background"])
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    # Khởi tạo font chữ cho tiêu đề và nút
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 50)

    # Màu sắc cho nút và văn bản
    button_color = (0, 102, 204)
    button_hover_color = (222, 188, 153)
    text_color = (255, 255, 255)

    # Danh sách các nút trong menu
    buttons = [
        {"text": "Start Game", "pos": (WIDTH // 2, 250), "size": (250, 60)},
        {"text": "High Scores", "pos": (WIDTH // 2, 350), "size": (250, 60)},
        {"text": "Exit", "pos": (WIDTH // 2, 450), "size": (250, 60)},
    ]

    running = True
    while running:
        screen.blit(bg_image, (0, 0))  # Vẽ hình nền

        # Vẽ tiêu đề
        title_text = title_font.render("Crab Dodge Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 120))
        screen.blit(title_text, title_rect)

        mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Thoát chương trình
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra nhấp chuột
                mouse_clicked = True

        for button in buttons:
            # Tạo hình chữ nhật đại diện cho nút
            button_rect = pygame.Rect(0, 0, button["size"][0], button["size"][1])
            button_rect.center = button["pos"]

            # Kiểm tra nếu chuột di chuyển qua nút
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(
                    screen, button_hover_color, button_rect, border_radius=10
                )
                if mouse_clicked:
                    # Xử lý khi nhấp vào từng nút
                    if button["text"] == "Start Game":
                        player_name = get_player_name(screen)  # Lấy tên người chơi
                        game = Game()
                        game.get_player_name = (
                            lambda: player_name
                        )  # Truyền tên người chơi
                        game.run()  # Chạy trò chơi
                    elif button["text"] == "High Scores":
                        display_high_scores(screen)  # Hiển thị điểm cao
                    elif button["text"] == "Exit":
                        running = False  # Thoát chương trình
            else:
                pygame.draw.rect(screen, button_color, button_rect, border_radius=10)

            # Vẽ văn bản trên nút
            text = button_font.render(button["text"], True, text_color)
            text_rect = text.get_rect(center=button["pos"])
            screen.blit(text, text_rect)

        pygame.display.flip()  # Cập nhật màn hình

    pygame.quit()  # Thoát pygame


# Hàm lấy tên người chơi
def get_player_name(screen):
    WIDTH, HEIGHT = 800, 600  # Kích thước cửa sổ

    # Tải và thay đổi kích thước hình nền
    bg_image = pygame.image.load(IMAGES["backgrounds"][2])
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    font = pygame.font.Font(None, 32)  # Font chữ
    title_font = pygame.font.Font(None, 50)  # Font tiêu đề
    input_box = InputBox(WIDTH // 2 - 100, HEIGHT // 2, 200, 32)  # Hộp nhập liệu

    # Tiêu đề
    title_text = title_font.render("Enter Your Name:", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    # Nút bắt đầu
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)
    button_text = font.render("Start Game", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)

    name = "Player"  # Tên mặc định
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Thoát chương trình
                return name

            result = input_box.handle_event(event)  # Xử lý sự kiện nhập liệu
            if result:
                name = result if result.strip() else "Player"  # Lấy tên người chơi
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Nhấp vào nút bắt đầu
                    name = input_box.text if input_box.text.strip() else "Player"
                    done = True

        input_box.update()  # Cập nhật hộp nhập liệu

        # Vẽ giao diện
        screen.blit(bg_image, (0, 0))
        screen.blit(title_text, title_rect)
        input_box.draw(screen)
        pygame.draw.rect(screen, (0, 102, 204), button_rect, border_radius=10)
        screen.blit(button_text, button_text_rect)

        pygame.display.flip()  # Cập nhật màn hình

    return name


# Hàm hiển thị điểm cao
def display_high_scores(screen):
    scores = get_high_scores()  # Lấy danh sách điểm cao
    WIDTH, HEIGHT = 800, 600  # Kích thước cửa sổ

    # Tải và thay đổi kích thước hình nền
    bg_image = pygame.image.load(IMAGES["score_background"])
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    font = pygame.font.Font(None, 36)  # Font chữ

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Thoát chương trình
                running = False
            if (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):  # Nhấn ESC để thoát
                running = False

        screen.blit(bg_image, (0, 0))  # Vẽ hình nền

        if scores.empty:
            # Hiển thị thông báo nếu không có điểm cao
            no_scores_text = font.render(
                "No high scores available.", True, (255, 255, 255)
            )
            screen.blit(no_scores_text, (WIDTH // 2 - 150, HEIGHT // 2))
        else:
            # Hiển thị danh sách điểm cao
            for i, row in scores.iterrows():
                score_text = font.render(
                    f"{i + 1}. {row['Name']} - {row['Score']}", True, (255, 165, 0)
                )
                screen.blit(score_text, (WIDTH // 2 - 100, 150 + i * 40))

        pygame.display.flip()  # Cập nhật màn hình

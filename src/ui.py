import pygame
import pygame.locals as pl
from game import Game
from database import get_high_scores


class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color("dodgerblue2")
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box
            self.color = (
                pygame.Color("dodgerblue2")
                if self.active
                else pygame.Color("lightskyblue3")
            )
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text
                self.txt_surface = self.font.render(self.text, True, self.color)
        return None

    def update(self):
        # Resize the box if the text is too long
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect
        pygame.draw.rect(screen, self.color, self.rect, 2)


def main_menu():
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crab Dodge Game")

    # Load và scale background cho menu
    bg_image = pygame.image.load("Game/image/menu_bg.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    # Font cho menu
    title_font = pygame.font.Font(None, 72)
    button_font = pygame.font.Font(None, 50)

    # Màu sắc
    button_color = (0, 102, 204)
    button_hover_color = (0, 153, 255)
    text_color = (255, 255, 255)

    # Định nghĩa các nút
    buttons = [
        {"text": "Start Game", "pos": (WIDTH // 2, 250), "size": (250, 60)},
        {"text": "High Scores", "pos": (WIDTH // 2, 350), "size": (250, 60)},
        {"text": "Exit", "pos": (WIDTH // 2, 450), "size": (250, 60)},
    ]

    running = True
    while running:
        # Vẽ background
        screen.blit(bg_image, (0, 0))

        # Vẽ tiêu đề
        title_text = title_font.render("Crab Dodge Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 120))
        screen.blit(title_text, title_rect)

        # Vị trí chuột
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True

        # Vẽ các nút
        for button in buttons:
            button_rect = pygame.Rect(0, 0, button["size"][0], button["size"][1])
            button_rect.center = button["pos"]

            # Kiểm tra hover
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(
                    screen, button_hover_color, button_rect, border_radius=10
                )
                if mouse_clicked:
                    if button["text"] == "Start Game":
                        player_name = get_player_name(screen)
                        game = Game()
                        game.get_player_name = (
                            lambda: player_name
                        )  # Override player name method
                        game.run()
                    elif button["text"] == "High Scores":
                        get_high_scores(screen)
                    elif button["text"] == "Exit":
                        running = False
            else:
                pygame.draw.rect(screen, button_color, button_rect, border_radius=10)

            # Vẽ text lên nút
            text = button_font.render(button["text"], True, text_color)
            text_rect = text.get_rect(center=button["pos"])
            screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()


def get_player_name(screen):
    WIDTH, HEIGHT = 800, 600

    # Load và scale background cho menu input name
    bg_image = pygame.image.load("Game/image/menu_bg.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 50)
    input_box = InputBox(WIDTH // 2 - 100, HEIGHT // 2, 200, 32)

    title_text = title_font.render("Enter Your Name:", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)
    button_text = font.render("Start Game", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)

    name = "Player"  # Default name
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return name

            result = input_box.handle_event(event)
            if result:
                name = result if result.strip() else "Player"
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    name = input_box.text if input_box.text.strip() else "Player"
                    done = True

        input_box.update()

        screen.blit(bg_image, (0, 0))

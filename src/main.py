import pygame
import os
from ui import main_menu

# from image import *


def check_resources():
    """Kiểm tra các thư mục và tệp cần thiết"""
    # Kiểm tra thư mục ảnh
    if not os.path.exists("Game/image"):
        os.makedirs("Game/image")
        print("Đã tạo thư mục Game/image")

    # Kiểm tra file config
    if not os.path.exists("Game/config.ini"):
        with open("Game/config.ini", "w") as config_file:
            config_file.write("[database]\n")
            config_file.write("dbName=game_db\n")
            config_file.write("hostName=localhost\n")
            config_file.write("password=password\n")
            config_file.write("userName=postgres\n")
            config_file.write("port=5432\n")
        print("Đã tạo file config.ini mặc định")


def main():
    pygame.init()

    # Kiểm tra tài nguyên trước khi chạy
    check_resources()

    # Danh sách file ảnh cần có
    required_images = [
        "Game\\image\\crab.png",  # crab
        "Game\\image\\biohazard.png",  # bag1
        "Game\\image\\biohazard.png",  # bag2
        "Game\\image\\shell.png",  # boost
        "Game\\image\\shell.png",  # point
        "Game\\image\\background_bien.png",  # beach1
        "Game\\image\\background_bien.png",  # beach2
        "Game\\image\\background_bien.png",  # beach3
        "Game\\image\\background_bien.png",  # menu background
    ]

    # Thông báo về các file ảnh cần thêm
    missing_images = [
        img
        for img in required_images
        if not os.path.exists(img.replace("Game\\image\\", "Game/image/"))
    ]  # Fixed path handling
    if missing_images:
        print("Vui lòng thêm các file ảnh sau vào thư mục Game/image:")
        for img in missing_images:
            print(f"- {img.replace('Game\\image\\', '')}")
        return  # Exit if resources are missing

    # Chạy menu chính
    main_menu()


if __name__ == "__main__":
    main()

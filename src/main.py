import pygame
import os
from ui import main_menu


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
        "crab.png",
        "bad1.png",
        "bad2.png",
        "boost.png",
        "point.png",
        "beach1.jpg",
        "beach2.jpg",
        "beach3.jpg",
        "menu_bg.jpg",
    ]

    # Thông báo về các file ảnh cần thêm
    missing_images = [
        img for img in required_images if not os.path.exists(f"Game/image/{img}")
    ]
    if missing_images:
        print("Vui lòng thêm các file ảnh sau vào thư mục Game/image:")
        for img in missing_images:
            print(f"- {img}")

    # Chạy menu chính
    main_menu()


if __name__ == "__main__":
    main()

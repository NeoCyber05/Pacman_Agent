from Utils.utils import *
from constants import *
import pygame

# KHỞI TẠO CÁC BIẾN
N = M = Score = _state_PacMan = 0
_map = []
_wall = []
_road = []
_food = []
_ghost = []
_food_Position = []
_ghost_Position = []
_visited = []
PacMan: Player
Level = 1
Map_name = ""


# KHỞI TẠO PYGAME
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PacMan AI')
clock = pygame.time.Clock()

pygame.font.init()
my_font = pygame.font.SysFont('Contrail One', 30)    #Score lúc game run
my_font_2 = pygame.font.SysFont('Contrail One', 100) #Your Score ( Hiện lúc end game)


def readMapInFile(map_name: str):
    f = open(map_name, "r")   # Mở file để đọc
    x = f.readline().split()  # Đọc dòng đầu tiên của file, chứa kích thước bản đồ (N và M)
    global N, M, _map
    _map = []                    # Khởi tạo lại bản đồ
    N, M = int(x[0]), int(x[1])  # Gán N và M từ file vào các biến toàn cục (số hàng và số cột của bản đồ)

    for _ in range(N):  # Lặp qua từng hàng của bản đồ
        line = f.readline().split()
        _m = []
        for j in range(M):           # Lặp qua từng cột trong mỗi hàng
            _m.append(int(line[j]))
        _map.append(_m)

    global PacMan
    x = f.readline().split()  # Đọc dòng cuối cùng của file chứa tọa độ của PacMan

    # Tính toán lề (margin) để căn giữa bản đồ trên màn hình
    MARGIN["TOP"] = max(0, (HEIGHT - N * SIZE_WALL) // 2)
    MARGIN["LEFT"] = max(0, (WIDTH - M * SIZE_WALL) // 2)

    # Khởi tạo đối tượng PacMan với tọa độ lấy từ file và ảnh khởi tạo đầu tiên
    PacMan = Player(int(x[0]), int(x[1]), IMAGE_PACMAN[0])

    f.close()



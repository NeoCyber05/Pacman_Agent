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


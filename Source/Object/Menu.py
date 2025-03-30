import os

import pygame
import sys

from constants import FPS, WIDTH, HEIGHT, BLUE, BLACK, WALL, FOOD, WHITE, YELLOW, MONSTER, IMAGE_GHOST, \
    IMAGE_PACMAN

# Khởi tạo các thành phần pygame
clock = pygame.time.Clock()
bg = pygame.image.load("images/home_bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
pygame.init()
font = pygame.font.SysFont('Arial', 40)
my_font = pygame.font.SysFont('Comic Sans MS', 70)

# Biến toàn cục
_N = _M = 0
__map = 0
SIZE_WALL = 20


class Button:
    """
    Lớp Button dùng để tạo các phần tử giao diện tương tác
    """
    def __init__(self, x, y, width, height, screen, buttonText="Button", onClickFunction=None):
        # Khởi tạo thuộc tính của nút
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction
        self.screen = screen

        # Định nghĩa màu sắc cho các trạng thái khác nhau của nút
        self.fillColors = {
            'normal': '#FF4500',
            'hover': '#FF6347',
            'pressed': '#FF7F50',
        }

        # Tạo bề mặt và hình chữ nhật cho nút
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Hiển thị văn bản của nút
        self.buttonSurf = font.render(buttonText, True, (255, 255, 255))

    def process(self):
        """
        Xử lý tương tác và hiển thị nút
        """
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.onClickFunction()

        # Canh giữa văn bản trên nút
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        pygame.draw.rect(self.buttonSurface, BLUE, (0, 0, self.width, self.height), 5)
        self.screen.blit(self.buttonSurface, self.buttonRect)


class Menu:
    """
    Lớp Menu chính cho trò chơi
    """
    def __init__(self, screen):
        # Khởi tạo thuộc tính menu
        self.current_level = 0
        self.clicked = False
        self.map_name = []
        self.current_map = 0
        self.done = False
        self.current_screen = 1  # Bắt đầu từ menu chính
        self.screen = screen
        
        # Tạo nút cho menu chính
        self.btnStart = Button(WIDTH // 2 - 100 + 5, HEIGHT - 170, 200, 100, screen, "Start", self.myFunction)

        # Tạo nút cho lựa chọn cấp độ
        self.btnLevel1 = Button(WIDTH // 2 - 150, HEIGHT // 4 * 0 + 20, 300, 100, screen, "Level 1",
                                self._load_map_level_1)
        self.btnLevel2 = Button(WIDTH // 2 - 150, HEIGHT // 4 * 1 + 20, 300, 100, screen, "Level 2",
                                self._load_map_level_2)
        self.btnLevel3 = Button(WIDTH // 2 - 150, HEIGHT // 4 * 2 + 20, 300, 100, screen, "Level 3",
                                self._load_map_level_3)
        self.btnLevel4 = Button(WIDTH // 2 - 150, HEIGHT // 4 * 3 + 20, 300, 100, screen, "Level 4",
                                self._load_map_level_4)

        # Tạo nút cho điều hướng bản đồ
        self.btnPrev = Button(WIDTH // 2 - 250, HEIGHT // 4 * 3 + 35, 100, 100, screen, "<", self.prevMap)
        self.btnNext = Button(WIDTH // 2 + 150, HEIGHT // 4 * 3 + 35, 100, 100, screen, ">", self.nextMap)
        self.btnPlay = Button(WIDTH // 2 - 75, HEIGHT // 4 * 3 + 35, 150, 100, screen, "PLAY", self.selectMap)

        # Tạo nút quay lại
        self.btnBack = Button(40, HEIGHT // 4 * 3 + 35, 150, 100, screen, "BACK", self.myFunction)

    def nextMap(self):
        """
        Chuyển đến bản đồ tiếp theo trong cấp độ hiện tại
        """
        if self.clicked:
            self.current_screen = 3
            self.current_map = (self.current_map + 1) % len(self.map_name)
        self.clicked = False

    def prevMap(self):
        """
        Chuyển đến bản đồ trước đó trong cấp độ hiện tại
        """
        if self.clicked:
            self.current_screen = 3
            self.current_map -= 1
            if self.current_map < 0:
                self.current_map += len(self.map_name)
        self.clicked = False

    def myFunction(self):
        """
        Chuyển đến màn hình lựa chọn cấp độ và đặt lại lựa chọn
        """
        self.current_screen = 2
        self.map_name = []
        self.current_map = 0
        self.current_level = 0

    def _load_map_level_1(self):
        """
        Tải bản đồ cho Cấp độ 1
        """
        if self.clicked:
            self.current_level = 1
            for file in os.listdir('../Input/Level1'):
                self.map_name.append('../Input/Level1/' + file)
            self.current_screen = 3
        self.clicked = False

    def _load_map_level_2(self):
        """
        Tải bản đồ cho Cấp độ 2
        """
        if self.clicked:
            self.current_level = 2
            for file in os.listdir('../Input/Level2'):
                self.map_name.append('../Input/Level2/' + file)
            self.current_screen = 3
        self.clicked = False

    def _load_map_level_3(self):
        """
        Tải bản đồ cho Cấp độ 3
        """
        if self.clicked:
            self.current_level = 3
            for file in os.listdir('../Input/Level3'):
                self.map_name.append('../Input/Level3/' + file)
            self.current_screen = 3
        self.clicked = False

    def _load_map_level_4(self):
        """
        Tải bản đồ cho Cấp độ 4
        """
        if self.clicked:
            self.current_level = 4
            for file in os.listdir('../Input/Level4'):
                self.map_name.append('../Input/Level4/' + file)
            self.current_screen = 3
        self.clicked = False

    def draw_map(self, fileName):
        """
        Vẽ bản xem trước bản đồ dựa trên tệp bản đồ đã chọn
        """
        # Hiển thị thông tin cấp độ và bản đồ
        text_surface = my_font.render(
            'LEVEL {level} - MAP {map}'.format(level=self.current_level, map=self.current_map + 1), False, WHITE)
        self.screen.blit(text_surface, (WIDTH // 2 - 270, 0))

        # Mở và đọc tệp bản đồ
        f = open(fileName, "r")
        x = f.readline().split()
        count_ghost = 0
        N, M = int(x[0]), int(x[1])

        # Tính toán lề để canh giữa bản đồ
        MARGIN_TOP = 100
        MARGIN_LEFT = (WIDTH - M * SIZE_WALL) // 2

        # Vẽ các phần tử bản đồ
        for i in range(N):
            line = f.readline().split()
            for j in range(M):
                cell = int(line[j])
                if cell == WALL:
                    # Vẽ tường
                    image = pygame.Surface([SIZE_WALL, SIZE_WALL])
                    # image.fill(color)
                    pygame.draw.rect(image, BLUE, (0, 0, SIZE_WALL, SIZE_WALL), 1)
                    top = i * SIZE_WALL + MARGIN_TOP
                    left = j * SIZE_WALL + MARGIN_LEFT
                    self.screen.blit(image, (left, top))
                elif cell == FOOD:
                    # Vẽ thức ăn
                    image = pygame.Surface([SIZE_WALL // 2, SIZE_WALL // 2])
                    image.fill(WHITE)
                    image.set_colorkey(WHITE)
                    pygame.draw.ellipse(image, YELLOW, [0, 0, SIZE_WALL // 2, SIZE_WALL // 2])

                    top = i * SIZE_WALL + MARGIN_TOP + SIZE_WALL // 2 - SIZE_WALL // 4
                    left = j * SIZE_WALL + MARGIN_LEFT + SIZE_WALL // 2 - SIZE_WALL // 4
                    self.screen.blit(image, (left, top))
                elif cell == MONSTER:
                    # Vẽ ma
                    image = pygame.image.load(IMAGE_GHOST[count_ghost]).convert_alpha()
                    image = pygame.transform.scale(image, (SIZE_WALL, SIZE_WALL))
                    top = i * SIZE_WALL + MARGIN_TOP
                    left = j * SIZE_WALL + MARGIN_LEFT
                    count_ghost = (count_ghost + 1) % len(IMAGE_GHOST)
                    self.screen.blit(image, (left, top))

        # Vẽ vị trí Pacman
        x = f.readline().split()
        image = pygame.image.load(IMAGE_PACMAN[0]).convert_alpha()
        image = pygame.transform.scale(image, (SIZE_WALL, SIZE_WALL))
        top = int(x[0]) * SIZE_WALL + MARGIN_TOP
        left = int(x[1]) * SIZE_WALL + MARGIN_LEFT
        self.screen.blit(image, (left, top))

        f.close()

    def selectMap(self):
        if self.clicked:
            self.done = True

    def run(self):
        """
        Vòng lặp menu chính
        """
        while not self.done:
            self.clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            # Màn hình menu chính
            if self.current_screen == 1:
                self.screen.blit(bg, (0, 0))
                self.btnStart.process()

            # Màn hình lựa chọn cấp độ
            elif self.current_screen == 2:
                self.screen.fill(BLACK)
                self.btnLevel1.process()
                self.btnLevel2.process()
                self.btnLevel3.process()
                self.btnLevel4.process()

            # Màn hình hiển thị bản đồ ban đầu
            elif self.current_screen == 3:
                self.screen.fill(BLACK)
                self.current_screen = 4
                self.draw_map(self.map_name[self.current_map])

            # Màn hình điều hướng bản đồ
            elif self.current_screen == 4:
                self.btnNext.process()
                self.btnPrev.process()
                self.btnPlay.process()
                self.btnBack.process()

            pygame.display.flip()
            clock.tick(FPS)

        # Trả về cấp độ và tệp bản đồ đã chọn
        return [self.current_level, self.map_name[self.current_map]]
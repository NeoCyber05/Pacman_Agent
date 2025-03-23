from constants import FOOD, EMPTY, WALL

#          phải    trái     lên      xuống
moving = [[0, 1], [0, -1], [1, 0], [-1, 0]]
#DDX -> moving

#Check object có nằm trong map ko
def in_bound(row:int , col:int ,N:int,M:int ) -> bool:
    return 0<row<N and 0< col < M

#Check vị trí hợp lệ
def isValid(_map,row:int ,col:int ,N:int , M:int ) -> bool:
    return in_bound(row,col,N,M) and (_map[row][col] == FOOD or _map[row][col] == EMPTY)

#Check chạm tường
def isWall(_map, row: int, col: int, N: int, M: int) -> bool:
    return in_bound(row, col, N, M) and _map[row][col] != WALL


# Tính kc Manhattan
def Manhattan(x1: int, y1: int, x2: int, y2: int) -> float:
    return abs(x1 - x2) + abs(y1 - y2)



def find_nearest_food(food_positions: list[list[int]], start_row: int, start_col: int):

    if not food_positions:
        return [-1, -1, -1]

    # Danh sách gồm các tuple (chỉ số, vị trí) cho food
    toa_do_food = list(enumerate(food_positions))

    # Hàm tính khoảng cách từ vị trí bắt đầu đến một thức ăn
    def distance_to_food(food):
        index, row,col = food

        distance = Manhattan(food_row, food_col, start_row, start_col)
        return distance

    # Tìm thức ăn có khoảng cách ngắn nhất trong list
    nearest_food = min(toa_do_food, key=distance_to_food)

    # nearest_food là một tuple (index, [row, col])
    index, food_row,food_col = nearest_food
    return [food_row, food_col, index]



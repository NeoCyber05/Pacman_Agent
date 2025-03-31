from Utils.utils import *
import math
import random


class Node:
    def __init__(self, prev, action):
        self.prev = prev
        self.prevaction = action
        self.childList = []
        self.visitnumber = 0
        self.score = 0
        self.expanded = False

    def createChild(self, action):
        childNode = Node(self, action)
        self.childList.append(childNode)
        return childNode


def gameEvaluation(rootState, currentState):
    # Đánh giá trạng thái game
    # Trả về điểm số - có thể cần điều chỉnh dựa vào cách đánh giá trạng thái của bạn
    if currentState.isWin():
        return 1000
    elif currentState.isLose():
        return -1000
    else:
        # Đánh giá dựa trên điểm số, khoảng cách đến thức ăn, v.v.
        return currentState.getScore() - rootState.getScore()


class GameState:
    def __init__(self, _map, food_Position, pacman_row, pacman_col, N, M, Score=0):
        self.map = _map.copy()
        self.food_Position = food_Position.copy()
        self.pacman_row = pacman_row
        self.pacman_col = pacman_col
        self.N = N
        self.M = M
        self.Score = Score

    def getLegalPacmanActions(self):
        # Trả về danh sách các hành động hợp lệ
        actions = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # left, right, up, down
        action_names = ["LEFT", "RIGHT", "UP", "DOWN"]

        for i in range(4):
            new_row = self.pacman_row + directions[i][0]
            new_col = self.pacman_col + directions[i][1]

            if 0 <= new_row < self.N and 0 <= new_col < self.M and self.map[new_row][
                new_col] != 1:  # Nếu không phải là tường
                actions.append(action_names[i])

        return actions

    def generatePacmanSuccessor(self, action):
        # Tạo trạng thái mới sau khi thực hiện hành động
        new_row, new_col = self.pacman_row, self.pacman_col

        if action == "LEFT":
            new_col -= 1
        elif action == "RIGHT":
            new_col += 1
        elif action == "UP":
            new_row -= 1
        elif action == "DOWN":
            new_row += 1

        # Kiểm tra nếu là vị trí hợp lệ
        if 0 <= new_row < self.N and 0 <= new_col < self.M and self.map[new_row][new_col] != 1:
            new_state = GameState(self.map, self.food_Position.copy(), new_row, new_col, self.N, self.M, self.Score)

            # Kiểm tra nếu ăn được thức ăn
            food_found = False
            for i, pos in enumerate(self.food_Position):
                if pos[0] == new_row and pos[1] == new_col:
                    new_state.food_Position.pop(i)
                    new_state.Score += 10  # Điểm cho việc ăn thức ăn
                    food_found = True
                    break

            return new_state

        return None

    def isWin(self):
        # Thắng nếu ăn hết thức ăn
        return len(self.food_Position) == 0

    def isLose(self):
        # Thua nếu bị ma bắt (cần triển khai logic phát hiện ma)
        # Đơn giản hóa: giả sử không có ma, không bao giờ thua
        return False

    def getScore(self):
        return self.Score


def backUp(node, score):
    while node.prev is not None:
        node.visitnumber += 1
        node.score += score
        node = node.prev
    node.visitnumber += 1  # Cập nhật cho nút gốc


def defaultPolicy(node, rootState):
    # Mô phỏng trò chơi từ trạng thái hiện tại
    nodeSet = []
    tempNode = node

    while tempNode.prev is not None:
        nodeSet.append(tempNode)
        tempNode = tempNode.prev

    nodeSet.reverse()
    tempState = rootState

    # Tái tạo trạng thái hiện tại
    for i in nodeSet:
        prevState = tempState
        tempState = tempState.generatePacmanSuccessor(i.prevaction)
        if tempState is None:
            backUp(i, gameEvaluation(rootState, prevState))
            return None
        if tempState.isWin():
            backUp(i, gameEvaluation(rootState, tempState))
            return None
        if tempState.isLose():
            backUp(i, gameEvaluation(rootState, tempState))
            return None

    # Mô phỏng một số bước ngẫu nhiên
    for j in range(5):  # Mô phỏng 5 bước
        if not (tempState.isWin() or tempState.isLose()):
            legal = tempState.getLegalPacmanActions()
            if not legal:
                break
            prevState = tempState
            tempState = tempState.generatePacmanSuccessor(random.choice(legal))
            if tempState is None:
                return None
        else:
            break

    return gameEvaluation(rootState, tempState)


def bestChild(node, exploration_weight=1.0):
    curr_max = -float('inf')
    best_children = []

    for child in node.childList:
        if child.visitnumber > 0:  # Tránh chia cho 0
            # UCB1 formula
            exploitation = child.score / child.visitnumber
            exploration = exploration_weight * math.sqrt((2 * math.log(node.visitnumber)) / child.visitnumber)
            value = exploitation + exploration

            if value > curr_max:
                curr_max = value
                best_children = [child]
            elif value == curr_max:
                best_children.append(child)

    if best_children:
        return random.choice(best_children)
    return None


def expansion(node, rootState):
    # Mở rộng node bằng cách thêm một node con mới
    nodeSet = []
    action_list = []
    tempNode = node

    while tempNode.prev is not None:
        nodeSet.append(tempNode)
        tempNode = tempNode.prev

    nodeSet.reverse()
    tempState = rootState

    # Tái tạo trạng thái hiện tại
    for i in nodeSet:
        prevState = tempState
        tempState = tempState.generatePacmanSuccessor(i.prevaction)
        if tempState is None:
            backUp(i, gameEvaluation(rootState, prevState))
            return None
        if tempState.isWin():
            backUp(i, gameEvaluation(rootState, tempState))
            return None
        if tempState.isLose():
            backUp(i, gameEvaluation(rootState, tempState))
            return None

    # Lấy danh sách hành động đã được thử
    for child in node.childList:
        action_list.append(child.prevaction)

    # Thêm một hành động mới
    legal_actions = tempState.getLegalPacmanActions()
    for action in legal_actions:
        if action not in action_list:
            child_node = node.createChild(action)

            if len(node.childList) == len(legal_actions):
                node.expanded = True

            return child_node

    # Nếu tất cả hành động đã được thử
    node.expanded = True
    return None


def treePolicy(root_node, root_state):
    node = root_node

    while True:
        if not node.expanded:
            return expansion(node, root_state)
        else:
            next_node = bestChild(node)
            if next_node is None:
                return node
            node = next_node


def MCTS(map, food_Position, start_row, start_col, N, M, iterations=100):
    # Khởi tạo trạng thái gốc
    root_state = GameState(map, food_Position, start_row, start_col, N, M)
    root_node = Node(None, None)
    root_node.visitnumber = 1  # Để tránh chia cho 0 trong UCB1

    # Chạy thuật toán MCTS
    for _ in range(iterations):
        expanded_node = treePolicy(root_node, root_state)
        if expanded_node is None:
            continue

        score = defaultPolicy(expanded_node, root_state)
        if score is not None:
            backUp(expanded_node, score)

    # Chọn hành động tốt nhất
    best_actions = []
    max_visits = -1

    for child in root_node.childList:
        if child.visitnumber > max_visits:
            max_visits = child.visitnumber
            best_actions = [child.prevaction]
        elif child.visitnumber == max_visits:
            best_actions.append(child.prevaction)

    if not best_actions:
        # Nếu không có hành động nào, chọn một hành động hợp lệ ngẫu nhiên
        legal_actions = root_state.getLegalPacmanActions()
        if legal_actions:
            return random.choice(legal_actions)
        return None

    # Trả về hành động tốt nhất
    return best_actions[random.randint(0, len(best_actions) - 1)]

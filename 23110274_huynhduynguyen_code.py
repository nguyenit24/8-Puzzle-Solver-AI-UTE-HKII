import pygame
import random
from collections import deque
import copy
import time
import heapq
import numpy as np
pygame.init()
WIDTH = 800
HEIGHT = 900
CELL_SIZE = 100
GRID = 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('8 Puzzle HDN')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
font = pygame.font.Font(None, 70)
font_small = pygame.font.Font(None, 30)
final_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
slider_width = 300
slider_height = 20
slider_x = (WIDTH - slider_width) // 2
slider_y = HEIGHT - 80
class Node:
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost
        self.cost = cost
    def get_index_0(self):
        for i in range(GRID):
            for j in range(GRID):
                if self.state[i][j] == 0:
                    return i, j
        return None
    def get_childstate(self):
        child_state = []
        x_0, y_0 = self.get_index_0()
        moves = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]
        for i, j, m in moves:
            new_i, new_j = x_0 + i, y_0 + j
            if 0 <= new_i < GRID and 0 <= new_j < GRID:
                new_state = copy.deepcopy(self.state)
                new_state[x_0][y_0], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[x_0][y_0]
                child_state.append(Node(new_state, self, m, self.cost + 1))
        return child_state
    def __eq__(self, other):
        return self.state == other.state
    def __hash__(self):
        return hash(str(self.state))
    def __lt__(self, other):
        return self.cost < other.cost
def heuristic(state):
    distance = 0
    for i in range(GRID):
        for j in range(GRID):
            value = state[i][j]
            if value != 0: 
                x, y = divmod(value - 1, GRID)  
                distance += abs(i - x) + abs(j - y)
    return distance
def bfs(state):
    start_time = time.perf_counter()
    start_node = Node(state)
    if start_node.state == final_state:
        return [start_node]
    visited = set()
    queue = deque([start_node])
    while queue:
        current_node = queue.popleft()
        visited.add(current_node)
        for child in current_node.get_childstate():
            if child not in visited:
                if child.state == final_state:
                    path = []
                    while child:
                        path.append(child)
                        child = child.parent
                    return path[::-1]
                queue.append(child)
    return None
def dfs(state):
    def extract_path(node):
        path = []
        while node:
            path.append(node)
            node = node.parent
        return path[::-1]
    stack = [Node(state)]
    visited = set([Node(state)])
    while stack:
        node = stack.pop()
        if node.state == final_state:
            return extract_path(node)
        for child in node.get_childstate():
            if child not in visited:
                visited.add(child)
                stack.append(child)
    return None
def depth_limited_search(node, depth, visited):
    if node.state == final_state:
        return [node]
    if depth <= 0:
        return None
    visited.add(node)
    for child in node.get_childstate():
        if child not in visited:
            result = depth_limited_search(child, depth - 1, visited)
            if result is not None:
                return [node] + result
    return None
def iddfs(state, max_depth=50):
    start_time = time.perf_counter()
    start_node = Node(state)
    if start_node.state == final_state:
        return [start_node]
    for depth in range(max_depth):
        visited = set()
        result = depth_limited_search(start_node, depth, visited)
        if result is not None:
            return result
    return None
def ucs(state):
    start_node = Node(state)
    if start_node.state == final_state:
        return [start_node]
    visited = set()
    priority_queue = [(0, id(start_node), start_node)]
    heapq.heapify(priority_queue)
    while priority_queue:
        total_cost, _, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node.state == final_state:
            path = []
            while current_node:
                path.append(current_node)
                current_node = current_node.parent
            print(f"UCS: Found solution with cost {total_cost}")
            return path[::-1]
        for child in current_node.get_childstate():
            if child not in visited:
                child_cost = total_cost + 1
                child.cost = child_cost 
                heapq.heappush(priority_queue, (child_cost, id(child), child))
    print("UCS: No solution found")
    return None
def greedy(state):
    start_time = time.perf_counter()
    start_node = Node(state)
    if start_node.state == final_state:
        return [start_node]
    visited = set()
    priority_queue = [(heuristic(start_node.state), id(start_node), start_node)]
    heapq.heapify(priority_queue)
    while priority_queue:
        _, _, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node.state == final_state:
            path = []
            while current_node:
                path.append(current_node)
                current_node = current_node.parent
            end_time = time.perf_counter()
            print(f"Greedy: Found solution, Time: {end_time - start_time:.4f}s")
            return path[::-1]
        for child in current_node.get_childstate():
            if child not in visited:
                h = heuristic(child.state)
                heapq.heappush(priority_queue, (h, id(child), child))
    print("Greedy: No solution found")
    return None
def hill_climbing(state):
    start_time = time.perf_counter()
    current_node = Node(state)
    if current_node.state == final_state:
        return [current_node]
    visited = set()
    path = [current_node]
    while True:
        visited.add(current_node)
        if current_node.state == final_state:
            end_time = time.perf_counter()
            print(f"Time: {end_time - start_time:.4f}s")
            return path
        children = current_node.get_childstate()
        current_h = heuristic(current_node.state)
        best_child = None
        best_h = current_h
        print(best_h)
        for child in children:
            if child not in visited:
                h = heuristic(child.state)
                if h < best_h: 
                    best_h = h
                    best_child = child
        if best_child is None:  
            break
        current_node = best_child
        path.append(current_node)
    end_time = time.perf_counter()
    print(f"Time: {end_time - start_time:.4f}s")
    return path
def him_climbing_simple(state):
    start_time = time.perf_counter()
    current_node = Node(state)
    if current_node.state == final_state:
        return [current_node]
    visited = set()
    path = [current_node]
    while True:
        visited.add(current_node)
        if current_node.state == final_state:
            end_time = time.perf_counter()
            print(f"Time: {end_time - start_time:.4f}s")
            return path
        children = current_node.get_childstate() 
        current_h = heuristic(current_node.state)
        for child in children:
            if child not in visited:
                h = heuristic(child.state)
                if h < current_h:  
                    current_node = child
                    path.append(current_node)
                    break
        end_time = time.perf_counter()
        print(f" Time: {end_time - start_time:.4f}s")
        return path
def stochastic_hill_climbing(state):
    start_time = time.perf_counter()
    current_node = Node(state)
    if current_node.state == final_state:
        return [current_node]
    visited = set()
    path = [current_node]
    while True:
        visited.add(current_node)
        children = current_node.get_childstate()
        if not children:
            break
        current_h = heuristic(current_node.state)
        better_children = [child for child in children if heuristic(child.state) > current_h]
        if not better_children:  
            break
        current_node = random.choice(better_children)
        path.append(current_node)
    end_time = time.perf_counter()
    print(f"Time: {end_time - start_time:.4f}s")
    return path
def random_state():
    numbers = list(range(9))
    random.shuffle(numbers)
    return [numbers[i:i+3] for i in range(0, 9, 3)]
def is_sol(state):
    flat = [num for row in state for num in row if num != 0]
    inversions = sum(1 for i in range(len(flat)) for j in range(i+1, len(flat)) if flat[i] > flat[j])
    return inversions % 2 == 0
def draw_state(states, is_belief=False):
    screen.fill(WHITE)
    if is_belief and isinstance(states, list):
        grid_width = GRID * CELL_SIZE
        spacing = 20
        total_width = grid_width * 2 + spacing
        start_x = (WIDTH - total_width) // 2
        start_y = 50
        belief_states = states[:2] if len(states) >= 2 else states + [[[0, 0, 0], [0, 0, 0], [0, 0, 0]] for _ in range(2 - len(states))]
        for idx, state in enumerate(belief_states):
            offset_x = start_x + idx * (grid_width + spacing)
            for i in range(GRID):
                for j in range(GRID):
                    num = state[i][j]
                    x = offset_x + j * CELL_SIZE
                    y = start_y + i * CELL_SIZE
                    if num != 0:
                        pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), border_radius=10)
                        text = font.render(str(num), True, BLACK)
                        text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                        screen.blit(text, text_rect)
                    else:
                        pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE), border_radius=10)
                    pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2, border_radius=10)
            label = font_small.render(f"State {idx + 1}", True, BLACK)
            screen.blit(label, (offset_x, start_y - 30))
    else:
        state = states
        if isinstance(states, list) and len(states) == 1:
            state = states[0]
        grid_width = GRID * CELL_SIZE
        start_x = (WIDTH - grid_width) // 2
        start_y = (HEIGHT - grid_width - 400) // 2
        for i in range(GRID):
            for j in range(GRID):
                num = state[i][j]
                x = start_x + j * CELL_SIZE
                y = start_y + i * CELL_SIZE
                if num != 0:
                    pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), border_radius=10)
                    text = font.render(str(num), True, BLACK)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE), border_radius=10)
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 2, border_radius=10)
def ida_star(state):
    start_time = time.perf_counter()
    start_node = Node(state)
    if start_node.state == final_state:
        return [start_node]
    def search(node, g_cost, threshold, visited, path):
        h_cost = heuristic(node.state)
        f_cost = g_cost + h_cost
        if f_cost > threshold:
            return None, f_cost
        if node.state == final_state:
            return [node], f_cost
        min_exceeded = float('inf')
        visited.add(node)
        path.append(node)
        for child in node.get_childstate():
            if child not in visited:
                child_g_cost = g_cost + 1
                child.cost = child_g_cost
                result, new_f = search(child, child_g_cost, threshold, visited, path)
                if result is not None:
                    return [node] + result, f_cost
                min_exceeded = min(min_exceeded, new_f)
        visited.remove(node)
        path.pop()
        return None, min_exceeded
    threshold = heuristic(start_node.state)
    while True:
        visited = set()
        path = []    
        result, new_threshold = search(start_node, 0, threshold, visited, path)
        if result is not None:
            end_time = time.perf_counter()
            print(f"IDA*: Tìm thấy giải pháp, Thời gian: {end_time - start_time:.4f}s, Chi phí: {len(result)-1}")
            return result
        if new_threshold == float('inf'):
            print("IDA*: Không tìm thấy giải pháp")
            return None
        threshold = new_threshold
def reconstruct_path(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]
def bfs_with_belief(initial_belief_set):
    start_time = time.perf_counter()
    belief_set = [Node(state) for state in initial_belief_set]
    initial_signature = tuple(tuple(tuple(row) for row in node.state) for node in belief_set)
    open_set = deque([(belief_set, [])])  
    closed_set = set()  
    path = []  
    while open_set:
        current_belief, current_path = open_set.popleft()
        belief_signature = tuple(tuple(tuple(row) for row in node.state) for node in current_belief)
        path.append([node.state for node in current_belief])
        if all(node.state == final_state for node in current_belief):
            end_time = time.perf_counter()
            print(f"BFS_Belief: Found solution, Time: {end_time - start_time:.4f}s")
            return path
        if belief_signature in closed_set:
            continue
        closed_set.add(belief_signature)
        for action in ["up", "down", "left", "right"]:
            new_belief = []
            for node in current_belief:
                x_0, y_0 = node.get_index_0()
                moves = {
                    "up": (-1, 0),
                    "down": (1, 0),
                    "left": (0, -1),
                    "right": (0, 1)
                }
                i, j = moves[action]
                new_i, new_j = x_0 + i, y_0 + j
                if 0 <= new_i < GRID and 0 <= new_j < GRID:
                    new_state = copy.deepcopy(node.state)
                    new_state[x_0][y_0], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[x_0][y_0]
                    flat_state = tuple(tuple(row) for row in new_state)
                    if flat_state not in [tuple(tuple(row) for row in n.state) for n in new_belief]:
                        new_belief.append(Node(new_state, node, action, node.cost + 1))
            if new_belief:
                open_set.append((new_belief, current_path + [new_belief]))
    print("BFS_Belief: No solution found")
    return path
def dfs_with_belief(initial_belief_set):
    start_time = time.perf_counter()
    belief_set = [Node(state) for state in initial_belief_set]
    stack = [(belief_set, [])]  
    closed_set = set()
    path = []
    while stack:
        current_belief, current_path = stack.pop()
        belief_signature = tuple(tuple(tuple(row) for row in node.state) for node in current_belief)
        path.append([node.state for node in current_belief])
        if all(node.state == final_state for node in current_belief):
            end_time = time.perf_counter()
            print(f"DFS_Belief: Found solution, Time: {end_time - start_time:.4f}s")
            return path
        if belief_signature in closed_set:
            continue
        closed_set.add(belief_signature)
        for action in ["up", "down", "left", "right"]:
            new_belief = []
            for node in current_belief:
                x_0, y_0 = node.get_index_0()
                moves = {
                    "up": (-1, 0),
                    "down": (1, 0),
                    "left": (0, -1),
                    "right": (0, 1)
                }
                i, j = moves[action]
                new_i, new_j = x_0 + i, y_0 + j
                if 0 <= new_i < GRID and 0 <= new_j < GRID:
                    new_state = copy.deepcopy(node.state)
                    new_state[x_0][y_0], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[x_0][y_0]
                    flat_state = tuple(tuple(row) for row in new_state)
                    if flat_state not in [tuple(tuple(row) for row in n.state) for n in new_belief]:
                        new_belief.append(Node(new_state, node, action, node.cost + 1))
            if new_belief:
                stack.append((new_belief, current_path + [new_belief]))
    print("DFS_Belief: No solution found")
    return path
def goalTest(state):
    return state == tuple(tuple(row) for row in final_state)
def actions(beliefState):
    return ["up", "down", "left", "right"]
def transitionModel(beliefState, action):
    next_states = set()
    for state in beliefState:
        state = [list(row) for row in state]
        x_0, y_0 = Node(state).get_index_0()
        moves = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }
        if action in moves:
            i, j = moves[action]
            new_i, new_j = x_0 + i, y_0 + j
            if 0 <= new_i < GRID and 0 <= new_j < GRID:
                new_state = copy.deepcopy(state)
                new_state[x_0][y_0], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[x_0][y_0]
                next_states.add(tuple(tuple(row) for row in new_state))
    return list(next_states)
def _canonical_belief_state(belief_state_list_of_physical_tuples):
    return tuple(sorted(belief_state_list_of_physical_tuples))
def _and_or_search_recursive(current_belief_state_tuples, goal_test_func, actions_func, transition_model_func, visited_canonical_path):
    if not current_belief_state_tuples:
        return "failure"
    if all(goal_test_func(physical_state_tuple) for physical_state_tuple in current_belief_state_tuples):
        return []
    current_canonical = _canonical_belief_state(current_belief_state_tuples)
    if current_canonical in visited_canonical_path:
        return "failure"
    for action in actions_func(current_belief_state_tuples):
        next_belief_state_tuples = transition_model_func(current_belief_state_tuples, action)
        if not next_belief_state_tuples:
            continue
        plan_segment = _and_or_search_recursive(
            next_belief_state_tuples,
            goal_test_func,
            actions_func,
            transition_model_func,
            visited_canonical_path + [current_canonical]
        )
        if plan_segment != "failure":
            return [action] + plan_segment
    return "failure"
def AND_OR_Search_Wrapper(initial_belief_list_of_lists, goal_test_func, actions_func, transition_model_func):
    initial_belief_tuples = [tuple(tuple(row) for row in state) for state in initial_belief_list_of_lists]
    return _and_or_search_recursive(initial_belief_tuples, goal_test_func, actions_func, transition_model_func, [])
def solve_8_puzzle_with_AND_OR(initial_belief_list_of_lists):
    plan = AND_OR_Search_Wrapper(initial_belief_list_of_lists, goalTest, actions, transitionModel)
    path_of_belief_states_for_display = [copy.deepcopy(initial_belief_list_of_lists)]
    if plan == "failure" or plan is None:
        print("AND-OR Search: No solution found.")
        return path_of_belief_states_for_display 
    if not plan: 
        print("AND-OR Search: Initial state is already a goal.")
        return path_of_belief_states_for_display
    print(f"AND-OR Search: Solution plan found: {plan}")
    current_belief_tuples = [tuple(tuple(row) for row in state) for state in initial_belief_list_of_lists]
    for action_step in plan:
        next_belief_tuples = transitionModel(current_belief_tuples, action_step)
        if not next_belief_tuples:
            print(f"AND-OR Search: Error during plan execution. Action '{action_step}' "
                  f"from a belief state led to an empty next belief state. Stopping path reconstruction.")
            return path_of_belief_states_for_display
        next_belief_list_of_lists = [[list(row) for row in state_tuple] for state_tuple in next_belief_tuples]
        path_of_belief_states_for_display.append(next_belief_list_of_lists)
        current_belief_tuples = next_belief_tuples
    return path_of_belief_states_for_display
initial_belief = [
    [[2, 8, 3], [1, 6, 4], [7, 0, 5]],
    [[2, 8, 3], [1, 6, 4], [0, 7, 5]]
]
def AND_OR_Search(beliefState, goalTest, actions, transitionModel):
    beliefState = [tuple(tuple(row) for row in state) for state in beliefState]
    initial_state = beliefState[0]
    plan = OR_Search([initial_state], [], goalTest, actions, transitionModel)
    return plan
def OR_Search(beliefState, path, goalTest, actions, transitionModel):
    if all(goalTest(state) for state in beliefState):
        return []
    if beliefState in path:
        return "failure"
    for action in actions(beliefState):
        outcomeStates = transitionModel(beliefState, action)
        plan = AND_Search(outcomeStates, path + [beliefState], goalTest, actions, transitionModel)
        if plan != "failure":
            return [action] + plan  
    return "failure"
def AND_Search(outcomeStates, path, goalTest, actions, transitionModel):
    if not outcomeStates:
        return "failure"
    state = outcomeStates[0]  
    plan = OR_Search([state], path, goalTest, actions, transitionModel)
    if plan == "failure":
        return "failure"
    return plan  
def solve_8_puzzle_with_AND_OR(initial_belief):
    plan = AND_OR_Search(initial_belief, goalTest, actions, transitionModel)
    if plan == "failure":
        return None
    current_state = [list(row) for row in initial_belief[0]] 
    path = [current_state]  
    def execute_plan(plan, current_state):
        if not plan:
            return []
        action = plan[0]
        if len(plan) == 1: 
            return []
        x_0, y_0 = Node(current_state).get_index_0()
        new_state = copy.deepcopy(current_state)
        if action == "up":
            new_state[x_0][y_0], new_state[x_0-1][y_0] = new_state[x_0-1][y_0], new_state[x_0][y_0]
        elif action == "down":
            new_state[x_0][y_0], new_state[x_0+1][y_0] = new_state[x_0+1][y_0], new_state[x_0][y_0]
        elif action == "left":
            new_state[x_0][y_0], new_state[x_0][y_0-1] = new_state[x_0][y_0-1], new_state[x_0][y_0]
        elif action == "right":
            new_state[x_0][y_0], new_state[x_0][y_0+1] = new_state[x_0][y_0+1], new_state[x_0][y_0]
        return [new_state] + execute_plan(plan[1:], new_state)
    path.extend(execute_plan(plan, current_state))
    return path
initial_belief = [
    [[2, 8, 3], [1, 6, 4], [7, 0, 5]],
    [[2, 8, 3], [1, 6, 4], [0, 7, 5]]
]
def draw_slider(speed):
    pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_width, slider_height), border_radius=10)
    slider_pos = slider_x + int(slider_width * speed / 1000)
    pygame.draw.circle(screen, BLACK, (slider_pos, slider_y + slider_height // 2), 10)
    speed_text = font_small.render(f"Speed: {speed}ms", True, BLACK)
    screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, slider_y + slider_height + 10))
def Astar(state):
    start_node = Node(state)
    if start_node.state == final_state:
        return [start_node]
    visited = set()
    priority_queue = [(heuristic(start_node.state), 0, id(start_node), start_node)]
    heapq.heapify(priority_queue)
    while priority_queue:
        f_cost, g_cost, _, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node.state == final_state:
            path = []
            while current_node:
                path.append(current_node)
                current_node = current_node.parent
            return path[::-1]
        for child in current_node.get_childstate():
            if child not in visited:
                child_g_cost = g_cost + 1
                child_h_cost = heuristic(child.state)
                child_f_cost = child_g_cost + child_h_cost
                child.cost = child_g_cost 
                heapq.heappush(priority_queue, (child_f_cost, child_g_cost, id(child), child))
    print("A*: No solution found")
    return None
import math
def simulated_annealing(state):
    start_time = time.perf_counter()
    current_node = Node(state)
    if current_node.state == final_state:
        return [current_node]
    path = [current_node]
    T = 1000000
    alpha = 0.9995  
    min_temp = 0.0001  
    while T > min_temp:
        if current_node.state == final_state:
            end_time = time.perf_counter()
            print(f"Simulated Annealing: Found solution, Time: {end_time - start_time:.4f}s")
            return path
        children = current_node.get_childstate()
        if not children:
            break
        next_node = random.choice(children)
        current_h = heuristic(current_node.state)
        next_h = heuristic(next_node.state)
        delta_h = current_h - next_h 
        print(delta_h)
        if delta_h > 0 or math.exp(delta_h / T) > random.random():
            current_node = next_node
            path.append(current_node)
        T *= alpha
    end_time = time.perf_counter()
    print(f"Simulated Annealing: No solution found, Time: {end_time - start_time:.4f}s")
    return path
import heapq
import time
def bfs_for_path(start_state, target_state):
    start_node = Node(start_state)
    if start_node.state == target_state:
        return [start_node]
    visited = set()
    queue = deque([start_node])
    while queue:
        current_node = queue.popleft()
        visited.add(current_node)
        for child in current_node.get_childstate():
            if child not in visited:
                if child.state == target_state:
                    path = []
                    while child:
                        path.append(child)
                        child = child.parent
                    return path[::-1]
                queue.append(child)
    return [Node(start_state)]  
def genetic_algorithm(state, population_size=100, generations=2000):
    start_time = time.perf_counter()
    population = [random_state() for _ in range(population_size)]
    population[0] = copy.deepcopy(state)  
    def fitness(state):
        return -heuristic(state)
    def crossover(parent1, parent2):
        flat1 = [num for row in parent1 for num in row]
        flat2 = [num for row in parent2 for num in row]
        size = len(flat1)
        start, end = sorted([random.randint(0, size-1) for _ in range(2)])
        child = [None] * size
        child[start:end+1] = flat1[start:end+1]
        pos = 0
        for i in range(size):
            if start <= i <= end:
                continue
            while flat2[pos] in child[start:end+1]:
                pos += 1
            child[i] = flat2[pos]
            pos += 1
        return [child[i:i+3] for i in range(0, 9, 3)]
    def mutate(state):
        flat = [num for row in state for num in row]
        zero_idx = flat.index(0)
        possible_moves = []
        if zero_idx % 3 > 0: possible_moves.append(zero_idx - 1)  
        if zero_idx % 3 < 2: possible_moves.append(zero_idx + 1)  
        if zero_idx >= 3: possible_moves.append(zero_idx - 3)    
        if zero_idx < 6: possible_moves.append(zero_idx + 3)   
        if possible_moves:
            swap_idx = random.choice(possible_moves)
            flat[zero_idx], flat[swap_idx] = flat[swap_idx], flat[zero_idx]
        return [flat[i:i+3] for i in range(0, 9, 3)]
    final_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  
    best_state = copy.deepcopy(state)
    best_fitness = fitness(best_state)
    for generation in range(generations):
        population.sort(key=fitness, reverse=True)
        current_best = population[0]
        current_fitness = fitness(current_best)
        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_state = copy.deepcopy(current_best)
        if current_best == final_state:
            end_time = time.perf_counter()
            print(f"Genetic Algorithm: Found solution in generation {generation}, Time: {end_time - start_time:.4f}s")
            return bfs_for_path(state, final_state)
        next_generation = population[:population_size // 2] 
        while len(next_generation) < population_size:
            parent1, parent2 = random.choices(population[:population_size // 4], k=2)
            child = crossover(parent1, parent2)
            if random.random() < 0.1:  
                child = mutate(child)
            next_generation.append(child)
        population = next_generation
    end_time = time.perf_counter()
    print(f"Genetic Algorithm: No solution found after {generations} generations, Time: {end_time - start_time:.4f}s")
    return bfs_for_path(state, best_state)  
import heapq
import time
def beam_search(state, beam_width=3):
    start_time = time.perf_counter()
    start_node = Node(state)
    if start_node.state == final_state:
        return [start_node]
    beam = [(heuristic(start_node.state),start_node)]
    visited = set()  
    while beam:
        next_beam = []
        for _ in range(min(len(beam), beam_width)):
            if not beam:
                break
            h, current_node = heapq.heappop(beam)
            if current_node.state == final_state:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = current_node.parent
                end_time = time.perf_counter()
                print(f"Beam Search: Found solution, Time: {end_time - start_time:.4f}s, Steps: {len(path)-1}")
                return path[::-1]
            if current_node not in visited:
                visited.add(current_node)
                children = current_node.get_childstate()
                for child in children:
                    if child not in visited:
                        h_child = heuristic(child.state)
                        heapq.heappush(next_beam, (h_child, child))
        beam = []
        for _ in range(min(len(next_beam), beam_width)):
            if next_beam:
                beam.append(heapq.heappop(next_beam))
    end_time = time.perf_counter()
    print(f"Beam Search: No solution found, Time: {end_time - start_time:.4f}s")
    return None
def backtracking_fill_puzzle(state, index=0, user=None, path=None):
    if user is None:
        user = [False] * 9
    if path is None:
        path = []
    if index == 9:
        if state == final_state:
            return path
        return None

    row = index // 3
    col = index % 3 #
    for num in range(1, 9):
        if not user[num]:
            user[num] = True
            new_state = copy.deepcopy(state)
            new_state[row][col] = num
            new_node = Node(new_state, path[-1] if path else None)
            path.append(new_node)
            result = backtracking_fill_puzzle(new_state, index + 1, user, path)
            if result is not None:
                return result
            user[num] = False
            path.pop()

    if index == 8:
        new_state = copy.deepcopy(state)
        new_state[row][col] = 0
        new_node = Node(new_state, path[-1] if path else None)
        path.append(new_node)
    
        if new_state == final_state:
            return path
  
        path.pop()
    return None
import pickle
import os
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.3
Q_table = {}
Q_TABLE_FILE = "q_table.pkl"
def get_state_key(state):
    return tuple(tuple(row) for row in state)
def get_possible_actions(state):
    x_0, y_0 = Node(state).get_index_0()
    actions = []
    if x_0 > 0: actions.append("up")
    if x_0 < GRID - 1: actions.append("down")
    if y_0 > 0: actions.append("left")
    if y_0 < GRID - 1: actions.append("right")
    return actions
def take_action(state, action):
    x_0, y_0 = Node(state).get_index_0()
    moves = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }
    i, j = moves[action]
    new_i, new_j = x_0 + i, y_0 + j
    new_state = copy.deepcopy(state)
    new_state[x_0][y_0], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[x_0][y_0]
    return new_state
def reward_function(state):
    if state == final_state:
        return 100
    return -1 - heuristic(state) / 10
def perturb_state(state, steps=1):
    current_state = copy.deepcopy(state)
    for _ in range(steps):
        actions = get_possible_actions(current_state)
        if not actions:
            break
        action = random.choice(actions)
        current_state = take_action(current_state, action)
    return current_state
def save_q_table():
    with open(Q_TABLE_FILE, 'wb') as f:
        pickle.dump(Q_table, f)
    print(f"Q-Learning: Q-table đã được lưu vào {Q_TABLE_FILE}")
def load_q_table():
    global Q_table
    if os.path.exists(Q_TABLE_FILE):
        with open(Q_TABLE_FILE, 'rb') as f:
            Q_table = pickle.load(f)
        print(f"Q-Learning: Q-table đã được tải từ {Q_TABLE_FILE}, kích thước: {len(Q_table)}")
        return True
    return False
def train_q_learning(initial_state, episodes=2000, max_steps=200):
    global Q_table
    start_time = time.perf_counter()
    if load_q_table():
        print("Q-Learning: Sử dụng Q-table đã lưu, bỏ qua huấn luyện")
        return
    Q_table = {}
    for episode in range(episodes):
        if random.random() < 0.5:
            current_state = copy.deepcopy(initial_state)
        else:
            current_state = perturb_state(initial_state, steps=random.randint(1, 5))
        steps = 0
        while steps < max_steps:
            state_key = get_state_key(current_state)
            if state_key not in Q_table:
                Q_table[state_key] = {action: 0 for action in get_possible_actions(current_state)}
            if random.random() < EPSILON:
                action = random.choice(get_possible_actions(current_state))
            else:
                action = max(Q_table[state_key], key=Q_table[state_key].get)
            new_state = take_action(current_state, action)
            reward = reward_function(new_state)
            new_state_key = get_state_key(new_state)
            if new_state_key not in Q_table:
                Q_table[new_state_key] = {action: 0 for action in get_possible_actions(new_state)}
            best_next_action = max(Q_table[new_state_key], key=Q_table[new_state_key].get)
            Q_table[state_key][action] += ALPHA * (
                reward + GAMMA * Q_table[new_state_key][best_next_action] - Q_table[state_key][action]
            )
            current_state = new_state
            steps += 1
            if current_state == final_state:
                break
        if (episode + 1) % 100 == 0:
            print(f"Q-Learning: Hoàn thành {episode + 1}/{episodes} episode, kích thước Q-table: {len(Q_table)}")
    end_time = time.perf_counter()
    print(f"Q-Learning: Huấn luyện hoàn tất, Thời gian: {end_time - start_time:.4f}s, Kích thước Q-table: {len(Q_table)}")
    save_q_table()
def q_learning(state, episodes=2000, max_steps=200):
    start_time = time.perf_counter()
    if not Q_table and not load_q_table():
        print("Q-Learning: Huấn luyện Q-table...")
        train_q_learning(state, episodes, max_steps)
    solution = []
    current_state = copy.deepcopy(state)
    visited = set()
    steps = 0
    state_key = get_state_key(current_state)
    if state_key not in Q_table:
        Q_table[state_key] = {action: 0 for action in get_possible_actions(current_state)}
    while current_state != final_state and steps < max_steps:
        state_key = get_state_key(current_state)
        visited.add(state_key)
        actions = get_possible_actions(current_state)
        if not actions:
            print("Q-Learning: Không có hành động hợp lệ")
            break
        action = max(Q_table[state_key], key=Q_table[state_key].get)
        new_state = take_action(current_state, action)
        new_state_key = get_state_key(new_state)
        if new_state_key not in Q_table:
            Q_table[new_state_key] = {action: 0 for action in get_possible_actions(new_state)}
        if new_state_key in visited:
            print("Q-Learning: Phát hiện vòng lặp, thử hành động khác")
            alternative_actions = [a for a in actions if a != action]
            if not alternative_actions:
                print("Q-Learning: Không có hành động thay thế, dừng lại")
                break
            action = random.choice(alternative_actions)
            new_state = take_action(current_state, action)
            new_state_key = get_state_key(new_state)
            if new_state_key not in Q_table:
                Q_table[new_state_key] = {action: 0 for action in get_possible_actions(new_state)}
        solution.append(Node(current_state))
        current_state = new_state
        steps += 1
    if current_state == final_state:
        solution.append(Node(current_state))
        end_time = time.perf_counter()
        print(f"Q-Learning: Tìm thấy giải pháp, Thời gian: {end_time - start_time:.4f}s, Số bước: {len(solution)-1}")
    else:
        solution.append(Node(current_state))
        end_time = time.perf_counter()
        print(f"Q-Learning: Không tìm thấy giải pháp, Thời gian: {end_time - start_time:.4f}s, Số bước: {len(solution)-1}")
    return solution
def forward_checking(state, domain, index):
    row = index // 3
    col = index % 3
    for i in range(3):
        if state[row][i] in domain[row][col]:
            domain[row][col].remove(state[row][i])
        if state[i][col] in domain[row][col]:
            domain[row][col].remove(state[i][col])
def min_conflicts(state, max_steps=1000):
    start_time = time.perf_counter()
    current_state = copy.deepcopy(state)
    path = [Node(current_state)]
    if all(current_state[i][j] == 0 for i in range(3) for j in range(3)):
        numbers = list(range(9))
        random.shuffle(numbers)
        current_state = [numbers[i:i+3] for i in range(0, 9, 3)]
        path = [Node(current_state)]
    def get_conflicts(state, row, col, value):
        conflicts = 0
        for i in range(3):
            if i != col and state[row][i] == value:
                conflicts += 1
            if i != row and state[i][col] == value:
                conflicts += 1
        return conflicts
    for _ in range(max_steps):
        if current_state == final_state:
            end_time = time.perf_counter()
            print(f"Min-Conflicts: Found solution, Time: {end_time - start_time:.4f}s")
            return path
        conflicted = []
        for i in range(3):
            for j in range(3):
                if current_state[i][j] != 0 and get_conflicts(current_state, i, j, current_state[i][j]) > 0:
                    conflicted.append((i, j))
        if not conflicted:
            conflicted = [(i, j) for i in range(3) for j in range(3) if current_state[i][j] != final_state[i][j] and current_state[i][j] != 0]
        if not conflicted:
            break
        row, col = random.choice(conflicted)
        current_val = current_state[row][col]
        min_conflict_val = current_val
        min_conflicts = get_conflicts(current_state, row, col, current_val)
        possible_values = [v for v in range(1, 9) if v != current_val and v not in [current_state[row][k] for k in range(3)] and v not in [current_state[k][col] for k in range(3)]]
        for val in possible_values:
            conflicts = get_conflicts(current_state, row, col, val)
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                min_conflict_val = val
        new_state = copy.deepcopy(current_state)
        new_state[row][col] = min_conflict_val
        current_state = new_state
        path.append(Node(current_state, path[-1] if path else None))
    end_time = time.perf_counter()
    print(f"Min-Conflicts: No solution found, Time: {end_time - start_time:.4f}s")
    return path
def backtracking_with_forward_checking(state, index=0, user=None, path=None):
    start_time = time.perf_counter()
    if user is None:
        user = [False] * 9
    if path is None:
        path = []
    if index == 9:
        if state == final_state:
            end_time = time.perf_counter()
            print(f"Backtracking with Forward Checking: Found solution, Time: {end_time - start_time:.4f}s")
            return path
        return None
    row = index // 3
    col = index % 3
    domain = [num for num in range(1, 9) if not user[num]]
    for i in range(3):
        if state[row][i] in domain:
            domain.remove(state[row][i])
        if state[i][col] in domain:
            domain.remove(state[i][col])
    for num in domain:
        user[num] = True
        new_state = copy.deepcopy(state)
        new_state[row][col] = num
        new_node = Node(new_state, path[-1] if path else None)
        path.append(new_node)
        result = backtracking_with_forward_checking(new_state, index + 1, user, path)
        if result is not None:
            return result
        user[num] = False
        path.pop()
    if index == 8:
        new_state = copy.deepcopy(state)
        new_state[row][col] = 0
        new_node = Node(new_state, path[-1] if path else None)
        path.append(new_node)
        if new_state == final_state:
            end_time = time.perf_counter()
            print(f"Backtracking with Forward Checking: Found solution, Time: {end_time - start_time:.4f}s")
            return path
        path.pop()
    return None
def search_with_partial_observation(initial_belief, actions, transition_model, goal_test):
    start_time = time.perf_counter()
    belief_state = [tuple(tuple(row) for row in state) for state in initial_belief]
    open_set = deque([(belief_state, [])])
    closed_set = set()
    path = []
    while open_set:
        current_belief, current_path = open_set.popleft()
        path.append([[list(row) for row in state] for state in current_belief])
        if all(goal_test(state) for state in current_belief):
            end_time = time.perf_counter()
            print(f"Partial Observation: Found solution, Time: {end_time - start_time:.4f}s")
            return path
        belief_signature = tuple(current_belief)
        if belief_signature in closed_set:
            continue
        closed_set.add(belief_signature)
        for action in actions(current_belief):
            new_belief = transition_model(current_belief, action)
            if new_belief:
                open_set.append((new_belief, current_path + [new_belief]))
    print("Partial Observation: No solution found")
    return path
def draw_buttons(selected_algo):
    buttons = [
        ("Reset", RED, (20, 450, 120, 40), selected_algo == "Reset"),
        ("Random", GREEN, (150, 450, 120, 40), selected_algo == "Random"),
        ("Run", BLACK, (WIDTH - 140, 450, 120, 40), selected_algo == "Run"),
        ("BFS", BLUE, (20, 500, 80, 40), selected_algo == "BFS"),
        ("DFS", BLUE, (110, 500, 80, 40), selected_algo == "DFS"),
        ("IDDFS", BLUE, (200, 500, 80, 40), selected_algo == "IDDFS"),
        ("UCS", BLUE, (290, 500, 80, 40), selected_algo == "UCS"),
        ("Greedy", BLUE, (20, 550, 80, 40), selected_algo == "Greedy"),
        ("A*", BLUE, (110, 550, 80, 40), selected_algo == "A*"),
        ("IDA*", BLUE, (200, 550, 80, 40), selected_algo == "IDA*"),
        ("Hill", BLUE, (290, 550, 80, 40), selected_algo == "Hill"),
        ("Hill_Simple", BLUE, (20, 600, 120, 40), selected_algo == "Hill_Simple"),
        ("stochastic_hill", BLUE, (150, 600, 120, 40), selected_algo == "stochastic_hill"),
        ("simulated", BLUE, (280, 600, 120, 40), selected_algo == "simulated"),
        ("beam", BLUE, (410, 600, 80, 40), selected_algo == "beam"),
        ("Genetic", BLUE, (20, 650, 120, 40), selected_algo == "Genetic"),
        ("BFS_Belief", BLUE, (150, 650, 120, 40), selected_algo == "BFS_Belief"),
        ("DFS_Belief", BLUE, (280, 650, 120, 40), selected_algo == "DFS_Belief"),
        ("Backtracking", BLUE, (20, 700, 120, 40), selected_algo == "Backtracking"),
        ("Backtracking_FC", BLUE, (150, 700, 120, 40), selected_algo == "Backtracking_FC"),
        ("Min_Conflicts", BLUE, (280, 700, 120, 40), selected_algo == "Min_Conflicts"),
        ("Partial_Obs", BLUE, (410, 700, 120, 40), selected_algo == "Partial_Obs"),
        ("Q-Learning", BLUE, (20, 750, 120, 40), selected_algo == "Q-Learning"),
        ("AND_OR", BLUE, (150, 750, 120, 40), selected_algo == "AND_OR"),
    ]
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for text, color, rect, selected in buttons:
        is_hovered = rect[0] <= mouse_x <= rect[0] + rect[2] and rect[1] <= mouse_y <= rect[1] + rect[3]
        button_color = GREEN if selected else (color if not is_hovered else (200, 200, 200))
        pygame.draw.rect(screen, button_color, rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, rect, width=2, border_radius=10)
        btn_text = font_small.render(text, True, WHITE)
        btn_rect = btn_text.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
        screen.blit(btn_text, btn_rect)
import csv
import os
def main():
    current_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
    running = True
    solution = None
    step = 0
    selected_algo = "Greedy"
    speed = 500
    dragging = False
    execution_time = 0
    belief_states = None
    belief_algorithms = ["BFS_Belief", "DFS_Belief", "Partial_Obs", "AND_OR"]
    buttons = [
        ("Reset", RED, (20, 450, 120, 40)),
        ("Random", GREEN, (150, 450, 120, 40)),
        ("Run", BLACK, (WIDTH - 140, 450, 120, 40)),
        ("BFS", BLUE, (20, 500, 80, 40)),
        ("DFS", BLUE, (110, 500, 80, 40)),
        ("IDDFS", BLUE, (200, 500, 80, 40)),
        ("UCS", BLUE, (290, 500, 80, 40)),
        ("Greedy", BLUE, (20, 550, 80, 40)),
        ("A*", BLUE, (110, 550, 80, 40)),
        ("IDA*", BLUE, (200, 550, 80, 40)),
        ("Hill", BLUE, (290, 550, 80, 40)),
        ("Hill_Simple", BLUE, (20, 600, 120, 40)),
        ("stochastic_hill", BLUE, (150, 600, 120, 40)),
        ("simulated", BLUE, (280, 600, 120, 40)),
        ("beam", BLUE, (410, 600, 80, 40)),
        ("Genetic", BLUE, (20, 650, 120, 40)),
        ("BFS_Belief", BLUE, (150, 650, 120, 40)),
        ("DFS_Belief", BLUE, (280, 650, 120, 40)),
        ("Backtracking", BLUE, (20, 700, 120, 40)),
        ("Backtracking_FC", BLUE, (150, 700, 120, 40)),
        ("Min_Conflicts", BLUE, (280, 700, 120, 40)),
        ("Partial_Obs", BLUE, (410, 700, 120, 40)),
        ("Q-Learning", BLUE, (20, 750, 120, 40)),
        ("AND_OR", BLUE, (150, 750, 120, 40)),
    ]

    # Khởi tạo file CSV với tiêu đề nếu chưa tồn tại
    csv_file = "execution_times.csv"
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithm", "Execution_Time", "Steps"])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for btn_text, _, (btn_x, btn_y, btn_w, btn_h) in buttons:
                    if btn_x <= x <= btn_x + btn_w and btn_y <= y <= btn_y + btn_h:
                        if btn_text == "Reset":
                            current_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
                            solution = None
                            step = 0
                            belief_states = None
                        elif btn_text == "Random":
                            while True:
                                current_state = random_state()
                                if is_sol(current_state):
                                    break
                            solution = None
                            step = 0
                            belief_states = None
                        elif btn_text == "Run":
                            if not selected_algo:
                                print("Vui lòng chọn thuật toán trước khi chạy!")
                                continue
                            print(f"Chạy thuật toán: {selected_algo}")
                            start_time = time.perf_counter()
                            belief_states = None
                            solution = None
                            steps = 0
                            if selected_algo == "BFS":
                                solution = bfs(current_state)
                            elif selected_algo == "DFS":
                                solution = dfs(current_state)
                            elif selected_algo == "IDDFS":
                                solution = iddfs(current_state)
                            elif selected_algo == "UCS":
                                solution = ucs(current_state)
                            elif selected_algo == "A*":
                                solution = Astar(current_state)
                            elif selected_algo == "IDA*":
                                solution = ida_star(current_state)
                            elif selected_algo == "Hill":
                                solution = hill_climbing(current_state)
                            elif selected_algo == "Hill_Simple":
                                solution = him_climbing_simple(current_state)
                            elif selected_algo == "stochastic_hill":
                                solution = stochastic_hill_climbing(current_state)
                            elif selected_algo == "simulated":
                                solution = simulated_annealing(current_state)
                            elif selected_algo == "beam":
                                solution = beam_search(current_state, 2)
                            elif selected_algo == "Genetic":
                                solution = genetic_algorithm(current_state)
                            elif selected_algo == "Backtracking_FC":
                                current_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                                solution = backtracking_with_forward_checking(current_state)
                                if solution:
                                    print("Backtracking với Forward Checking: Đã giải được bài toán")
                                else:
                                    print("Backtracking với Forward Checking: Không tìm được lời giải")
                            elif selected_algo == "Partial_Obs":
                                initial_belief = [
                                    [[2, 8, 3], [1, 6, 4], [7, 0, 5]],
                                    [[2, 8, 3], [1, 6, 4], [0, 7, 5]]
                                ]
                                solution = search_with_partial_observation(initial_belief, actions, transitionModel, goalTest)
                                if solution:
                                    print("Tìm kiếm với Quan sát Một phần: Đã tìm được lời giải")
                                    belief_states = initial_belief
                                else:
                                    print("Tìm kiếm với Quan sát Một phần: Không tìm được lời giải")
                                    solution = [initial_belief]
                            elif selected_algo == "BFS_Belief":
                                initial_belief = [
                                    [[1, 2, 3], [4, 0, 5], [6, 7, 8]],
                                    [[1, 2, 3], [4, 5, 0], [6, 7, 8]]
                                ]
                                solution = bfs_with_belief(initial_belief)
                                belief_states = initial_belief
                                if not solution:
                                    solution = [initial_belief]
                            elif selected_algo == "DFS_Belief":
                                initial_belief = [
                                    [[1, 2, 3], [4, 0, 5], [6, 7, 8]],
                                    [[1, 2, 3], [4, 5, 0], [6, 7, 8]]
                                ]
                                solution = dfs_with_belief(initial_belief)
                                belief_states = initial_belief
                                if not solution:
                                    solution = [initial_belief]
                            elif selected_algo == "AND_OR":
                                initial_belief = [
                                    [[2, 8, 3], [1, 6, 4], [7, 0, 5]],
                                    [[2, 8, 3], [1, 6, 4], [0, 7, 5]]
                                ]
                                solution = solve_8_puzzle_with_AND_OR(initial_belief)
                                belief_states = initial_belief
                                if solution:
                                    print("Tìm kiếm AND-OR: Đã tìm được lời giải")
                                else:
                                    print("Tìm kiếm AND-OR: Không tìm được lời giải")
                                    solution = [initial_belief]
                            elif selected_algo == "Q-Learning":
                                solution = q_learning(current_state, episodes=1000, max_steps=10000)
                            elif selected_algo == "Backtracking":
                                current_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                                solution = backtracking_fill_puzzle(current_state, 0, [False] * 9, [])
                                if solution:
                                    print("Backtracking: Đã điền bài toán thành công")
                                else:
                                    print("Backtracking: Không điền được bài toán")
                            elif selected_algo == "Min_Conflicts":
                                current_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                                solution = min_conflicts(current_state)
                                if solution:
                                    print("Min-Conflicts: Đã tìm được lời giải")
                                else:
                                    print("Min-Conflicts: Không tìm được lời giải")
                            elif selected_algo == "Greedy":
                                solution = greedy(current_state)
                            else:
                                print(f"Thuật toán không xác định: {selected_algo}")
                                continue
                            end_time = time.perf_counter()
                            execution_time = end_time - start_time
                            # Tính số bước
                            if solution:
                                steps = len(solution) - 1 if len(solution) > 1 else 0
                            else:
                                steps = 0
                            # Ghi vào file CSV
                            with open(csv_file, mode='a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([selected_algo, execution_time, steps])
                            print(f"Đã lưu {selected_algo} - Thời gian: {execution_time:.4f}s, Số bước: {steps}")
                            step = 0
                        else:
                            selected_algo = btn_text
                            print(f"Đã chọn thuật toán: {selected_algo}")
                        break
                    elif slider_x <= x <= slider_x + slider_width and slider_y <= y <= slider_y + slider_height:
                        dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                x = max(slider_x, min(slider_x + slider_width, event.pos[0]))
                speed = int((x - slider_x) / slider_width * 1000)
        if selected_algo in belief_algorithms and belief_states:
            print(f"Hiển thị belief states tại bước {step}: {belief_states}")
            draw_state(belief_states, is_belief=True)
        else:
            draw_state(current_state, is_belief=False)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for text, color, rect in buttons:
            is_hovered = rect[0] <= mouse_x <= rect[0] + rect[2] and rect[1] <= mouse_y <= rect[1] + rect[3]
            button_color = GREEN if text == selected_algo else (color if not is_hovered else (200, 200, 200))
            pygame.draw.rect(screen, button_color, rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, rect, width=2, border_radius=10)
            btn_text = font_small.render(text, True, WHITE)
            btn_rect = btn_text.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
            screen.blit(btn_text, btn_rect)
        draw_slider(speed)
        if solution and step < len(solution):
            if selected_algo in belief_algorithms:
                belief_states = solution[step]
                print(f"Bước {step}: {belief_states}")
            else:
                current_state = solution[step].state
                print(f"Bước {step}: {current_state}")
            step += 1
            pygame.time.wait(speed)
        if solution:
            time_text = font_small.render(f"{execution_time:.6f}s", True, BLACK)
            screen.blit(time_text, (WIDTH//2 + 120, HEIGHT - time_text.get_height() - 30))
        text_step = font.render(str(step), True, BLACK)
        screen.blit(text_step, (WIDTH//2 - text_step.get_width()//2, HEIGHT - text_step.get_height() - 10))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()

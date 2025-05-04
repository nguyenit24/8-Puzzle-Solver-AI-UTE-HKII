import pygame
import random
from collections import deque
import copy
import time
import heapq
import numpy as np

pygame.init()
WIDTH = 700
HEIGHT = 900
CELL_SIZE = 120
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
                
                if h < current_h:  #
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

def draw_state(state):
    """Draw the puzzle state with improved UI."""
    screen.fill(WHITE)

    # Calculate the total grid size
    grid_width = GRID * CELL_SIZE

    # Calculate the starting position to center the grid horizontally
    start_x = (WIDTH - grid_width) // 2

    for i in range(GRID):
        for j in range(GRID):
            num = state[i][j]
            x = start_x + j * CELL_SIZE
            y = i * CELL_SIZE

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
def bfs_with_belief(initialBelief_set):
    start_time = time.perf_counter()
    belief_set = [Node(state) for state in initialBelief_set]
    open_set = deque([belief_set])
    closed_set = set()

    while open_set:
        current_belief = open_set.popleft()
        if all(node.state == final_state for node in current_belief):
            end_time = time.perf_counter()
            print(f"BFS_Belief: Found solution, Time: {end_time - start_time:.4f}s")
            return reconstruct_path(current_belief[0])
        belief_signature = tuple(tuple(tuple(row) for row in node.state) for node in current_belief)
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
                    if flat_state not in [tuple(tuple(row) for row in n.state) for n in current_belief]:
                        new_belief.append(Node(new_state,node,action,node.cost+1))
            if len(new_belief) > 0:
                open_set.append(new_belief)

    print("BFS_Belief: No solution found")
    return None    

def dfs_with_belief(initialBelief_set):
    start_time = time.perf_counter()
    belief_set = [Node(state) for state in initialBelief_set]
    stack = [belief_set]
    closed_set = set()

    while stack:
        current_belief = stack.pop()
        if all(node.state == final_state for node in current_belief):
            end_time = time.perf_counter()
            print(f"DFS_Belief: Found solution, Time: {end_time - start_time:.4f}s")
            return reconstruct_path(current_belief[0])
        belief_signature = tuple(tuple(tuple(row) for row in node.state) for node in current_belief)
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
                    if flat_state not in [tuple(tuple(row) for row in n.state) for n in current_belief]:
                        new_belief.append(Node(new_state,node,action,node.cost+1))
            if len(new_belief) > 0:
                stack.append(new_belief)

    print("DFS_Belief: No solution found")
    return None
def bfs_with_Conformant_Belief(B,G):
    start_time = time.perf_counter()
    belief_set = [Node(n1) for n1 in B]
    open_set = deque(belief_set[0])
    initailG = [Node(n2) for n2 in G]
    closed_set = set()
    while open_set :
        current_belief = open_set.popleft()
        if all(current_belief.state == node.state for node in initailG):
            end_time = time.perf_counter()
            print(f"BFS_Belief: Found solution, Time: {end_time - start_time:.4f}s")
            return reconstruct_path(current_belief[0]) 
        belief_signature = tuple(tuple(tuple(row) for row in node.state) for node in current_belief)
        if belief_signature in closed_set:
            continue
        closed_set.add(belief_signature)
    return False

def AND_OR_Search(beliefState, goalTest, actions, transitionModel):
    beliefState = [tuple(tuple(row) for row in state) for state in beliefState]  
    plan = OR_Search(beliefState, [], goalTest, actions, transitionModel)
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
            return [action, plan]

    return "failure"


def AND_Search(outcomeStates, path, goalTest, actions, transitionModel):
    subplans = []

    for state in outcomeStates:
        plan = OR_Search([state], path, goalTest, actions, transitionModel)

        if plan == "failure":
            return "failure"

        subplans.append(plan)

    return subplans

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

def solve_8_puzzle_with_AND_OR(initial_belief):
    plan = AND_OR_Search(initial_belief, goalTest, actions, transitionModel)
    if plan == "failure":
        return None
    
    # Convert plan to path
    current_state = initial_belief[0]
    path = [Node(current_state)]
    
    def execute_plan(plan, current_state):
        if not plan:
            return []
            
        if isinstance(plan, list):
            if len(plan) == 2:  # [action, subplan]
                action, subplan = plan
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
                
                return [Node(new_state, path[-1], action)] + execute_plan(subplan, new_state)
            else:  # List of subplans
                result = []
                for subplan in plan:
                    result.extend(execute_plan(subplan, current_state))
                return result
        return []
    
    path.extend(execute_plan(plan, current_state))
    return path

initial_belief = [
    [[2, 8, 3], [1, 6, 4], [7, 0, 5]],
    [[2, 8, 3], [1, 6, 4], [0, 7, 5]]
]

def draw_buttons(selected_algo):
    """Draw buttons with improved UI."""
    buttons = [
        ("Reset", RED, (20, 400, 100, 40)),
        ("Random", GREEN, (130, 400, 100, 40)),
        ("BFS", BLUE, (20, 450, 70, 40), selected_algo == "BFS"),
        ("DFS", BLUE, (100, 450, 70, 40), selected_algo == "DFS"),
        ("IDDFS", BLUE, (180, 450, 70, 40), selected_algo == "IDDFS"),
        ("UCS", BLUE, (260, 450, 70, 40), selected_algo == "UCS"),
        ("Greedy", BLUE, (20, 500, 70, 40), selected_algo == "Greedy"),
        ("A*", BLUE, (100, 500, 70, 40), selected_algo == "A*"),
        ("IDA*", BLUE, (180, 500, 70, 40), selected_algo == "IDA*"),
        ("Hill", BLUE, (260, 500, 70, 40), selected_algo == "Hill"),
        ("Hill_Simple", BLUE, (20, 550, 120, 40), selected_algo == "Hill_Simple"),
        ("stochastic_hill", BLUE, (150, 550, 170, 40), selected_algo == "stochastic_hill"),
        ("simulated", BLUE, (20, 650, 120, 40), selected_algo == "simulated"),
        ("beam", BLUE, (150, 650, 60, 40), selected_algo == "beam"),
        ("Genetic", BLUE, (220, 650, 100, 40), selected_algo == "Genetic"),
        ("BFS_Belief", BLUE, (20, 600, 70, 40), selected_algo == "BFS_Belief"),
        ("DFS_Belief", BLUE, (100, 600, 70, 40), selected_algo == "DFS_Belief"),
        ("AND_OR", BLUE, (20, 700, 150, 40), selected_algo == "AND_OR"),
        ("Backtracking", BLUE, (180, 700, 150, 40), selected_algo == "Backtracking"),
        ("Q-Learning", BLUE, (20, 750, 100, 40), selected_algo == "Q-Learning"),
        ("Run", BLACK, (WIDTH // 2 - 50, 770, 100, 40)),
    ]

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for text, color, rect, *selected in buttons:
        # Check if mouse is hovering over the button
        is_hovered = rect[0] <= mouse_x <= rect[0] + rect[2] and rect[1] <= mouse_y <= rect[1] + rect[3]
        button_color = GREEN if selected and selected[0] else (color if not is_hovered else (200, 200, 200))

        # Draw button with rounded corners
        pygame.draw.rect(screen, button_color, rect, border_radius=10)

        # Draw button border
        pygame.draw.rect(screen, BLACK, rect, width=2, border_radius=10)

        # Render button text
        btn_text = font_small.render(text, True, WHITE)
        btn_rect = btn_text.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
        screen.blit(btn_text, btn_rect)


def draw_slider(speed):
    """Draw the slider with improved UI."""
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
    col = index % 3
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

# Q-learning parameters
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
EPSILON = 0.1  # Exploration rate

# Initialize Q-table
Q_table = {}

def get_state_key(state):
    """Convert the state to a hashable key for Q-table."""
    return tuple(tuple(row) for row in state)

def get_possible_actions(state):
    """Return possible actions for the current state."""
    x_0, y_0 = Node(state).get_index_0()
    actions = []
    if x_0 > 0: actions.append("up")
    if x_0 < GRID - 1: actions.append("down")
    if y_0 > 0: actions.append("left")
    if y_0 < GRID - 1: actions.append("right")
    return actions

def take_action(state, action):
    """Apply an action to the state and return the new state."""
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
    """Define the reward for a given state."""
    if state == final_state:
        return 100  # High reward for reaching the goal
    return -1  # Small penalty for each step

def q_learning(state, episodes=1000, max_steps=100):
    """Perform Q-learning to solve the puzzle."""
    for episode in range(episodes):
        current_state = copy.deepcopy(state)
        steps = 0
        
        while current_state != final_state and steps < max_steps:
            state_key = get_state_key(current_state)
            
            # Initialize Q-table for the current state if not already present
            if state_key not in Q_table:
                Q_table[state_key] = {action: 0 for action in get_possible_actions(current_state)}
            
            # Choose action using epsilon-greedy strategy
            if np.random.rand() < EPSILON:
                action = random.choice(get_possible_actions(current_state))
            else:
                action = max(Q_table[state_key], key=Q_table[state_key].get)
            
            # Take action and observe new state and reward
            new_state = take_action(current_state, action)
            reward = reward_function(new_state)
            new_state_key = get_state_key(new_state)
            
            # Initialize Q-table for the new state if not already present
            if new_state_key not in Q_table:
                Q_table[new_state_key] = {action: 0 for action in get_possible_actions(new_state)}
            
            # Update Q-value using the Q-learning formula
            best_next_action = max(Q_table[new_state_key], key=Q_table[new_state_key].get, default=0)
            Q_table[state_key][action] += ALPHA * (
                reward + GAMMA * Q_table[new_state_key][best_next_action] - Q_table[state_key][action]
            )
            
            # Move to the new state
            current_state = new_state
            steps += 1

    # Extract the solution path
    solution = []
    current_state = copy.deepcopy(state)
    while current_state != final_state:
        state_key = get_state_key(current_state)
        if state_key not in Q_table:
            break  # If no Q-value exists for the current state, stop
        action = max(Q_table[state_key], key=Q_table[state_key].get)
        solution.append(Node(current_state))
        current_state = take_action(current_state, action)
    solution.append(Node(final_state))
    return solution

def main():
    current_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
    running = True
    solution = None
    step = 0
    selected_algo = "Greedy"
    speed = 500
    dragging = False
    execution_time = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 20 <= x <= 120 and 400 <= y <= 440:
                    current_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
                    solution = None
                    step = 0
                elif 130 <= x <= 230 and 400 <= y <= 440:
                    while True:
                        current_state = random_state()
                        if is_sol(current_state):
                            break
                    solution = None
                    step = 0
                elif 20 <= x <= 90 and 450 <= y <= 490:
                    selected_algo = "BFS"
                elif 100 <= x <= 170 and 450 <= y <= 490:
                    selected_algo = "DFS"
                elif 180 <= x <= 250 and 450 <= y <= 490:
                    selected_algo = "IDDFS"
                elif 260 <= x <= 330 and 450 <= y <= 490:
                    selected_algo = "UCS"
                elif 20 <= x <= 90 and 500 <= y <= 540:
                    selected_algo = "Greedy"
                elif 100 <= x <= 170 and 500 <= y <= 540:
                    selected_algo = "A*"   
                elif 180 <= x <= 250 and 500 <= y <= 540:
                    selected_algo = "IDA*"
                elif 260 <= x <= 330 and 500 <= y <= 540:
                    selected_algo = "Hill"
                elif (20 <= x <= 140 and 550 <= y <= 590):
                    selected_algo = "Hill_Simple"
                elif (150 <= x <= 320 and 550 <= y <= 590):
                    selected_algo = "stochastic_hill"
                elif (20 <= x <= 140 and 650 <= y <= 690):
                    selected_algo = "simulated"
                elif (150 <= x <= 210 and 650 <= y <= 690):
                    selected_algo = "beam"
                elif (220 <= x <= 320 and 650 <= y <= 690):
                    selected_algo = "Genetic"
                elif 20 <= x <= 90 and 600 <= y <= 640:  
                    selected_algo = "BFS_Belief"
                elif 100 <= x <= 170 and 600 <= y <= 640:  
                    selected_algo = "DFS_Belief"
                elif 20 <= x <= 170 and 700 <= y <= 740:
                    selected_algo = "AND_OR"
                    solution = solve_8_puzzle_with_AND_OR(initial_belief)
                    if solution:
                        print("AND-OR Search: Solution found")
                    else:
                        print("AND-OR Search: No solution found")
                    step = 0
                elif 180 <= x <= 330 and 700 <= y <= 740:  
                    selected_algo = "Backtracking"
                    current_state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                    solution = backtracking_fill_puzzle(current_state, 0, [False] * 9, [])
                    if solution:
                        print("Backtracking: Puzzle filled successfully")
                    else:
                        print("Backtracking: Failed to fill the puzzle")
                    step = 0
                elif 20 <= x <= 120 and 750 <= y <= 790:
                    selected_algo = "Q-Learning"
                elif WIDTH//2 - 50 <= x <= WIDTH//2 + 50 and 770 <= y <= 810:
                    start_time = time.time()
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
                        solution = beam_search(current_state,2)
                    elif selected_algo == "Genetic":
                        solution = genetic_algorithm(current_state)
                    elif selected_algo == "BFS_Belief":
                        belief_set = [
                            [[1, 2, 3], [4, 0, 5], [6, 7, 8]],
                            [[1, 2, 3], [4, 5, 0], [6, 7, 8]]
                        ]
                        solution = bfs_with_belief(belief_set)
                    elif selected_algo == "DFS_Belief":
                        belief_set = [
                            [[1, 2, 3], [4, 0, 5], [6, 7, 8]],
                            [[1, 2, 3], [4, 5, 0], [6, 7, 8]]
                        ]
                        solution = dfs_with_belief(belief_set)
                    elif selected_algo == "Q-Learning":
                        solution = q_learning(current_state, episodes=1000, max_steps=100)
                    else:
                        solution = greedy(current_state)

                    end_time = time.time()
                    execution_time = end_time - start_time
                    step = 0
                elif slider_x <= x <= slider_x + slider_width and slider_y <= y <= slider_y + slider_height:
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                x = max(slider_x, min(slider_x + slider_width, event.pos[0]))
                speed = int((x - slider_x) / slider_width * 1000)

        draw_state(current_state)
        draw_buttons(selected_algo)
        draw_slider(speed)
        
        if solution and step < len(solution):
            current_state = solution[step].state
            print(current_state)
            print(step)
            step += 1
            pygame.time.wait(speed)

        if solution:
            time_text = font_small.render(f"{execution_time:.6f}s", True, BLACK)
            screen.blit(time_text, (WIDTH//2 + 120, HEIGHT - time_text.get_height() - 10))
        text_step = font.render(str(step), True, BLACK)
        screen.blit(text_step, (WIDTH//2 - text_step.get_width()//2, HEIGHT - text_step.get_height() + 10))
        
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
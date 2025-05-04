# 🧩 8 Puzzle Solver - Trí Tuệ Nhân Tạo

## 📘 Giới thiệu

Dự án này là một ứng dụng giải bài toán **8 Puzzle** sử dụng nhiều **thuật toán tìm kiếm** và **tối ưu hóa** khác nhau.  
8 Puzzle là một bài toán cổ điển trong lĩnh vực **Trí tuệ nhân tạo**, nơi người chơi cần sắp xếp các ô số từ trạng thái ban đầu về trạng thái đích bằng cách di chuyển ô trống.

Ứng dụng có giao diện đồ họa trực quan, giúp người dùng dễ dàng tương tác và quan sát quá trình hoạt động của các thuật toán.

---

## ⚙️ Chức năng chính

### 1. Giao diện người dùng (UI)

- Xây dựng bằng thư viện **Pygame**.
- Hiển thị trạng thái hiện tại của bảng 8 Puzzle.
- Các nút chức năng:
  - 🔁 **Reset**: Đặt lại trạng thái ban đầu.
  - 🎲 **Random**: Tạo trạng thái ngẫu nhiên.
  - 🔍 **Chọn thuật toán**: Nhấn vào các nút tương ứng.
  - ▶️ **Run**: Chạy thuật toán đã chọn để tìm lời giải.
  - 🐢🐇 **Slider điều chỉnh tốc độ**: Tùy chỉnh tốc độ hiển thị lời giải.

---

### 2. Các thuật toán tìm kiếm

#### 🔎 Thuật toán tìm kiếm cơ bản:

- **BFS** (Breadth-First Search)
- **DFS** (Depth-First Search)
- **IDDFS** (Iterative Deepening DFS)
- **UCS** (Uniform Cost Search)

#### 🧠 Thuật toán heuristic:

- **Greedy Search**
- **A\*** (A-Star)
- **IDA\*** (Iterative Deepening A\*)

#### 📈 Thuật toán tối ưu hóa:

- **Hill Climbing**
- **Stochastic Hill Climbing**
- **Simulated Annealing**
- **Beam Search**
- **Genetic Algorithm**

---

### 3. Các thuật toán với niềm tin (Belief)

- **BFS_Belief**
- **DFS_Belief**
- **AND-OR Search**

---

### 4. Thuật toán học tăng cường (Reinforcement Learning)

- **Q-Learning**

---

### 5. Thuật toán quay lui (Backtracking)

- Áp dụng phương pháp **quay lui** để điền các ô trống trong bảng 8 Puzzle.

---

## 🖥️ Hướng dẫn sử dụng

### 1. Chạy chương trình

```bash
python python 23110274_huynhduynguyen_btt.py
```

### 2. Tương tác với giao diện

- 🔁 **Reset**: Đặt lại trạng thái ban đầu.
- 🎲 **Random**: Tạo trạng thái ngẫu nhiên.
- 🔍 **Chọn thuật toán**: Nhấn vào các nút tương ứng.
- ▶️ **Run**: Bắt đầu tìm lời giải.
- 🐢🐇 **Slider**: Điều chỉnh tốc độ hiển thị.

---

## 💻 Công nghệ sử dụng

- **Python**: Ngôn ngữ chính.
- **Pygame**: Giao diện đồ họa.
- **Numpy**: Xử lý ma trận và số học.
- **Heapq**: Hàng đợi ưu tiên.
- **Deque**: Hàng đợi hai đầu (dùng trong BFS/DFS).

---

## 🚀 Hướng phát triển

- Tối ưu hiệu suất thuật toán.
- Thêm thuật toán như **Minimax**, **Alpha-Beta Pruning**.
- Cải tiến giao diện người dùng (UI/UX).

---

## 🖼️ Ảnh minh họa



---

## 👤 Tác giả

- **Họ và tên**: Huỳnh Duy Nguyễn  
- **MSSV**: 23110274

import tkinter as tk
import random

WIDTH = 400
HEIGHT = 400
SEGMENT_SIZE = 20


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.timer_id = None
        self.current_speed = 10
        self.snake = []
        self.running = True
        self.food = None
        self.score = 0
        self.canvas = tk.Canvas(self.root, bg="black",
                                width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.score_label = self.canvas.create_text(
            WIDTH // 2, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 24)
        )

        self.build_hamiltonian_cycle()
        self.snake_set = set(self.snake)

        self.spawn_snake()
        self.spawn_food()
        self.run_game()

    def build_hamiltonian_cycle(self):
        self.hamiltonian_cycle = []
        rows = HEIGHT // SEGMENT_SIZE
        cols = WIDTH // SEGMENT_SIZE

        for row in range(rows):
            if row % 2 == 0:
                for col in range(cols):
                    self.hamiltonian_cycle.append(
                        (col * SEGMENT_SIZE, row * SEGMENT_SIZE))
            else:
                for col in reversed(range(cols)):
                    self.hamiltonian_cycle.append(
                        (col * SEGMENT_SIZE, row * SEGMENT_SIZE))

    def spawn_snake(self):
        self.snake = [self.hamiltonian_cycle[0],
                      self.hamiltonian_cycle[1], self.hamiltonian_cycle[2]]
        self.snake_set = set(self.snake)

    def spawn_food(self):
        free_cells = [(x * SEGMENT_SIZE, y * SEGMENT_SIZE) for x in range(WIDTH // SEGMENT_SIZE)
                      for y in range(HEIGHT // SEGMENT_SIZE) if (x * SEGMENT_SIZE, y * SEGMENT_SIZE) not in self.snake_set]

        if not free_cells:
            self.running = False
            return

        self.food = random.choice(free_cells)
        self.canvas.create_rectangle(
            self.food[0], self.food[1], self.food[0] + SEGMENT_SIZE, self.food[1] + SEGMENT_SIZE, fill="red", tags="food"
        )

    def move_snake(self):
        head_index = self.hamiltonian_cycle.index(self.snake[0])
        next_index = (head_index + 1) % len(self.hamiltonian_cycle)
        new_head = self.hamiltonian_cycle[next_index]

        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.canvas.delete("food")
            self.spawn_food()
            self.score += 1
            self.canvas.itemconfigure(
                self.score_label, text=f"Score: {self.score}")
        else:
            self.snake.pop()

        self.snake.insert(0, new_head)
        self.snake_set = set(self.snake)
        self.update_canvas()

        if len(self.snake) == (WIDTH // SEGMENT_SIZE) * (HEIGHT // SEGMENT_SIZE):
            self.running = False

    def update_canvas(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill="green", tags="snake"
            )

    def run_game(self):
        if self.running:
            self.move_snake()
            self.timer_id = self.root.after(self.current_speed, self.run_game)
        else:
            self.game_over()

    def game_over(self):
        free_cells = [(x * SEGMENT_SIZE, y * SEGMENT_SIZE) for x in range(WIDTH // SEGMENT_SIZE)
                      for y in range(HEIGHT // SEGMENT_SIZE) if (x * SEGMENT_SIZE, y * SEGMENT_SIZE) not in self.snake_set]

        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="GAME OVER!\nNo more free cells!" if not free_cells else "GAME OVER!",
            fill="white",
            font=("Arial", 24),
            tags="gameover",
        )
        print(f"Конец игры! Итоговый счёт: {self.score}")
        self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Змейка")
    game = SnakeGame(root)
    root.mainloop()

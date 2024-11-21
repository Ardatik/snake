import tkinter as tk
import random

WIDTH = 1920
HEIGHT = 1080
SEGMENT_SIZE = 20
GAME_SPEED = 100

class Snake:
    def __init__(self, root):
        self.root = root
        self.root.title("Змейка Full HD")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg="black")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, bg="black", width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = None
        self.score = 0
        self.running = True

        self.score_label = self.canvas.create_text(
            WIDTH // 2, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 24)
        )

        self.root.bind("<KeyPress>", self.change_direction)
        self.root.bind("<KeyPress-r>", self.restart_game)

        self.spawn_food()
        self.run_game()

    def spawn_food(self):
        x = random.randint(0, (WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
        y = random.randint(0, (HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
        self.food = (x, y)
        self.canvas.create_rectangle(
            x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill="red", tags="food"
        )

    def change_direction(self, event):
        if not self.running:
            return
        new_direction = event.keysym
        opposites = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if new_direction in opposites and opposites[new_direction] != self.direction:
            self.direction = new_direction

    def run_game(self):
        if self.running:
            self.move_snake()
            self.check_collision()
            self.root.after(GAME_SPEED, self.run_game)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Left":
            head_x -= SEGMENT_SIZE
        elif self.direction == "Right":
            head_x += SEGMENT_SIZE
        elif self.direction == "Up":
            head_y -= SEGMENT_SIZE
        elif self.direction == "Down":
            head_y += SEGMENT_SIZE

        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        if self.food == new_head:
            self.snake.append(self.snake[-1])
            self.canvas.delete("food")
            self.spawn_food()
            self.score += 1
            self.canvas.itemconfigure(self.score_label, text=f"Score: {self.score}")

        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill="green", tags="snake"
            )

    def check_collision(self):
        head = self.snake[0]
        # Проверка выхода за границы
        if (
            head[0] < 0
            or head[0] >= WIDTH
            or head[1] < 0
            or head[1] >= HEIGHT
            or head in self.snake[1:]
        ):
            self.running = False
            self.game_over()

    def game_over(self):
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="GAME OVER! Press 'R' to Restart",
            fill="white",
            font=("Arial", 36),
            tags="gameover",
        )

    def restart_game(self, event):
        self.running = True
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.score = 0
        self.canvas.delete("food")
        self.canvas.delete("snake")
        self.canvas.delete("gameover")
        self.canvas.itemconfigure(self.score_label, text=f"Score: {self.score}")
        self.spawn_food()
        self.run_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

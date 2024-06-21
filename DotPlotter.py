import tkinter as tk
import tkinter.simpledialog as simpledialog
import random

class DotPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Dot Plotter")
        self.root.configure(bg="black")  # Set window background to black

        self.canvas_width = 600
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        self.num_dots = 0
        self.dot_size = 3  # Adjust dot size here
        self.dots = []
        self.pause = False  # Flag to pause regeneration

        self.get_user_input()
        self.start_regeneration()

    def get_user_input(self):
        self.num_dots = simpledialog.askinteger("Dot Plotter", "Enter number of dots:")
        if self.num_dots is None or self.num_dots <= 0:
            self.root.quit()
            return
        
        self.generate_dots()

    def generate_dots(self):
        # Clear previous dots and connections
        self.canvas.delete("all")
        self.dots.clear()

        # Generate random dots
        for _ in range(self.num_dots):
            x = random.randint(50, self.canvas_width - 50)
            y = random.randint(50, self.canvas_height - 50)
            self.dots.append((x, y))
            self.canvas.create_oval(x - self.dot_size, y - self.dot_size,
                                    x + self.dot_size, y + self.dot_size, fill="red")

        # Connect dots with dotted curved lines
        self.connect_dots()

    def connect_dots(self):
        # Clear previous connections
        self.canvas.delete("line")

        # Generate random connections
        for i in range(self.num_dots):
            for j in range(i + 1, self.num_dots):
                x1, y1 = self.dots[i]
                x2, y2 = self.dots[j]

                # Create a curved line using Bézier curve approximation
                cx1, cy1 = x1 + (x2 - x1) * 0.4, y1 + (y2 - y1) * 0.1  # Control point 1
                cx2, cy2 = x1 + (x2 - x1) * 0.6, y1 + (y2 - y1) * 0.9  # Control point 2

                # Create a dotted line
                self.canvas.create_line(x1, y1, x2, y2, smooth=True, splinesteps=20, fill="white", tags="line", dash=(3, 3))

        # Schedule next regeneration if not paused
        if not self.pause:
            self.root.after(50, self.regenerate)  # Refresh every 5 seconds

    def start_regeneration(self):
        # Initial generation
        self.generate_dots()

    def regenerate(self):
        # Move dots to new random positions
        for dot in self.dots:
            x = random.randint(50, self.canvas_width - 50)
            y = random.randint(50, self.canvas_height - 50)
            self.canvas.coords(dot[0], x - self.dot_size, y - self.dot_size,
                               x + self.dot_size, y + self.dot_size)

        # Reconnect dots with new positions
        self.connect_dots()

    def toggle_pause(self):
        self.pause = not self.pause
        if not self.pause:
            self.generate_dots()

if __name__ == "__main__":
    root = tk.Tk()
    app = DotPlotter(root)

    # Pause Button
    pause_button = tk.Button(root, text="Pause/Resume", command=app.toggle_pause, bg="white")
    pause_button.pack()

    root.mainloop()

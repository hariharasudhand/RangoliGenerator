import tkinter as tk
import tkinter.simpledialog as simpledialog
import random

class RangoliGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Rangoli Generator")
        self.root.configure(bg="black")  # Set window background to black

        self.canvas_width = 600
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        self.num_rows = None
        self.num_cols = None
        self.dot_size = 3  # Adjust dot size here
        self.dot_spacing = 50  # Adjust dot spacing here
        self.dots = []
        self.pause = False  # Flag to pause regeneration

        self.get_user_input()
        self.start_regeneration()

    def get_user_input(self):
        self.num_rows = simpledialog.askinteger("Rangoli Generator", "Enter number of rows:")
        if self.num_rows is None or self.num_rows <= 0:
            self.root.quit()
            return
        
        self.num_cols = simpledialog.askinteger("Rangoli Generator", "Enter number of columns:")
        if self.num_cols is None or self.num_cols <= 0:
            self.root.quit()
            return
        
        self.generate_rangoli()

    def generate_rangoli(self):
        # Clear previous dots and connections
        self.canvas.delete("all")
        self.dots.clear()

        # Generate dots in a grid pattern
        for row in range(self.num_rows):
            line_color = "white" if row % 2 == 0 else "pink"
            for col in range(self.num_cols):
                x = col * self.dot_spacing + 50
                y = row * self.dot_spacing + 50
                self.dots.append((x, y))
                self.canvas.create_oval(x - self.dot_size, y - self.dot_size,
                                        x + self.dot_size, y + self.dot_size, fill="red")
        
        # Generate random connections between dots
        self.connect_dots()

    def connect_dots(self):
        # Clear previous connections
        self.canvas.delete("line")

        # Randomly connect dots to create patterns
        num_connections = random.randint(self.num_rows * self.num_cols // 2, self.num_rows * self.num_cols)
        for _ in range(num_connections):
            dot1 = random.choice(self.dots)
            dot2 = random.choice(self.dots)
                
            # Ensure dots are not horizontally aligned
            while dot1[0] == dot2[0]:
                dot2 = random.choice(self.dots)
                
            # Create a curved line using Bézier curve approximation
            x1, y1 = dot1[0], dot1[1]
            x2, y2 = dot2[0], dot2[1]

            # Determine the number of segments for the zigzag
            num_segments = random.randint(2, 8)
            points = []
            for i in range(num_segments + 1):
                frac = i / num_segments
                px = x1 * (1 - frac) + x2 * frac
                py = y1 * (1 - frac) + y2 * frac
                deviation = random.randint(-20, 20)
                if i % 2 == 0:
                    deviation *= -1
                points.append(px + deviation)
                points.append(py + deviation)

            # Create a dotted line
            for i in range(0, len(points) - 2, 2):
                self.canvas.create_line(points[i], points[i+1], points[i+2], points[i+3], fill="white", dash=(3, 3))

        # Schedule next regeneration if not paused
        if not self.pause:
            self.root.after(100, self.regenerate)


    def start_regeneration(self):
        # Initial generation
        self.generate_rangoli()

    def regenerate(self):
        self.generate_rangoli()

    def toggle_pause(self):
        self.pause = not self.pause
        if not self.pause:
            self.generate_rangoli()

if __name__ == "__main__":
    root = tk.Tk()
    app = RangoliGenerator(root)

    # Pause Button
    pause_button = tk.Button(root, text="Pause/Resume", command=app.toggle_pause, bg="white")
    pause_button.pack()

    root.mainloop()

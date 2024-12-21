import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

# Sample list of 2D arrays
arrays = [
    [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]],
    [["a", "b", "x"], ["d", "y", "f"], ["z", "h", "i"]],
    [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]],
]

# Convert 2D arrays to numpy array (for rendering)
def char_array_to_numeric(array):
    return np.array([[ord(char) for char in row] for row in array])

# Interactive visualization class
class ArrayViewer:
    def __init__(self, arrays):
        self.arrays = arrays
        self.index = 0
        self.fig, self.ax = plt.subplots()
        self.im = None
        self.draw_array()

        axprev = plt.axes([0.7, 0.01, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.01, 0.1, 0.075])
        self.bnext = Button(axnext, 'Next')
        self.bprev = Button(axprev, 'Previous')

        self.bnext.on_clicked(self.next_array)
        self.bprev.on_clicked(self.prev_array)

    def draw_array(self):
        self.ax.clear()
        char_array = self.arrays[self.index]
        numeric_array = char_array_to_numeric(char_array)
        self.im = self.ax.imshow(numeric_array, cmap="viridis", origin="upper")

        # Annotate the characters
        for i, row in enumerate(char_array):
            for j, char in enumerate(row):
                self.ax.text(j, i, char, ha="center", va="center", color="white")

        self.ax.set_title(f"Array {self.index + 1}/{len(self.arrays)}")
        self.fig.canvas.draw()

    def next_array(self, event):
        if self.index < len(self.arrays) - 1:
            self.index += 1
            self.draw_array()

    def prev_array(self, event):
        if self.index > 0:
            self.index -= 1
            self.draw_array()

# Launch the interactive viewer
# viewer = ArrayViewer(arrays)
# plt.show()

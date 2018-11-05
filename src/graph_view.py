import tkinter as tk
import networkx as nx


class GraphViewer:
    def __init__(self, parent):
        self._parent = parent
        self._canvas = tk.Canvas(parent, width=1024, height=768)
        self._canvas.pack()

    def on_next(self, G):
        self._canvas.delete('all')

        def scale(x, y):
            zoom = 0.7
            width = self._canvas.winfo_width()
            height = self._canvas.winfo_height()
            size = min(width, height)
            x = (width + size * x * zoom) / 2
            y = (height + size * y * zoom) / 2
            return x, y

        layout = nx.spring_layout(G)
        for from_, to in G.edges:
            x_from, y_from = scale(*layout[from_])
            x_to, y_to = scale(*layout[to])
            self._canvas.create_line(x_from, y_from, x_to, y_to)
        for x, y in layout.values():
            x, y = scale(x, y)
            self._canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red')

    def on_error(self, err):
        print('error in drawing', err)
        self._parent.quit()

    def on_complete(self):
        pass

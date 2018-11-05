import tkinter as tk
import networkx as nx
from rx.subjects import BehaviorSubject, Subject


class GraphViewer:
    def __init__(self, parent):
        self._parent = parent
        self._canvas = tk.Canvas(parent, width=1024, height=768)
        self._canvas.pack()
        self.zoom = BehaviorSubject(0.7)
        self._k = self.zoom.scan(lambda acc, curr: acc * curr)
        self.x_center = BehaviorSubject(0.5)
        self.y_center = BehaviorSubject(0.5)
        self.layout = BehaviorSubject(nx.spring_layout)
        self._G = Subject()
        def draw(G, x_center, y_center, k, layout):
            def scale(x, y):
                width = self._canvas.winfo_width()
                height = self._canvas.winfo_height()
                size = min(width, height) / 2
                x = width * x_center + size * x * k
                y = height * x_center + size * y * k
                return x, y
            self._canvas.delete('all')
            nodes = layout(G)
            for from_, to in G.edges:
                x_from, y_from = scale(*nodes[from_])
                x_to, y_to = scale(*nodes[to])
                self._canvas.create_line(x_from, y_from, x_to, y_to)
            for x, y in nodes.values():
                x, y = scale(x, y)
                self._canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red')

        wrap = lambda *args: args
        redraw = self._G.combine_latest(self.x_center, self.y_center, self._k, self.layout, draw)
        redraw.subscribe()


    def on_next(self, G):
        self._G.on_next(G)
        self.x_center.on_next(0.5)
        self.y_center.on_next(0.5)

    def on_error(self, err):
        print('error in drawing', err)
        self._parent.quit()

    def on_complete(self):
        pass

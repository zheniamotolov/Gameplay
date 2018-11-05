from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx


def _draw(canvas, G):
    plt.clf()
    nx.draw(G, layout=nx.spring_layout(G))
    canvas.draw()


class GraphViewer:
    def __init__(self, parent):
        f = plt.figure(figsize=(5, 4), dpi=100)
        self._parent = parent
        self._canvas = FigureCanvasTkAgg(f, master=parent)
        self._canvas.get_tk_widget().pack()

    def on_next(self, G):
        _draw(self._canvas, G)

    def on_error(self, err):
        print('error in drawing', err)
        self._parent.quit()

    def on_complete(self):
        pass

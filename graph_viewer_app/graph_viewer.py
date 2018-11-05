import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from import_handler import ImportHandler
from export_handler import ExportHandler
import pygraphviz as pgv
import matplotlib.image as mpimg


class GraphViewerGUI:
    def __init__(self, parent):
        self._graph = nx.Graph()
        figure = plt.figure(figsize=(10, 10))
        self._parent = parent
        self._canvas = FigureCanvasTkAgg(figure, master=parent)
        self._canvas.get_tk_widget().pack()
        self._parent.wm_protocol('WM_DELETE_WINDOW', parent.quit)
        self.create_menubar()

    def create_menubar(self):
        menubar = tk.Menu(self._parent)
        files_menubar = tk.Menu(menubar, tearoff=0)
        import_handler = ImportHandler()
        export_handler = ExportHandler()
        files_menubar.add_command(label='Import',
                                  command=lambda: self.draw(import_handler.import_graph_from_file(self.reset_graph())))
        files_menubar.add_command(label='Export',
                                  command=lambda: self.draw(export_handler.export_graph_to_file(self._graph)))
        files_menubar.add_command(label='Visualize planar embedding of graph',
                                  command=lambda: self.show_planar_embedding_of_graph())
        menubar.add_cascade(label='File', menu=files_menubar)

        grphs_menubar = tk.Menu(menubar, tearoff=0)
        grphs_menubar.add_command(label='Cube', command=lambda: self.show_cube())
        grphs_menubar.add_command(label='Cycle', command=lambda: self.show_cycle())
        grphs_menubar.add_command(label='Complete', command=lambda: self.show_complete())
        # grphs_menubar.add_command(label='4D hypercube', command=lambda: self.show_hyper4d())
        menubar.add_cascade(label='Graphs', menu=grphs_menubar)
        self._parent.config(menu=menubar)

    def reset_graph(self):
        self._graph = nx.Graph()
        return self._graph

    def show_complete(self):
        self._graph = nx.complete_graph(5)
        self.draw(self._graph)

    def show_cube(self):
        self._graph = nx.cubical_graph()
        self.draw(self._graph)

    def show_cycle(self):
        self._graph = nx.cycle_graph(7)
        self.draw(self._graph)

    def show_hyper4d(self):
        self._graph = nx.hypercube_graph(4)
        show_labels = False
        self.draw(self._graph, show_labels)

    def show_planar_embedding_of_graph(self):
        # if nx.check_planarity(self._graph)[0]:
        a_graph = pgv.AGraph()
        a_graph.node_attr['shape'] = 'circle'
        a_graph.node_attr['style'] = 'filled'
        a_graph.node_attr['color'] = 'red'
        a_graph.add_edges_from(self._graph.edges())
        a_graph.layout(prog='dot')
        a_graph.draw('../resources/planar.png')
        plt.clf()
        img = mpimg.imread('../resources/planar.png')
        plt.axis('off')
        plt.imshow(img)
        self._canvas.draw()

    def draw(self, graph, show_labels=True):
        plt.clf()
        nx.draw(graph, with_labels=show_labels, node_size=1500, layout=nx.spring_layout(graph))
        self._canvas.draw()


def main():
    root = tk.Tk()
    graph_viewer = GraphViewerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

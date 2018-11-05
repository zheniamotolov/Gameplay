import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from import_handler import ImportHandler
from export_handler import ExportHandler
import pygraphviz as pgv


class GraphViewerGUI:
    def __init__(self, parent):
        self._graph = nx.Graph()
        figure = plt.figure(figsize=(5, 4), dpi=100)
        self._parent = parent
        self._canvas = FigureCanvasTkAgg(figure, master=parent)
        self._canvas.get_tk_widget().pack()
        parent.wm_protocol('WM_DELETE_WINDOW', parent.quit)
        self.create_menubar()
        self.create_buttons()

    def create_menubar(self):
        menubar = tk.Menu(self._parent)
        filemenu = tk.Menu(menubar)
        import_handler = ImportHandler(self._graph)
        export_handler = ExportHandler()
        filemenu.add_command(label='Import', command=lambda: self.draw(import_handler.import_graph_from_file()))
        filemenu.add_command(label='Export',
                             command=lambda: self.draw(export_handler.export_graph_to_file(self._graph)))
        filemenu.add_command(label='Visualize planar embedding of graph',
                             command=lambda: self.show_planar_embedding_of_graph())
        menubar.add_cascade(label='File', menu=filemenu)
        self._parent.config(menu=menubar)

    def create_buttons(self):
        tk.Button(self._parent, text='Cube', command=lambda: self.show_cube()).pack(side='left', padx=(130, 0))
        tk.Button(self._parent, text='Cycle', command=lambda: self.show_cycle()).pack(side='left')
        tk.Button(self._parent, text='Complete', command=lambda: self.show_complete()).pack(side='left')
        tk.Button(self._parent, text='4D hypercube', command=lambda: self.show_hyper4d()).pack(side='left')

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
        self.draw(self._graph,show_labels)

    def show_planar_embedding_of_graph(self):
        if nx.check_planarity(self._graph)[0]:
            a_graph = pgv.AGraph()
            a_graph.node_attr['shape'] = 'circle'
            a_graph.node_attr['style'] = 'filled'
            a_graph.node_attr['color'] = 'red'
            a_graph.add_edges_from(self._graph.edges())
            a_graph.layout(prog='dot')
            a_graph.draw('../resources/planar.png')
        else:
            print('graph in not planar')

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

from itertools import count
import tkinter as tk
from tkinter import filedialog
import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from rx.subjects import Subject, BehaviorSubject
from sys import exit

def graph_from_file(filename):
    graph = nx.Graph()
    with open(filename, 'r') as fp:
        data = json.load(fp)
    for point in data['points']:
        graph.add_node(point['idx'])
    for line in data['lines']:
        from_idx, to_idx = line['points']
        graph.add_edge(from_idx, to_idx, weight=line['length'])
    return graph

def graph_to_file(filename, graph):
    points = [{'idx': node, 'post_idx': None} for node in graph.nodes]
    lines = [{'idx': idx, 'length': 1, 'points': [x, y]} for idx, (x, y) in zip(count(1), graph.edges)]
    data = {'points': points, 'lines': lines}
    with open(filename, 'w') as fp:
        json.dump(data, fp)

def ask_export_filename():
    filetypes = [('JSON', '*.json'), ('All Files', '*')]
    filename = filedialog.asksaveasfile(filetypes=filetypes).name
    return filename

def draw(canvas, G):
    plt.clf()
    nx.draw(G, layout=nx.spring_layout(G))
    canvas.draw()

def ask_import_filename():
    filetypes = [('JSON', '*.json'), ('All Files', '*')]
    filename = filedialog.askopenfile(filetypes=filetypes).name
    return filename


class GraphViewer():
    def __init__(self, parent):
        f = plt.figure(figsize=(5, 4), dpi=100)
        self._parent = parent
        self._canvas = FigureCanvasTkAgg(f, master=parent)
        self._canvas.get_tk_widget().pack()

    def on_next(self, G):
        draw(self._canvas, G)

    def on_error(self, err):
        print('error in drawing', err)
        self._parent.quit()
    def on_complete(self):
        pass


def main():
    G = BehaviorSubject(nx.Graph())
    import_filename = Subject()
    export_filename = Subject()
    import_filename.map(graph_from_file).subscribe(G)
    root = tk.Tk()
    graph_viewer = GraphViewer(root)
    G.subscribe(graph_viewer)
    pair = export_filename.with_latest_from(G, lambda x, y: (x, y))
    pair.subscribe(lambda pair: graph_to_file(pair[0], pair[1]))
    def import_handler():
        import_filename.on_next(ask_import_filename())

    def export_handler():
        export_filename.on_next(ask_export_filename())

    root.wm_protocol('WM_DELETE_WINDOW', exit)
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar)
    filemenu.add_command(label='Import', command=import_handler)
    filemenu.add_command(label='Export', command=export_handler)
    menubar.add_cascade(label='File', menu=filemenu)
    root.config(menu=menubar)
    tk.mainloop()

if __name__ == '__main__':
    main()

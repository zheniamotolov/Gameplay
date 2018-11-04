from tkinter import filedialog
import json
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv
from IPython.display import Image

def read_graph_from_file(filename):
    graph = nx.Graph()
    with open(filename, 'r') as fp:
        data = json.load(fp)
#     for point in data['points']: # graph vertexes can be set just via lines
#         graph.add_node(point['idx'])
    for line in data['lines']:
        from_idx, to_idx = line['points']
        graph.add_edge(from_idx, to_idx, weight=line['length'])
    return graph

def show_planar_embedding_of_graph():
    global graph
    if(nx.check_planarity(graph)[0]):
        A=pgv.AGraph()
        A.node_attr['shape']='circle'
        A.node_attr['style']='filled'
        A.node_attr['color']='red'
        A.add_edges_from(graph.edges())
        A.layout(prog='dot')
        A.draw('planar.png')
        display(Image('planar.png'))
    else:
        print('graph in not planar')
    
def export_graph_to_file(graph, filename):
    points = [{'idx': node, 'post_idx': None} for node in graph.nodes]
    lines = [{'idx': idx, 'length': 1, 'points': [x, y]} for idx, (x, y) in zip(count(1), graph.edges)]
    data = {'points': points, 'lines': lines}
    with open(filename, 'w') as fp:
        json.dump(data, fp)

def export_handler():
    global graph
    filetypes = [('JSON', '*.json'), ('All Files', '*')]
    filename = filedialog.asksaveasfile(filetypes=filetypes).name
    export_graph_to_file(graph, filename)

def draw():
    global graph
    plt.clf()
    nx.draw(graph,with_labels=True,node_size=1500)
    plt.show()


def open_file_handler():
    filetypes = [('JSON', '*.json'), ('All Files', '*')]
    filename = filedialog.askopenfile(filetypes=filetypes).name
    global graph
    graph = read_graph_from_file(filename)
    draw()


def cube():
    global graph
    graph = nx.cubical_graph()
    draw()

def complete():
    global graph
    graph = nx.complete_graph(5)
    draw()

def cycle():
    global graph
    graph = nx.cycle_graph(7)
    draw()
    
def hyper4d():
    global graph
    graph = nx.hypercube_graph(4)
    draw()

if __name__ == '__main__':
    graph = None # is global var really good practiece?
    tk.Button(text='Vizualize graph from json file', command=open_file_handler).pack()
    tk.Button(text='Vizualize planar embedding of graph', command=show_planar_embedding_of_graph).pack()
    tk.Button(text='Export', command=export_handler).pack()
    tk.Button(text='Cube', command=cube).pack()
    tk.Button(text='Cycle', command=cycle).pack()
    tk.Button(text='Complete', command=complete).pack()
    tk.Button(text='4D hypercube', command=hyper4d).pack()
    tk.mainloop()


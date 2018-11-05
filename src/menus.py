import tkinter as tk
from tkinter import filedialog
from rx.subjects import Subject
from serialization import graph_to_file, graph_from_file
import networkx as nx

def ask_export_filename():
    filetypes = [('JSON', '*.json'), ('All Files', '*')]
    filename = filedialog.asksaveasfile(filetypes=filetypes).name
    return filename


def ask_import_filename():
    filetypes = [('JSON', '*.json'), ('All Files', '*')]
    filename = filedialog.askopenfile(filetypes=filetypes).name
    return filename


def file(parent, G):
    import_filename = Subject()
    export_filename = Subject()
    import_filename.map(graph_from_file).subscribe(G)
    pair = export_filename.with_latest_from(G, lambda x, y: (x, y))
    pair.subscribe(lambda pair: graph_to_file(pair[1], pair[0]))

    def import_handler():
        import_filename.on_next(ask_import_filename())

    def export_handler():
        export_filename.on_next(ask_export_filename())

    menu = tk.Menu(parent)
    menu.add_command(label='Import', command=import_handler)
    menu.add_command(label='Export', command=export_handler)
    parent.add_cascade(label='File', menu=menu)
    return menu


def graphs(parent, G):
    def cubical_handler():
        G.on_next(nx.cubical_graph())

    def hypercube_handler():
        G.on_next(nx.hypercube_graph(4))

    def cycle_handler():
        G.on_next(nx.cycle_graph(7))

    def complete_handler():
        G.on_next(nx.complete_graph(5))
    
    menu = tk.Menu(parent)
    menu.add_command(label='Cubical', command=cubical_handler)
    menu.add_command(label='Hypercube', command=hypercube_handler)
    menu.add_command(label='Complete', command=complete_handler)
    menu.add_command(label='Cycle', command=cycle_handler)
    parent.add_cascade(label='Graphs', menu=menu)
    return menu

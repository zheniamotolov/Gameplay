import tkinter as tk
from tkinter import filedialog
import networkx as nx
from rx.subjects import Subject

from data_parser import DataParser


class Menu:
    def __init__(self, menubar, graph_viewer):
        self.__menubar = menubar
        self.__graph_viewer = graph_viewer

    def create_menu_items(self, G):
        self.create_file_submenu(G)
        self.create_view_submenu()
        self.show_graphs(G)
        self.layouts()

    def ask_export_filename(self):
        filename = None
        filetypes = (('JSON', '*.json'), ('All Files', '*'))
        filepath = filedialog.asksaveasfile(filetypes=filetypes)
        if filepath:
            filename = filepath.name
            filepath.close()
        return filename

    def ask_import_filename(self):
        filename = None
        filetypes = (('JSON', '*.json'), ('All Files', '*'))
        filepath = filedialog.askopenfile(filetypes=filetypes)
        if filepath:
            filename = filepath.name
            filepath.close()
        return filename

    def create_file_submenu(self, G):
        data_parser = DataParser()
        import_filename = Subject()
        export_filename = Subject()

        import_filename \
            .map(data_parser.import_graph_from_file) \
            .filter(lambda i: i is not None) \
            .subscribe(G)

        pair = export_filename.with_latest_from(G, lambda x, y: (x, y))
        pair.subscribe(lambda pair: data_parser.export_graph_to_file(pair[1], pair[0]))

        menu = tk.Menu(self.menubar)

        menu.add_command(label='Import', command=lambda: import_filename.on_next(self.ask_import_filename()))
        menu.add_command(label='Export', command=lambda: export_filename.on_next(self.ask_export_filename()))
        self.menubar.add_cascade(label='File', menu=menu)
        return menu

    def show_graphs(self, G):
        menu = tk.Menu(self.menubar)
        menu.add_command(label='Cubical', command=lambda: G.on_next(nx.cubical_graph()))
        menu.add_command(label='Hypercube', command=lambda: G.on_next(nx.hypercube_graph(4)))
        menu.add_command(label='Complete', command=lambda: G.on_next(nx.complete_graph(5)))
        menu.add_command(label='Cycle', command=lambda: G.on_next(nx.cycle_graph(7)))
        self.menubar.add_cascade(label='Graphs', menu=menu)
        return menu

    def create_view_submenu(self):
        menu = tk.Menu(self.menubar)
        menu.add_command(label='Zoom In', command=lambda: self.graph_viewer.zoom.on_next(2))
        menu.add_command(label='Zoom Out', command=lambda: self.graph_viewer.zoom.on_next(2)
                         )
        self.menubar.add_cascade(label='View', menu=menu)
        return menu

    def layouts(self):
        menu = tk.Menu(self.menubar)
        menu.add_command(label='Spring', command=lambda: self.graph_viewer.layout.on_next(nx.spring_layout))
        menu.add_command(label='Shell', command=lambda: self.graph_viewer.layout.on_next(nx.shell_layout))
        menu.add_command(label='Spectral', command=lambda: self.graph_viewer.layout.on_next(nx.spectral_layout))
        self.menubar.add_cascade(label='Layouts', menu=menu)
        return menu

    @property
    def menubar(self):
        return self.__menubar

    @menubar.setter
    def menubar(self, menubar):
        self.__menubar = menubar

    @property
    def graph_viewer(self):
        return self.__graph_viewer

    @graph_viewer.setter
    def graph_viewer(self, graph_viewer):
        self.__graph_viewer = graph_viewer

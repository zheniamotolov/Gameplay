import tkinter as tk
from tkinter import filedialog
from rx.subjects import Subject
from data_parser import DataParser
import networkx as nx


class Menu:
    def __init__(self, menubar, graph_viewer):
        self.__menubar = menubar
        self.__graph_viewer = graph_viewer

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

    def create_menu_items(self, G):
        self.create_file_submenu(G)
        self.create_view_submenu()
        self.show_graphs(G)
        self.layouts()

    def ask_export_filename(self):
        filename = None
        filetypes = [('JSON', '*.json'), ('All Files', '*')]
        filepath = filedialog.asksaveasfile(filetypes=filetypes)
        if filepath:
            filename = filepath.name
            filepath.close()
        return filename

    def ask_import_filename(self):
        filename = None
        filetypes = [('JSON', '*.json'), ('All Files', '*')]
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
            .map(data_parser.graph_from_file) \
            .filter(lambda i: i is not None) \
            .subscribe(G)
        pair = export_filename.with_latest_from(G, lambda x, y: (x, y))
        pair.subscribe(lambda pair: data_parser.graph_to_file(pair[1], pair[0]))

        def import_handler():
            import_filename.on_next(self.ask_import_filename())

        def export_handler():
            export_filename.on_next(self.ask_export_filename())

        menu = tk.Menu(self.menubar)
        menu.add_command(label='Import', command=import_handler)
        menu.add_command(label='Export', command=export_handler)
        self.menubar.add_cascade(label='File', menu=menu)
        return menu

    def show_graphs(self, G):
        def cubical_handler():
            G.on_next(nx.cubical_graph())

        def hypercube_handler():
            G.on_next(nx.hypercube_graph(4))

        def cycle_handler():
            G.on_next(nx.cycle_graph(7))

        def complete_handler():
            G.on_next(nx.complete_graph(5))

        menu = tk.Menu(self.menubar)
        menu.add_command(label='Cubical', command=cubical_handler)
        menu.add_command(label='Hypercube', command=hypercube_handler)
        menu.add_command(label='Complete', command=complete_handler)
        menu.add_command(label='Cycle', command=cycle_handler)
        self.menubar.add_cascade(label='Graphs', menu=menu)
        return menu

    def create_view_submenu(self):
        def zoom_in_handler():
            self.graph_viewer.zoom.on_next(2)

        def zoom_out_handler():
            self.graph_viewer.zoom.on_next(0.5)

        menu = tk.Menu(self.menubar)
        menu.add_command(label='Zoom In', command=zoom_in_handler)
        menu.add_command(label='Zoom Out', command=zoom_out_handler)
        self.menubar.add_cascade(label='View', menu=menu)
        return menu

    def layouts(self):
        def spring_handler():
            self.graph_viewer.layout.on_next(nx.spring_layout)

        def shell_handler():
            self.graph_viewer.layout.on_next(nx.shell_layout)

        def spectral_handler():
            self.graph_viewer.layout.on_next(nx.spectral_layout)

        menu = tk.Menu(self.menubar)
        menu.add_command(label='Spring', command=spring_handler)
        menu.add_command(label='Shell', command=shell_handler)
        menu.add_command(label='Spectral', command=spectral_handler)
        self.menubar.add_cascade(label='Layouts', menu=menu)
        return menu

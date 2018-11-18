import tkinter as tk
import networkx as nx
from rx.subjects import BehaviorSubject

from graph_view import GraphViewer
from menu import Menu


class AppController:
    def __init__(self, *args, **kwargs):
        self.root = tk.Tk(*args, **kwargs)
        self.root.wm_protocol('WM_DELETE_WINDOW', self.root.quit)

        self.model = AppModel()
        self.view = AppView(self.root)
        self.model.G.subscribe(self.view.graph_viewer)
        self.view.create_menu(self.model.G)
        self.root.config(menu=self.view.menubar)

    def run(self):
        self.root.title('Simple Graph Vizualizator')
        self.root.deiconify()
        self.root.mainloop()


class AppModel:
    def __init__(self):
        self.G = BehaviorSubject(nx.Graph())


class AppView:
    def __init__(self, master):
        self.graph_viewer = GraphViewer(master)
        self.menubar = tk.Menu(master, tearoff=0)

    def create_menu(self, G):
        menu = Menu(self.menubar, self.graph_viewer)
        menu.create_menu_items(G)

import tkinter as tk
import networkx as nx
from rx.subjects import BehaviorSubject
from graph_view import GraphViewer
import menus


def main():
    G = BehaviorSubject(nx.Graph())
    root = tk.Tk()
    graph_viewer = GraphViewer(root)
    G.subscribe(graph_viewer)
    root.wm_protocol('WM_DELETE_WINDOW', root.quit)
    menubar = tk.Menu(root, tearoff=0)
    menus.file(menubar, G)
    menus.view(menubar, graph_viewer)
    menus.graphs(menubar, G)
    root.config(menu=menubar)
    tk.mainloop()


if __name__ == '__main__':
    main()

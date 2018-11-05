from tkinter import filedialog
import json


class ImportHandler:
    def __init__(self, graph):
        self._graph = graph

    def import_graph_from_file(self):
        filetypes = [('JSON', '*.json'), ('All Files', '*')]
        filename = filedialog.askopenfile(filetypes=filetypes).name
        return self.read_graph(filename)

    def read_graph(self, filename):
        with open(filename, 'r') as fp:
            data = json.load(fp)
        for point in data['points']:
            self._graph.add_node(point['idx'])
        for line in data['lines']:
            from_idx, to_idx = line['points']
            self._graph.add_edge(from_idx, to_idx, weight=line['length'])
        return self._graph

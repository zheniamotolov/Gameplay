from tkinter import filedialog
import json
from itertools import count


class ExportHandler:

    def export_graph_to_file(self, graph):
        filetypes = [('JSON', '*.json'), ('All Files', '*')]
        filename = filedialog.asksaveasfile(filetypes=filetypes).name
        self.write_graph(filename, graph)

    def write_graph(self, filename, graph):
        points = [{'idx': node, 'post_idx': None} for node in graph.nodes]
        lines = [{'idx': idx, 'length': 1, 'points': [x, y]} for idx, (x, y) in zip(count(1), graph.edges)]
        data = {'points': points, 'lines': lines}
        with open(filename, 'w') as fp:
            json.dump(data, fp)

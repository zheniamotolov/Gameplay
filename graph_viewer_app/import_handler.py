from tkinter import filedialog
import json



class ImportHandler:

    def import_graph_from_file(self, graph):
        filetypes = [('JSON', '*.json'), ('All Files', '*')]
        filename = filedialog.askopenfile(filetypes=filetypes).name
        return self.read_graph(filename, graph)

    def read_graph(self, filename, graph):
        with open(filename, 'r') as fp:
            data = json.load(fp)
        for point in data['points']:
            graph.add_node(point['idx'])
        for line in data['lines']:
            from_idx, to_idx = line['points']
            graph.add_edge(from_idx, to_idx, weight=line['length'])
        return graph

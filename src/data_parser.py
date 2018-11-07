import json
import networkx as nx
from itertools import count


class DataParser:
    def graph_from_file(self, filename):
        if filename is None:
            return

        G = nx.Graph()
        with open(filename, 'r') as fp:
            data = json.load(fp)
            for point in data['points']:
                G.add_node(point['idx'])
            for line in data['lines']:
                from_idx, to_idx = line['points']
                G.add_edge(from_idx, to_idx, weight=line['length'])
        return G

    def graph_to_file(self, G, filename):
        if filename is None:
            return

        points = [{'idx': node, 'post_idx': None} for node in G.nodes]
        lines = [
            {
                'idx': idx,
                'length': 1,
                'points': [x, y]
            } for idx, (x, y) in zip(count(1), G.edges)
        ]
        data = {'points': points, 'lines': lines}
        with open(filename, 'w') as fp:
            json.dump(data, fp)

from typing import List, Dict, Optional, Tuple
import heapq
import networkx as nx
import matplotlib.pyplot as plt

ufscar_vertex_label = "UFSCar"


class Vertex:
    def __init__(self, name: str):
        self.name: str = name

    def __repr__(self) -> str:
        return self.name


class Edge:
    def __init__(self, origin: Vertex, destination: Vertex, weight: float):
        self.origin: Vertex = origin
        self.destination: Vertex = destination
        self.weight: float = weight


class Graph:
    def __init__(self):
        self.vertices: Dict[str, Vertex] = {}
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = {}

    def add_vertex(self, vertex_name: str) -> None:
        if vertex_name not in self.vertices:
            self.vertices[vertex_name] = Vertex(vertex_name)
            self.adjacency_list[vertex_name] = []

    def add_edge(self, origin_name: str, destination_name: str, weight: float) -> None:
        self.add_vertex(origin_name)
        self.add_vertex(destination_name)
        self.adjacency_list[origin_name].append((destination_name, weight))
        self.adjacency_list[destination_name].append((origin_name, weight))

    def dijkstra(self, start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        distances = {name: float('inf') for name in self.vertices}
        distances[start] = 0.0
        predecessors = {name: None for name in self.vertices}

        heap = [(0.0, start)]
        while heap:
            current_distance, current_vertex = heapq.heappop(heap)
            for neighbor, weight in self.adjacency_list[current_vertex]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(heap, (distance, neighbor))

        return distances, predecessors

    def plot_shortest_path_tree(self, predecessors: Dict[str, Optional[str]]) -> None:
        graph = nx.Graph()
        for node, parent in predecessors.items():
            if parent:
                weight = next(w for neighbor, w in self.adjacency_list[parent] if neighbor == node)
                graph.add_edge(parent, node, weight=weight)

        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)

        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

        plt.title("Caminho mínimo da Ufscar")
        plt.show()


def read_vertices(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]


def read_edges(path: str) -> List[Edge]:
    edges = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            origin, destination, weight_str = line.strip().split(',')
            weight = float(weight_str)
            edges.append(Edge(Vertex(origin), Vertex(destination), weight))

    return edges


def main() -> None:
    vertex_names = read_vertices("graphs/grafo_sao_carlos_vertices.txt")
    edges = read_edges("graphs/grafo_sao_carlos_arestas.txt")

    graph = Graph()

    for name in vertex_names:
        graph.add_vertex(name)

    for edge in edges:
        graph.add_edge(edge.origin.name, edge.destination.name, edge.weight)

    if ufscar_vertex_label not in graph.vertices:
        print("The Ufscar vertex does not exist")
        return

    distances, predecessors = graph.dijkstra(ufscar_vertex_label)

    print("\nDistâncias da Ufscar:")
    for location, distance in distances.items():
        print(f"{location}: {distance:.2f} km")

    furthest = sorted(distances.items(), key=lambda x: x[1], reverse=True)[:3]
    print("\nTop 3 bairros mais distantes da Ufscar:")
    for neighborhood, distance in furthest:
        print(f"{neighborhood} - {distance:.2f} km")

    graph.plot_shortest_path_tree(predecessors)


if __name__ == "__main__":
    main()

'''
Author: Bartłomiej Jamiołkowski
Date: 28.10.2022
Topic: Aho-Corasick automaton
'''

# Klasa implementująca iterator
class GraphIterator:
    def __init__(self, visited_nodes):
        self.visited_nodes = visited_nodes

    def __iter__(self):
        self.visited_index = 0
        return self

    def __next__(self):
        try:
            visited_node = self.visited_nodes[self.visited_index]
            self.visited_index += 1
            return visited_node
        except IndexError:
            raise StopIteration


# Klasa reprezentująca graf
class Graph:
    def __init__(self):
        self.graph_dict = {}  # Słownik, w którym klucz to wierzchołek a wartośc to lista sąsiadów

    def add_node(self, new_node):
        if new_node not in self.graph_dict:  # Unikanie duplikatów wierzchołków
            self.graph_dict[new_node] = []

    def add_edge(self, node_one, node_two):
        if node_one and node_two in self.graph_dict:  # Krawędź można dodać tylko pomiędzy istniejące wierzchołki
            self.graph_dict[node_one] += [node_two]
            self.graph_dict[node_two] += [node_one]

    def get_neighbours(self, node):
        if node in self.graph_dict:
            node_neighbours = list(self.graph_dict[node])
            return node_neighbours

    def remove_node(self, rem_node):
        if rem_node in self.graph_dict:  # Sprawdzanie czy można usunąc istniejący wierzchołek
            linked_nodes = list(self.graph_dict.get(rem_node))  # Lista sasiadow usuwanego wierchołka
            for linked_node in linked_nodes:  # Z każdego sąsiada usuwana jest informacja o wierzchołku
                linked_node_neighbours = list(self.graph_dict.get(linked_node))  # Lista sąsiadów sąsiada
                linked_node_neighbours.remove(rem_node) # Usunięcie wierzchołka z listy sąsiadów sąsiada wierzchołka
                self.graph_dict[linked_node] = linked_node_neighbours

            del self.graph_dict[rem_node]  # Usuniecie wierzchołka jako klucza slownika

    def remove_edge(self, node_one, node_two):
        if node_one in self.graph_dict[node_two] and node_two in self.graph_dict[node_one]:  # Sprawdzenie czy istnieje krawędź
            node_one_neighbours = list(self.graph_dict[node_one])  # Lista sąsiadów wierzchołka 1
            node_one_neighbours.remove(node_two)  # Usunięcie sąsaiada wierzchołek 2
            self.graph_dict[node_one] = node_one_neighbours

            node_two_neighbours = list(self.graph_dict[node_two])  # Lista sąsiadów wierzchołka 2
            node_two_neighbours.remove(node_one)
            self.graph_dict[node_two] = node_two_neighbours

    def bfs(self, root):
        queue, visited_nodes = [], []
        queue.append(root)
        visited_nodes.append(root)

        while len(queue) > 0:
            node = queue[0]
            queue.pop(0)
            for neighbor in self.graph_dict[node]:
                if neighbor not in visited_nodes:
                    queue.append(neighbor)
                    visited_nodes.append(neighbor)

        return GraphIterator(visited_nodes)

    def dfs(self, root):  # Nierencyjna implementacja algorytmu BFS
        stack, visited_nodes = [], []
        stack.append(root)
        while len(stack) > 0:
            node = stack.pop()
            if node not in visited_nodes:
                visited_nodes.append(node)
                for neighbour in self.graph_dict[node]:
                    stack.append(neighbour)

        return GraphIterator(visited_nodes)


if __name__ == '__main__':
    # Stworzenie i sprawdzenie grafu
    graph = Graph()
    node_list = ["A", "B", "C", "D", "E", "F", "G", "H"]
    edge_list = [["A", "B"], ["A", "C"], ["A", "E"], ["B", "D"], ["B", "F"], ["C", "G"], ["F", "E"], ["G", "H"]]

    for new_node in node_list:
        graph.add_node(new_node)

    for new_edge in edge_list:
        node_one, node_two = new_edge[0], new_edge[1]
        graph.add_edge(node_one, node_two)

    print(graph.graph_dict)

    neighbours = graph.get_neighbours("A")
    print(neighbours)

    graph.remove_edge("G", "H")
    print(graph.graph_dict)

    graph.remove_node("H")
    print(graph.graph_dict)

    print("Metoda BFS:")
    for bfs_node in graph.bfs("A"):
        print(bfs_node)

    print("Metoda DFS")
    for dfs_node in graph.dfs("A"):
        print(dfs_node)
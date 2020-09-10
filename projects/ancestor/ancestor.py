class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertices(self, vertex_id):
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)

    def add_node(self, v1, v2):
        if v1 not in self.vertices:
            self.add_vertices(v1)
        if v2 not in self.vertices:
            self.add_vertices(v2)
        self.vertices[v1].add(v2)

    def get_parents(self, vertex_id):
        parents_list = []
        for item in self.vertices[vertex_id]:
            parents_list.append(item)
        return parents_list

    def dfs(self, starting_vertex):
        s = Stack()
        s.push([starting_vertex])
        visited = set()
        out = []
        while s.size() > 0:
            path = s.pop()
            v = path[-1]
            if v not in visited:
                if len(self.get_parents(v)) < 1:
                    out.append(path)
                visited.add(v)
                for n in self.get_parents(v):
                    if n not in visited:
                        s.push(path + [n])
        return out

def earliest_ancestor(ancestors_list, starting_node):
    out = -1
    graph = Graph()
    for pair in ancestors_list:
        graph.add_node(pair[1], pair[0])
    search = graph.dfs(starting_node)
    if len(search) > 1:
        path_length = 0
        solution_path = []
        for path in search:
            if len(path) > path_length:
                path_length = len(path)
                solution_path = path
            elif len(path) == path_length:
                if path[-1] < solution_path[-1]:
                    solution_path = path
        solution_array = solution_path
    else:
        solution_array = search[0]
    if len(solution_array) > 1:
        out = solution_array[-1]
    return out
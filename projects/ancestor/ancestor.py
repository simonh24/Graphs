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

def earliest_ancestor(ancestors, starting_node):
    dict_ancestor = {}
    to_visit = Stack()
    visited = set()
    longest_path = []

    for i, x in enumerate(ancestors):
        dict_ancestor[i] = x

    for i, v in dict_ancestor.items():
        if v[1] is starting_node:
            to_visit.push([i])

    size = to_visit.size()

    if to_visit.size() > 0:
        while to_visit.size() > 0:
            path = to_visit.pop()
            v = path[-1]
            if v not in visited:
                visited.add(v)
                parent = dict_ancestor[v][0]
                for i, n in dict_ancestor.items():
                    if n[1] is parent:
                        new_path = path + [i]
                        to_visit.push(new_path)
                        if len(new_path) > len(longest_path):
                            longest_path = new_path
                    elif i == len(dict_ancestor) - 1:
                        longest_path = path
        final_answer = (dict_ancestor[longest_path[-1]][0])
        return final_answer 
    else:
        return -1
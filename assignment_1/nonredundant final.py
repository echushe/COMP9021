import sys

sys.setrecursionlimit(1000000)


class InputData(object):
    def __init__(self, graph, order):
        self.graph = graph
        self.order = order

    def get_graph(self):
        return self.graph

    def get_order(self):
        return self.order


class Vertex(object):
    def __init__(self, key):
        self.id = key
        self.adj = {}

    def add_neighbor(self, nbr, weight=0):
        self.adj[nbr] = weight

    def remove_neighbor(self, nbr):
        if nbr in self.adj:
            del self.adj[nbr]

    def get_neighbors(self):
        return self.adj.keys()

    def get_id(self):
        return self.id

    def get_weight(self, key):
        return self.adj[key]

    def get_all_sub(self, sub):
        aaa = self.get_neighbors()
        for temp in aaa:
            if not (temp in sub):
                sub.add(temp)
                temp.get_all_sub(sub)
        return sub


class DGraph(object):
    def __init__(self):
        self.vertex_list = {}
        self.size = 0

    def add_vertex(self, key):
        vertex = Vertex(key)
        self.vertex_list[key] = vertex
        self.size += 1
        return vertex

    def get_vertex(self, key):
        return self.vertex_list.get(key)

    def __contains__(self, key):
        if key in self.vertex_list:
            return True
        else:
            return False

    def add_edge(self, f, t, weight=0):
        if f not in self.vertex_list:
            self.add_vertex(f)
        if t not in self.vertex_list:
            self.add_vertex(t)
        self.vertex_list[f].add_neighbor(self.vertex_list[t], weight)

    def remove_edge(self, f, t):
        self.vertex_list[f].remove_neighbor(self.vertex_list[t])

    def get_vertices(self):
        return self.vertex_list.keys()

    def __iter__(self):
        return iter(self.vertex_list.values())

    def get_edge(self):
        edges = []
        vertices = self.get_vertices()
        for key in vertices:
            vertex = self.get_vertex(key)
            nbrs = vertex.get_neighbors()
            for nbr in nbrs:
                edge = [key, nbr.get_id()]
                edges.append(edge)
        return edges


def is_connected(start_vertex, end_vertex):
    connected_map = {}
    key = str(start_vertex.get_id()) + '-' + str(end_vertex.get_id())
    if not (key in connected_map):
        vertex_connected = check_connected(start_vertex, end_vertex)
        connected_map.setdefault(key, vertex_connected)
    return connected_map.get(key)


def check_connected(start_vertex, end_vertex):
    sub = set()
    start_vertex.get_all_sub(sub)
    for vertex_temp in sub:
        if vertex_temp.get_id() == end_vertex.get_id():
            return True
    return False


def top_sort(graph):
    top = []
    queue = []
    degree = {}
    for v in graph:
        degree[v] = 0
    for v in graph:
        for w in v.get_neighbors():
            degree[w] += 1
    for v in degree:
        if degree[v] == 0:
            queue.append(v)
    while queue:
        v = queue.pop(0)
        top.append(v)
        for i in v.get_neighbors():
            degree[i] -= 1
            if degree[i] == 0:
                queue.append(i)
    return top


def prune(graph, order):
    deque = top_sort(graph)
    for vertex in deque:
        prune_edge(vertex, order, deque)


def prune_edge(vertex, order, deque):
    target_dict = {}
    neighbors = vertex.get_neighbors()
    for nbr in neighbors:
        index = deque.index(nbr)
        target_dict.setdefault(index, nbr)
    # order
    if len(target_dict) > 0:
        dict_item = sorted(target_dict.items(), key=lambda d: d[0])
        targets = []
        for key, value in dict_item:
            targets.append(value)
        m = len(targets)
        for i in range(m):
            for j in range(i + 1, m):
                child1 = targets[i]
                child2 = targets[j]
                flag = is_connected(child1, child2)
                if flag:
                    remove_temp = "R({},{})".format(vertex.get_id(), child2.get_id())
                    if remove_temp in order:
                        order.remove(remove_temp)


def input_file():
    graph = DGraph()
    order = []
    file_name = input('Which data file do you want to use?')
    if file_name:
        try:
            with open(file_name, "r") as f:
                for line in f:
                    order.append(line.strip('\n'))
                    vertexs = line.strip('R').strip('(').strip(')\n').split(',')
                    v1 = vertexs[0]
                    v2 = vertexs[1]
                    graph.add_edge(v1, v2)
        except IOError:
            print("Data file is error!")
            exit()
    else:
        print("Data file does not exist!")
        exit()
    input_data = InputData(graph, order)
    return input_data


if __name__ == "__main__":
    this_ret = input_file()
    this_graph = this_ret.get_graph()
    this_order = this_ret.get_order()
    prune(this_graph, this_order)
    print('The nonredundant facts are:')
    for od in this_order:
        print(od)

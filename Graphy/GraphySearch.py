# GraphySearch, parent = GraphyRunSearchDialog

from collections import deque


class GraphySearch:

    def __init__(self, parent):

        # hierarchy
        self.parent = parent
        self.graphy = parent.graphy
        self.graphy.search = self

        # search protocols (set by set_search_type)
        self.search_setup = None
        self.search_step_forward = None
        self.search_step_back = None

        # graph references
        self.start_vertex = None
        self.end_vertex = None

        # search data
        self.predecessors = dict()
        self.traversal_weights = dict()
        self.heuristic_weights = dict()

        # playback data
        self.forward_stack = deque()
        self.back_stack = deque()

    def set_search_type(self, search_type):
        self.set_search_to_start()
        self.forward_stack = deque()
        self.back_stack = deque()
        self.predecessors = dict()
        self.traversal_weights = dict()
        if search_type == "Simple Breadth-First":
            self.search_setup = self.simple_bfs_setup
            self.search_step_forward = self.simple_forward
            self.search_step_back = self.simple_back
        elif search_type == "Simple Depth-First":
            self.search_setup = self.simple_dfs_setup
            self.search_step_forward = self.simple_forward
            self.search_step_back = self.simple_back
        elif search_type == "Weighted Breadth-First":
            self.search_setup = self.weighted_bfs_setup
            self.search_step_forward = self.weighted_bfs_forward
            self.search_step_back = self.weighted_bfs_back
        elif search_type == "Weighted Depth-First":
            self.search_setup = self.simple_bfs_setup
            self.search_step_forward = self.simple_forward
            self.search_step_back = self.simple_back
        elif search_type == "A*":
            # todo
            self.search_setup = self.simple_bfs_setup
            self.search_step_forward = self.simple_forward
            self.search_step_back = self.simple_back
        else:
            print('invalid search type selected')

    def set_search_to_start(self):
        while self.back_stack:
            self.search_step_back()

    def set_search_to_end(self):
        while self.forward_stack:
            self.search_step_forward()

    def simple_bfs_setup(self):
        print('setting up simple BFS')
        self.predecessors = dict()
        self.predecessors[self.start_vertex.id] = None
        self.forward_stack = deque()
        self.back_stack = deque()
        move = []
        end_id = self.end_vertex.id
        frontier = set()
        for vertex_id in self.start_vertex.neighbors:
            self.predecessors[vertex_id] = self.start_vertex.id
            frontier.add(vertex_id)
            if vertex_id != end_id:
                move.append((vertex_id, 'Unexplored', 'Frontier'))
        if move:
            self.forward_stack.append(move)

        frontier = deque(frontier)
        while frontier and end_id not in self.predecessors:
            move = []
            frontier_id = frontier.popleft()
            move.append((frontier_id, 'Frontier', 'Explored'))
            neighborhood = self.graphy.vertices[frontier_id].neighbors
            for neighbor_id in neighborhood:
                if neighbor_id not in self.predecessors:
                    self.predecessors[neighbor_id] = frontier_id
                    frontier.append(neighbor_id)
                    if not neighbor_id == end_id:
                        move.append((neighbor_id, "Unexplored", "Frontier"))
            if move:
                self.forward_stack.append(move)

        if end_id in self.predecessors:
            move = []
            previous_id = self.predecessors[end_id]
            while previous_id:
                edge_id = self.graphy.vertices[end_id].neighbors[previous_id].id
                move.append((edge_id, "Default", "Highlighted"))
                end_id = previous_id
                previous_id = self.predecessors[previous_id]
            if move:
                self.forward_stack.append(move)

    def simple_dfs_setup(self):
        print('setting up simple DFS')
        self.predecessors = dict()
        self.predecessors[self.start_vertex.id] = None
        self.forward_stack = deque()
        self.back_stack = deque()
        move = []
        end_id = self.end_vertex.id
        frontier = set()
        for vertex_id in self.start_vertex.neighbors:
            self.predecessors[vertex_id] = self.start_vertex.id
            frontier.add(vertex_id)
            if vertex_id != end_id:
                move.append((vertex_id, 'Unexplored', 'Frontier'))
        if move:
            self.forward_stack.append(move)

        frontier = deque(frontier)
        while frontier and end_id not in self.predecessors:
            move = []
            frontier_id = frontier.pop()
            move.append((frontier_id, 'Frontier', 'Explored'))
            neighborhood = self.graphy.vertices[frontier_id].neighbors
            for neighbor_id in neighborhood:
                if neighbor_id not in self.predecessors:
                    self.predecessors[neighbor_id] = frontier_id
                    frontier.append(neighbor_id)
                    if not neighbor_id == end_id:
                        move.append((neighbor_id, "Unexplored", "Frontier"))
            if move:
                self.forward_stack.append(move)

        if end_id in self.predecessors:
            move = []
            previous_id = self.predecessors[end_id]
            while previous_id:
                edge_id = self.graphy.vertices[end_id].neighbors[previous_id].id
                move.append((edge_id, "Default", "Highlighted"))
                end_id = previous_id
                previous_id = self.predecessors[previous_id]
            if move:
                self.forward_stack.append(move)

    def simple_forward(self):
        if self.forward_stack:
            move = self.forward_stack.popleft()
            if move[0][0] in self.graphy.vertices:
                for (vertex_id, state1, state2) in move:
                    self.graphy.vertices[vertex_id].set_status(state2)
            else:
                for (edge_id, state1, state2) in move:
                    self.graphy.edges[edge_id].set_status(state2)
            self.back_stack.append(move)

    def simple_back(self):
        if self.back_stack:
            move = self.back_stack.pop()
            if move[0][0] in self.graphy.vertices:
                for (vertex_id, state1, state2) in move:
                    self.graphy.vertices[vertex_id].set_status(state1)
            else:
                for (edge_id, state1, state2) in move:
                    self.graphy.edges[edge_id].set_status(state1)
            self.forward_stack.appendleft(move)

    def weighted_bfs_setup(self):
        print('setting up weighted BFS')
        self.predecessors = dict()
        self.predecessors[self.start_vertex.id] = None
        self.traversal_weights[self.start_vertex.id] = 0
        self.forward_stack = deque()
        self.back_stack = deque()
        move = []
        end_id = self.end_vertex.id
        frontier = set()
        for vertex_id in self.start_vertex.neighbors:
            self.predecessors[vertex_id] = self.start_vertex.id
            weight = self.start_vertex.neighbors[vertex_id].weight
            self.traversal_weights[vertex_id] = weight
            frontier.add(vertex_id)
            if vertex_id != end_id:
                move.append((vertex_id, 'Unexplored', 'Frontier', None, weight))
        if move:
            self.forward_stack.append(move)

        while frontier and end_id not in self.predecessors:
            move = []
            frontier_id = min(frontier, key=lambda x: self.traversal_weights[x])
            frontier.remove(frontier_id)
            frontier_weight = self.traversal_weights[frontier_id]
            move.append((frontier_id, 'Frontier', 'Explored', frontier_weight, None))
            neighborhood = self.graphy.vertices[frontier_id].neighbors
            for neighbor_id in neighborhood:
                weight = self.graphy.vertices[neighbor_id].neighbors[frontier_id].weight + frontier_weight
                go = neighbor_id not in self.predecessors
                if not go:
                    go = weight < self.traversal_weights[neighbor_id]
                if go:
                    self.predecessors[neighbor_id] = frontier_id
                    self.traversal_weights[neighbor_id] = weight
                    if not neighbor_id == end_id:
                        frontier.add(neighbor_id)
                        move.append((neighbor_id, "Unexplored", "Frontier", None, weight))
                    else:
                        move.append((neighbor_id, "End", "End", None, weight))
            if move:
                self.forward_stack.append(move)

        while frontier:
            move = []
            frontier_id = min(frontier, key=lambda x: self.traversal_weights[x])
            frontier.remove(frontier_id)
            frontier_weight = self.traversal_weights[frontier_id]
            if frontier_weight >= self.traversal_weights[end_id]:
                break
            move.append((frontier_id, 'Frontier', 'Explored', frontier_weight, None))
            neighborhood = self.graphy.vertices[frontier_id].neighbors
            for neighbor_id in neighborhood:
                weight = self.graphy.vertices[neighbor_id].neighbors[frontier_id].weight + frontier_weight
                go = neighbor_id not in self.predecessors
                if not go:
                    go = weight < self.traversal_weights[neighbor_id]
                if go:
                    self.predecessors[neighbor_id] = frontier_id
                    self.traversal_weights[neighbor_id] = weight
                    if not neighbor_id == end_id:
                        frontier.add(neighbor_id)
                        move.append((neighbor_id, "Unexplored", "Frontier", None, weight))
                    else:
                        move.append((neighbor_id, "End", "End", None, weight))
            if move:
                self.forward_stack.append(move)

        if end_id in self.predecessors:
            move = []
            previous_id = self.predecessors[end_id]
            while previous_id:
                edge_id = self.graphy.vertices[end_id].neighbors[previous_id].id
                move.append((edge_id, "Default", "Highlighted"))
                end_id = previous_id
                previous_id = self.predecessors[previous_id]
            if move:
                self.forward_stack.append(move)

    def weighted_bfs_forward(self):
        if self.forward_stack:
            move = self.forward_stack.popleft()
            if move[0][0] in self.graphy.vertices:
                for (vertex_id, state1, state2, weight1, weight2) in move:
                    vertex = self.graphy.vertices[vertex_id]
                    vertex.set_status(state2)
                    vertex.display_weight(weight2)
            else:
                for (edge_id, state1, state2) in move:
                    self.graphy.edges[edge_id].set_status(state2)
            self.back_stack.append(move)

    def weighted_bfs_back(self):
        if self.back_stack:
            move = self.back_stack.pop()
            if move[0][0] in self.graphy.vertices:
                for (vertex_id, state1, state2, weight1, weight2) in move:
                    vertex = self.graphy.vertices[vertex_id]
                    vertex.set_status(state1)
                    vertex.display_weight(weight1)
            else:
                for (edge_id, state1, state2) in move:
                    self.graphy.edges[edge_id].set_status(state1)
            self.forward_stack.appendleft(move)

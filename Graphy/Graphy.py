# master class

from tkinter import *
from PIL import Image, ImageTk
from GraphyMenuBar import GraphyMenuBar
from GraphyVertexSpawnButton import GraphyVertexSpawnButton
from GraphyVertex import GraphyVertex
from GraphyEdge import GraphyEdge
from GraphyInspector import GraphyInspector
from GraphyLegend import GraphyLegend
from collections import deque


class Graphy:

    def __init__(self):

        # window
        self.tk = Tk()
        self.tk.title("Graphy")

        # frame on left (canvas)
        self.left_frame = Frame(self.tk)
        self.left_frame.pack(side=LEFT)
        self.can = Canvas(self.left_frame)

        # frame on right (inspector, legend, ...)
        self.right_frame_width = 30
        self.right_frame_padding = 4
        self.right_frame = Frame(self.tk)
        self.right_frame.pack(side=RIGHT, fill='both')
        self.inspector = GraphyInspector(self)

        self.canvas_width = 1000
        self.canvas_height = 500
        self.can.config(width=self.canvas_width,
                        height=self.canvas_height,
                        background='white',
                        highlightthickness=0)
        self.can.grid(column=0, row=0, sticky=(N, W, E, S))

        # get padding for canvas resizing
        self.can.update()
        self.tk.update()
        self.canvas_padding = self.tk.winfo_width() - self.can.winfo_width()

        # top menu
        self.menubar = GraphyMenuBar(self)

        # graph utilities
        self.vertices = dict()  # vertex.id --> GraphyVertex object
        self.vertex_count = 0
        self.edges = dict()  # edge.id --> GraphyEdge object
        self.edge_count = 0
        self.vertex_spawn = GraphyVertexSpawnButton(self)

        # playback stacks and utils
        self.forward_stack = None  # popleft() to get move forward
        self.back_stack = None  # popright() to get get move backward
        self.predecessors = dict()
        self.traversal_weights = dict()
        self.search_setup = None
        self.search_step_forward = None
        self.search_step_back = None

        # selection and movement tracking
        self.held_vertex = None
        self.held_edge = None
        self.dragged_edge = None
        self.dragged_edge_offsets = None
        self.selected = None
        self.selected_icon_id = None
        self.is_setting_search_vertex = False
        self.start_vertex = None
        self.end_vertex = None
        self.is_setting_scale_edge = False
        self.scale_edge = None

        # vertex images
        self.vertex_size = 20

        # start vertex
        start_vertex_image = Image.open("images/StartVertex.png")
        start_vertex_image = start_vertex_image.resize((self.vertex_size, self.vertex_size), Image.ANTIALIAS)
        self.start_vertex_image = ImageTk.PhotoImage(start_vertex_image)

        # unexplored vertex
        unexplored_vertex_image = Image.open("images/UnexploredVertex.png")
        unexplored_vertex_image = unexplored_vertex_image.resize((self.vertex_size, self.vertex_size), Image.ANTIALIAS)
        self.unexplored_vertex_image = ImageTk.PhotoImage(unexplored_vertex_image)

        # frontier vertex
        frontier_vertex_image = Image.open("images/FrontierVertex.png")
        frontier_vertex_image = frontier_vertex_image.resize((self.vertex_size, self.vertex_size), Image.ANTIALIAS)
        self.frontier_vertex_image = ImageTk.PhotoImage(frontier_vertex_image)

        # explored vertex
        explored_vertex_image = Image.open("images/ExploredVertex.png")
        explored_vertex_image = explored_vertex_image.resize((self.vertex_size, self.vertex_size), Image.ANTIALIAS)
        self.explored_vertex_image = ImageTk.PhotoImage(explored_vertex_image)

        # end vertex
        end_vertex_image = Image.open("images/EndVertex.png")
        end_vertex_image = end_vertex_image.resize((self.vertex_size, self.vertex_size), Image.ANTIALIAS)
        self.end_vertex_image = ImageTk.PhotoImage(end_vertex_image)

        # selected vertex image (red outline)
        self.selected_icon_size = int(1.25 * self.vertex_size)
        selected_vertex_image = Image.open("images/SelectedVertexIcon.png")
        selected_vertex_image = selected_vertex_image.resize((self.selected_icon_size,
                                                             self.selected_icon_size),
                                                             Image.ANTIALIAS)
        self.selected_vertex_image = ImageTk.PhotoImage(selected_vertex_image)

        # legend
        self.legend = GraphyLegend(self)

        # controls
        self.tk.bind("<Configure>", self.resize)  # on resize
        self.can.bind("<Motion>", self.motion)  # on mouse movement over canvas
        self.can.bind("<Button-1>", self.click)  # left click to create
        self.can.bind("<Button-2>", self.mclick)  # middle click to select
        self.can.bind("<Button-3>", self.rclick)  # right click to move
        self.tk.bind("<Return>", self.change_vertex)  # press enter to change status
        self.mousex = 0
        self.mousey = 0

        # quit
        self.isPlaying = True
        self.tk.protocol('WM_DELETE_WINDOW', self.quit)

    def mainloop(self):
        while self.isPlaying:
            self.can.update()
            self.tk.update()
        self.tk.destroy()

    # when the window gets resized:
    def resize(self, event):

        # get new values
        new_width = self.tk.winfo_width() - self.canvas_padding
        new_height = self.tk.winfo_height()

        # set new values
        self.canvas_width = new_width
        self.canvas_height = new_height

        # adjust canvas dimensions
        self.can.config(width=self.canvas_width, height=self.canvas_height)

        # reposition the vertex creation button
        self.vertex_spawn.resize()

    # mouse movement
    def motion(self, event):
        if self.held_vertex:
            self.held_vertex.update_position(event.x, event.y)
        elif self.held_edge:
            self.held_edge.update_trailing_end(event.x, event.y)
        elif self.dragged_edge:
            (x1, y1, x2, y2) = self.dragged_edge_offsets
            x1 += event.x
            y1 += event.y
            x2 += event.x
            y2 += event.y
            self.dragged_edge.update_position(x1, y1, x2, y2)
        self.mousex = event.x
        self.mousey = event.y

    # left click on canvas; probably rename "canvas_click" when there are other things to click
    def click(self, event):

        # drop the edge you're dragging
        if self.dragged_edge:
            self.dragged_edge = None

        # drop the vertex being dragged
        elif self.held_vertex:
            self.held_vertex = None

        # attempt to attach half-created edge to second endpoint
        elif self.held_edge:
            item = self.can.find_closest(event.x, event.y)[0]
            if item == self.selected_icon_id:
                item = self.selected.id
            if item in self.vertices:
                self.held_edge.attach_second_vertex(self.vertices[item])
            else:
                print('unfinished edge deleted')
                self.held_edge.die()
            self.held_edge = None

        # set start/end vertex if choosing search params
        elif self.is_setting_search_vertex:
            item = self.can.find_closest(event.x, event.y)[0]
            if item == self.selected_icon_id:
                item = self.selected.id
            if item in self.vertices:
                self.set_search_vertex(self.vertices[item])
            self.is_setting_search_vertex = False
            self.menubar.search_window.get_focus()

        elif self.is_setting_scale_edge:
            item = self.can.find_closest(event.x, event.y)[0]
            if item == self.selected_icon_id:
                item = self.selected.id
            if item in self.edges:
                self.set_scale_edge(self.edges[item])
            self.is_setting_scale_edge = False
            self.menubar.weight_window.get_focus()

        else:
            item = self.can.find_closest(event.x, event.y)[0]
            if item == self.selected_icon_id:
                item = self.selected.id
            if item in self.vertices:
                self.create_edge(self.vertices[item], event)
                print('edge started')

    def mclick(self, event):
        if not (self.held_vertex or self.held_edge or self.dragged_edge):
            item = self.can.find_closest(event.x, event.y)[0]
            if item == self.selected_icon_id:
                self.selected.set_unselected()
            elif item in self.vertices:
                if self.selected and self.selected.id != item:
                    self.selected.set_unselected()
                self.selected = self.vertices[item]
                self.selected.set_selected()
            elif item in self.edges:
                if self.selected and self.selected.id != item:
                    self.selected.set_unselected()
                self.selected = self.edges[item]
                self.selected.set_selected()

    def rclick(self, event):
        if not (self.held_edge or self.held_vertex):
            item = self.can.find_closest(event.x, event.y)[0]
            if item == self.selected_icon_id:
                item = self.selected.id
            if item in self.vertices:
                self.held_vertex = self.vertices[item]
            elif item in self.edges:
                self.dragged_edge = self.edges[item]
                self.dragged_edge_offsets = self.can.coords(item)
                self.dragged_edge_offsets[0] -= event.x
                self.dragged_edge_offsets[2] -= event.x
                self.dragged_edge_offsets[1] -= event.y
                self.dragged_edge_offsets[3] -= event.y

    # todo haven't been able to use this yet
    def change_vertex(self, event):
        if self.held_vertex:
            self.held_vertex.can.itemconfig(self.held_vertex.id, image=self.start_vertex_image)
            self.held_vertex.set_status('Start')
            self.inspector.update()

    def create_unexplored_vertex(self, event):
        if not self.held_vertex:
            self.held_vertex = GraphyVertex(self,
                                            self.unexplored_vertex_image,
                                            'Unexplored',
                                            self.mousex,
                                            self.mousey)
            self.vertices[self.held_vertex.id] = self.held_vertex
            self.vertex_count += 1
            self.held_vertex.set_label(self.vertex_count)

    def set_search_vertex(self, vertex):
        if self.is_setting_search_vertex == 'Start':
            if self.start_vertex:
                self.start_vertex.set_default()
            vertex.set_status('Start')
            self.start_vertex = vertex
        elif self.is_setting_search_vertex == 'End':
            if self.end_vertex:
                self.end_vertex.set_default()
            vertex.set_status('End')
            self.end_vertex = vertex
        self.inspector.update()

    def create_edge(self, vertex, event):
        self.edge_count += 1
        self.held_edge = GraphyEdge(self, vertex, event)
        self.held_edge.set_label(self.edge_count)

    def set_scale_edge(self, edge):
        self.menubar.weight_window.set_scale(edge.get_weight_scale())

    def set_edge_weights(self, scale):
        for edge in self.edges.values():
            edge.set_weight_from_scale(scale)

    def set_search_type(self, search_type):
        self.set_search_to_start()
        self.forward_stack = deque()
        self.back_stack = deque()
        self.predecessors = dict()
        self.traversal_weights = dict()
        if search_type == "Simple Breadth-First":
            self.search_setup = self.simple_bfs_setup
            self.search_step_forward = self.simple_bfs_forward
            self.search_step_back = self.simple_bfs_back
        elif search_type == "Simple Depth-First":
            # todo
            self.search_setup = self.simple_dfs_setup
            self.search_step_forward = self.simple_bfs_forward  # simple bfs and dfs can use same stack controls
            self.search_step_back = self.simple_bfs_back
        elif search_type == "Weighted Breadth-First":
            # todo
            self.search_setup = self.weighted_bfs_setup
            self.search_step_forward = self.weighted_bfs_forward
            self.search_step_back = self.weighted_bfs_back
        elif search_type == "Weighted Depth-First":
            # todo
            self.search_setup = self.simple_bfs_setup
            self.search_step_forward = self.simple_bfs_forward
            self.search_step_back = self.simple_bfs_back
        elif search_type == "A*":
            # todo
            self.search_setup = self.simple_bfs_setup
            self.search_step_forward = self.simple_bfs_forward
            self.search_step_back = self.simple_bfs_back
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
        self.forward_stack.append(move)

        frontier = deque(frontier)
        while frontier and end_id not in self.predecessors:
            move = []
            frontier_id = frontier.popleft()
            move.append((frontier_id, 'Frontier', 'Explored'))
            neighborhood = self.vertices[frontier_id].neighbors
            for neighbor_id in neighborhood:
                if neighbor_id not in self.predecessors:
                    self.predecessors[neighbor_id] = frontier_id
                    frontier.append(neighbor_id)
                    if not neighbor_id == end_id:
                        move.append((neighbor_id, "Unexplored", "Frontier"))
            self.forward_stack.append(move)

        if end_id in self.predecessors:
            move = []
            previous_id = self.predecessors[end_id]
            while previous_id:
                edge_id = self.vertices[end_id].neighbors[previous_id].id
                move.append((edge_id, "Default", "Highlighted"))
                end_id = previous_id
                previous_id = self.predecessors[previous_id]
            self.forward_stack.append(move)

    def simple_bfs_forward(self):
        if self.forward_stack:
            move = self.forward_stack.popleft()
            if move[0][0] in self.vertices:
                for (vertex_id, state1, state2) in move:
                    self.vertices[vertex_id].set_status(state2)
            else:
                for (edge_id, state1, state2) in move:
                    self.edges[edge_id].set_status(state2)
            self.back_stack.append(move)

    def simple_bfs_back(self):
        if self.back_stack:
            move = self.back_stack.pop()
            if move[0][0] in self.vertices:
                for (vertex_id, state1, state2) in move:
                    self.vertices[vertex_id].set_status(state1)
            else:
                for (edge_id, state1, state2) in move:
                    self.edges[edge_id].set_status(state1)
            self.forward_stack.appendleft(move)

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
        self.forward_stack.append(move)

        frontier = deque(frontier)
        while frontier and end_id not in self.predecessors:
            move = []
            frontier_id = frontier.pop()
            move.append((frontier_id, 'Frontier', 'Explored'))
            neighborhood = self.vertices[frontier_id].neighbors
            for neighbor_id in neighborhood:
                if neighbor_id not in self.predecessors:
                    self.predecessors[neighbor_id] = frontier_id
                    frontier.append(neighbor_id)
                    if not neighbor_id == end_id:
                        move.append((neighbor_id, "Unexplored", "Frontier"))
            self.forward_stack.append(move)

        if end_id in self.predecessors:
            move = []
            previous_id = self.predecessors[end_id]
            while previous_id:
                edge_id = self.vertices[end_id].neighbors[previous_id].id
                move.append((edge_id, "Default", "Highlighted"))
                end_id = previous_id
                previous_id = self.predecessors[previous_id]
            self.forward_stack.append(move)

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
        self.forward_stack.append(move)

        while frontier and end_id not in self.predecessors:
            move = []
            frontier_id = min(frontier, key=lambda x:self.traversal_weights[x])
            frontier.remove(frontier_id)
            frontier_weight = self.traversal_weights[frontier_id]
            move.append((frontier_id, 'Frontier', 'Explored', frontier_weight, None))
            neighborhood = self.vertices[frontier_id].neighbors
            for neighbor_id in neighborhood:
                weight = self.vertices[neighbor_id].neighbors[frontier_id].weight + frontier_weight
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
            self.forward_stack.append(move)

        while frontier:
            move = []
            frontier_id = min(frontier, key=lambda x: self.traversal_weights[x])
            frontier.remove(frontier_id)
            frontier_weight = self.traversal_weights[frontier_id]
            if frontier_weight >= self.traversal_weights[end_id]:
                break
            move.append((frontier_id, 'Frontier', 'Explored', frontier_weight, None))
            neighborhood = self.vertices[frontier_id].neighbors
            for neighbor_id in neighborhood:
                weight = self.vertices[neighbor_id].neighbors[frontier_id].weight + frontier_weight
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
            self.forward_stack.append(move)

        if end_id in self.predecessors:
            move = []
            previous_id = self.predecessors[end_id]
            while previous_id:
                edge_id = self.vertices[end_id].neighbors[previous_id].id
                move.append((edge_id, "Default", "Highlighted"))
                end_id = previous_id
                previous_id = self.predecessors[previous_id]
            #end_id = self.end_vertex.id
            #move.append((end_id, "End", "End", None, self.traversal_weights[end_id]))
            self.forward_stack.append(move)

    def weighted_bfs_forward(self):
        if self.forward_stack:
            move = self.forward_stack.popleft()
            if move[0][0] in self.vertices:
                for (vertex_id, state1, state2, weight1, weight2) in move:
                    vertex = self.vertices[vertex_id]
                    vertex.set_status(state2)
                    vertex.display_weight(weight2)
            else:
                for (edge_id, state1, state2) in move:
                    self.edges[edge_id].set_status(state2)
                #(end_id, state1, state2, weight1, weight2) = move[-1]
                #self.vertices[end_id].display_weight(weight2)
            self.back_stack.append(move)

    def weighted_bfs_back(self):
        if self.back_stack:
            move = self.back_stack.pop()
            if move[0][0] in self.vertices:
                for (vertex_id, state1, state2, weight1, weight2) in move:
                    vertex = self.vertices[vertex_id]
                    vertex.set_status(state1)
                    vertex.display_weight(weight1)
            else:
                for (edge_id, state1, state2) in move:
                    self.edges[edge_id].set_status(state1)
                #(end_id, state1, state2, weight1, weight2) = move[-1]
                #self.vertices[end_id].display_weight(weight1)
            self.forward_stack.appendleft(move)

    # todo delete?
    def reset_search(self):
        self.forward_stack = deque()
        self.back_stack = deque()
        self.predecessors = dict()

    def get_focus(self):
        self.tk.focus_force()

    def quit(self):
        self.isPlaying = False

    # convert RGB tuple to corresponding hex string
    @staticmethod
    def hex_from_rgb(rgb_tuple):
        return "#{:02x}{:02x}{:02x}".format(*rgb_tuple)

    # convert hex string to corresponding RGB tuple
    @staticmethod
    def rgb_from_hex(hex_string):
        return tuple(ord(c) for c in hex_string.decode('hex'))


if __name__ == '__main__':
    G = Graphy()
    G.mainloop()

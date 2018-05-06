# Menu Bar, parent = Graphy
from tkinter import Menu, filedialog, messagebox
from GraphyRunSearchDialog import GraphyRunSearchDialog
from GraphyWeightDialog import GraphyWeightDialog
from collections import deque


class GraphyMenuBar:

    def __init__(self, parent):

        # hierarchy
        self.parent = parent
        self.tk = parent.tk
        self.mode = self.parent.mode

        # windows
        self.search_window = None
        self.weight_window = None

        # edge weights / euclidean distance
        self.weight_scale = 1

        # path of saved active file
        self.active_file = None

        # Bar
        self.menubar = Menu(self.tk)
        self.tk.config(menu=self.menubar)

        # File Menu
        self.filemenu = Menu(self.menubar)
        self.new_menu = Menu(self.menubar, tearoff=0)
        self.new_menu.add_command(label="Graph", command=self.start_new_graph)
        self.new_menu.add_command(label="Neural Net", command=self.start_new_net)
        self.filemenu.add_cascade(label="New", menu=self.new_menu)
        self.filemenu.add_command(label="Run Search", command=self.start_search)
        self.filemenu.add_command(label="Set Weights", command=self.set_weights)
        self.filemenu.add_command(label="Save As...", command=self.save_as)
        self.filemenu.add_command(label="Save", command=self.save)
        self.filemenu.add_command(label="Open", command=self.open)
        self.filemenu.add_command(label="Quit", command=self.tk.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Edit Menu
        self.editmenu = Menu(self.menubar)
        self.editmenu.add_command(label="Preferences", command=self.do_nothing)  # TODO
        self.editmenu.add_command(label="Controls", command=self.do_nothing)  # TODO
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)  # TODO

        # View Menu
        self.viewmenu = Menu(self.menubar)
        self.viewmenu.add_command(label="Display Preferences", command=self.do_nothing)  # TODO
        self.viewmenu.add_command(label="Zoom In", command=self.zoom_in)
        self.viewmenu.add_command(label="Zoom Out", command=self.zoom_out)
        self.menubar.add_cascade(label="View", menu=self.viewmenu)

    def do_nothing(self):
        return

    # first choose start and end vertices
    def start_search(self):

        if not self.search_window:
            self.search_window = GraphyRunSearchDialog(self)

        self.search_window.get_focus()

    def set_weights(self):

        if not self.weight_window:
            self.weight_window = GraphyWeightDialog(self)

        self.weight_window.get_focus()

    # label ; position ; adjacencies by weight ; adjacencies by label
    # position and adjacencies are both comma separated
    # last line is scale (this is where other forgotten metadata should be added as well)
    def save_as(self):
        if self.mode == "Graph":
            extension = ".graphy"
        elif self.mode == "Net":
            if not (self.parent.input_layer and self.parent.output_layer):
                messagebox.showerror(title="Invalid Input or Output", message="Neural net must have both an input and output layer to be saved.")
                return
            extension = ".netty"
        else:
            messagebox.showerror(title="Invalid Mode", message="Cannot save object of type \"self.mode\"")
            return
        file = filedialog.asksaveasfile(mode='w', defaultextension=extension)
        if file is None:
            return
        self.active_file = file.name
        contents = self.string_contents()
        file.write(contents)
        file.close()

    def save(self):
        if self.active_file:
            file = open(self.active_file, 'w')
            contents = self.string_contents()
            file.write(contents)
            file.close()
        else:
            self.save_as()

    def open(self):
        proceed = True
        if self.parent.vertices:
            proceed = messagebox.askyesno(title="Open File?", message="Any unsaved progress will be lost. Are you sure?")
        if proceed:
            path = filedialog.askopenfilename()
            if path[-7:] == ".graphy":
                self.open_graph(path)
            elif path[-6:] == ".netty":
                self.open_net(path)
            else:
                messagebox.showerror(title="Invalid File", message="Cannot open file \"" + path + "\"")

    def zoom_in(self):
        self.parent.can.scale("all", self.parent.can.winfo_width()/2, self.parent.can.winfo_height()/2-100, 1.2, 1.2)
        self.parent.vertex_spawn.resize()

    def zoom_out(self):
        self.parent.can.scale("all", self.parent.can.winfo_width()/2, self.parent.can.winfo_height()/2-100, 0.8, 0.8)

    def open_graph(self, path):
        file = open(path, 'r')
        if file is None:
            return
        self.set_mode("Graph")
        self.active_file = file.name
        self.reset_objects()
        self.parent.reset_canvas()
        lines = file.readlines()
        file.close()
        self.weight_scale = float(lines[-1])
        lines = lines[:-1]
        vertex_ids = []
        adjacencies = []
        adjacency_labels = []
        for line in lines:
            line = line.replace('\n', '')
            label, position, adjacency, adj_labels = line.split(';')
            x, y = position.split(',')
            vertex_id = self.parent.open_graph_create_vertex(int(x), int(y), label)
            vertex_ids.append(vertex_id)
            adjacency = [self.float_or_none(weight) for weight in adjacency.split(',') if weight]
            adjacencies.append(adjacency)
            adj_labels = [self.label_or_none(a) for a in adj_labels.split(',') if a]
            adjacency_labels.append(adj_labels)
        i = 0
        while i < len(vertex_ids):
            vertex_id = vertex_ids[i]
            j = 0
            while j < len(adjacencies[i]):
                if adjacencies[i][j]:
                    other_vertex_id = vertex_ids[i + j + 1]
                    weight = adjacencies[i][j]
                    edge_label = adjacency_labels[i][j]
                    edge = self.parent.open_graph_create_edge(vertex_id, other_vertex_id, edge_label, weight)
                    self.parent.vertices[vertex_id].add_neighbor(other_vertex_id, edge)
                    self.parent.vertices[other_vertex_id].add_neighbor(vertex_id, edge)
                    edge.update_endpoint_at_id(vertex_id)
                    edge.update_endpoint_at_id(other_vertex_id)
                j += 1
            i += 1

    def open_net(self, path):
        file = open(path, 'r')
        if file is None:
            return
        self.set_mode("Net")
        self.active_file = file.name
        self.reset_objects()
        self.parent.reset_canvas()
        lines = file.readlines()
        file.close()
        vertex_ids = []
        adjacencies = []
        for line in lines:
            line = line.replace('\n', '')
            label, activation, position, node_count, bias, leakiness, bound, outgoing = line.split(';')
            x, y = position.split(',')
            vertex_id = self.parent.open_net_create_vertex(int(x), int(y), label, activation, int(node_count), float(bias), float(leakiness), float(bound))
            vertex_ids.append(vertex_id)
            adjacency = []
            for triple in outgoing.split(','):
                if triple == "None":
                    adjacency.append(None)
                elif triple:
                    weight, noise, label = triple.split('|')
                    weight = float(weight)
                    noise = float(noise)
                    adjacency.append((weight, noise, label))
            adjacencies.append(adjacency)
        self.parent.vertices[vertex_ids[0]].set_input_layer(True)
        self.parent.vertices[vertex_ids[-1]].set_output_layer(True)
        i = 0
        while i < len(vertex_ids):
            vertex_id = vertex_ids[i]
            j = 0
            while j < len(vertex_ids):
                if adjacencies[i][j]:
                    other_vertex_id = vertex_ids[j]
                    weight, noise, label = adjacencies[i][j]
                    edge = self.parent.open_net_create_edge(vertex_id, other_vertex_id, label, weight, noise)
                    self.parent.vertices[vertex_id].add_neighbor(other_vertex_id, edge)
                    self.parent.vertices[other_vertex_id].add_neighbor(vertex_id, edge)
                    edge.update_endpoint_at_id(vertex_id)
                    edge.update_endpoint_at_id(other_vertex_id)
                j += 1
            i += 1

    def reset_objects(self):
        vertices = list(self.parent.vertices.values())
        for vertex in vertices:
            vertex.delete()

    def delete_search_window(self):
        self.search_window = None

    def string_contents(self):
        if self.mode == "Graph":
            return self.graph_string_contents()
        elif self.mode == "Net":
            return self.net_string_contents()

    def graph_string_contents(self):
        vertices = sorted(self.parent.vertices)
        vertex_count = len(vertices)
        lines = []
        i = 0
        while i < vertex_count:
            vertex_id = vertices[i]
            vertex = self.parent.vertices[vertex_id]
            line = vertex.label + ';'
            line += str(vertex.pos_x) + ',' + str(vertex.pos_y) + ';'
            j = i + 1
            adj_labels = ''
            while j < vertex_count:
                other_vertex_id = vertices[j]
                if other_vertex_id in vertex.neighbors:
                    edge = vertex.neighbors[other_vertex_id]
                    line += str(edge.weight) + ','
                    adj_labels += edge.label + ','
                else:
                    line += 'None,'
                    adj_labels += '__None__,'
                j += 1
            if line:
                if line[-1] == ',':
                    line = line[:-1]
            if adj_labels:
                if adj_labels[-1] == ',':
                    adj_labels = adj_labels[:-1]
            line = line + ';' + adj_labels
            lines.append(line)
            i += 1
        lines.append(str(self.weight_scale))
        contents = '\n'.join(lines)
        return contents

    # line 1 is input layer
    # last line is output layer
    # should drop any layers which aren't reachable from start
    # label ; activation ; position ; node count ; bias ; leakiness ; bound ; outgoing connections (weight|noise|label,)
    def net_string_contents(self):
        vertices = []
        completed_edges = set()
        end_id = self.parent.output_layer.id
        queue = deque()
        queue.append(self.parent.input_layer.id)
        while queue:
            id = queue.pop()
            if id != end_id:
                vertices.append(id)
            for neighbor_id in self.parent.vertices[id].neighbors:
                if neighbor_id not in vertices and neighbor_id != end_id:
                    queue.append(neighbor_id)
        vertices.append(end_id)

        lines = []
        i = 0
        while i < len(vertices):
            id = vertices[i]
            vertex = self.parent.vertices[id]
            line = vertex.label + ';'
            line += vertex.status + ';'
            line += str(vertex.pos_x) + ',' + str(vertex.pos_y) + ';'
            line += str(vertex.node_count) + ';'
            line += str(vertex.bias) + ';'
            line += str(vertex.leakiness) + ';'
            line += str(vertex.bound) + ';'
            j = 0
            while j < len(vertices):
                other_id = vertices[j]
                if other_id in vertex.neighbors:
                    edge = vertex.neighbors[other_id]
                    if edge.id_is_start_vertex(id):
                        line += str(edge.weight) + '|' + str(edge.noise) + '|' + edge.label + ','
                    else:
                        line += 'None,'
                else:
                    line += 'None,'
                j += 1
            if line:
                if line[-1] == ',':
                    line = line[:-1]
            lines.append(line)
            i += 1
        contents = '\n'.join(lines)
        return contents

    def start_new_graph(self):
        if messagebox.askyesno(title="Open File?", message="Any unsaved progress will be lost. Are you sure?"):
            self.active_file = None
            self.reset_objects()
            self.set_mode("Graph")

    def start_new_net(self):
        if messagebox.askyesno(title="Open File?", message="Any unsaved progress will be lost. Are you sure?"):
            self.active_file = None
            self.reset_objects()
            self.set_mode("Net")

    def set_mode(self, mode):
        if mode == "Graph":
            self.mode = mode
            self.parent.directed = False
            self.parent.set_mode(mode)
        elif mode == "Net":
            self.mode = mode
            self.parent.directed = True
            self.parent.set_mode(mode)
        else:
            print("Invalid mode for graphy.")

    @staticmethod
    def float_or_none(x):
        if x == 'None':
            return None
        else:
            return float(x)

    @staticmethod
    def label_or_none(x):
        if x == '__None__':
            return None
        else:
            return x

# Menu Bar, parent = Graphy
from tkinter import Menu, filedialog, messagebox
from GraphyRunSearchDialog import GraphyRunSearchDialog
from GraphyWeightDialog import GraphyWeightDialog


class GraphyMenuBar:

    def __init__(self, parent):

        self.parent = parent
        self.tk = parent.tk

        self.search_window = None
        self.weight_window = None
        self.weight_scale = 1

        # Bar
        self.menubar = Menu(self.tk)
        self.tk.config(menu=self.menubar)

        # File Menu
        self.filemenu = Menu(self.menubar)
        self.filemenu.add_command(label="Run Search", command=self.start_search)
        self.filemenu.add_command(label="Set Weights", command=self.set_weights)
        self.filemenu.add_command(label="Save As...", command=self.save_as)  # TODO
        self.filemenu.add_command(label="Save", command=self.do_nothing)  # TODO
        self.filemenu.add_command(label="Open", command=self.open)  # TODO
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
        self.viewmenu.add_command(label="Zoom In", command=self.do_nothing)  # TODO
        self.viewmenu.add_command(label="Zoom Out", command=self.do_nothing)  # TODO
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
        file = filedialog.asksaveasfile(mode='w', defaultextension=".graphy")
        if file is None:
            return
        vertices = sorted(self.parent.vertices)
        vertex_count = len(vertices)
        lines = []
        i = 0
        while i < vertex_count:
            vertex_id = vertices[i]
            vertex = self.parent.vertices[vertex_id]
            line = vertex.label + ';'
            line += str(vertex.pos_x) + ',' + str(vertex.pos_y) + ';'
            j = i+1
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
            print(str(i)+':  ' + line + ';' + adj_labels)
            line = line + ';' + adj_labels
            lines.append(line)
            i += 1
        lines.append(str(self.weight_scale))
        contents = '\n'.join(lines)
        file.write(contents)
        file.close()

    def open(self):
        proceed = True
        if self.parent.vertices:
            proceed = messagebox.askyesno(title="Open File?", message="Any unsaved progress will be lost. Are you sure?")
        if proceed:
            file = open(filedialog.askopenfilename(), 'r')
            if file is None:
                return
            vertices = list(self.parent.vertices.values())
            for vertex in vertices:
                vertex.delete()
            self.parent.reset_canvas()
            lines = file.readlines()
            file.close()
            self.weight_scale = float(lines[-1])
            lines = lines[:-1]
            vertex_ids = []
            adjacencies = []
            adjacency_labels = []
            for line in lines:
                line = line.replace('\n','')
                label, position, adjacency, adj_labels = line.split(';')
                x, y = position.split(',')
                vertex_id = self.parent.open_file_create_vertex(int(x), int(y), label)
                vertex_ids.append(vertex_id)
                adjacency = [self.float_or_none(weight) for weight in adjacency.split(',') if weight]
                adjacencies.append(adjacency)
                adj_labels = [self.label_or_none(x) for x in adj_labels.split(',') if x]
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
                        edge = self.parent.open_file_create_edge(vertex_id, other_vertex_id, edge_label, weight)
                        self.parent.vertices[vertex_id].add_neighbor(other_vertex_id, edge)
                        self.parent.vertices[other_vertex_id].add_neighbor(vertex_id, edge)
                        edge.update_endpoint_at_id(vertex_id)
                        edge.update_endpoint_at_id(other_vertex_id)
                    j += 1
                i += 1

    def delete_search_window(self):
        self.search_window = None

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

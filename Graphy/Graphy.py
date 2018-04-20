# master class

from tkinter import *
from PIL import Image, ImageTk
from math import sqrt
from GraphyMenuBar import GraphyMenuBar
from GraphyVertexSpawnButton import GraphyVertexSpawnButton
from GraphyVertex import GraphyVertex
from GraphyEdge import GraphyEdge
from GraphyInspector import GraphyInspector
from GraphyLegend import GraphyLegend


class Graphy:

    def __init__(self):

        # window
        self.tk = Tk()
        self.tk.title("Graphy")

        # graph / net mode
        self.mode = "Graph"

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

        # canvas setup
        self.canvas_width = 1000
        self.canvas_height = 500
        self.can.config(width=self.canvas_width,
                        height=self.canvas_height,
                        background='white',
                        highlightthickness=0)
        self.can.grid(column=0, row=0, sticky=(N, W, E, S))

        # offset trackers for canvas movement
        self.offset_x = 0
        self.offset_y = 0

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

        # GraphySearch
        self.search = None

        # selection and movement tracking
        self.held_vertex = None
        self.held_edge = None
        self.dragged_edge = None
        self.dragged_edge_offsets = None
        self.selected = None
        self.selected_icon_id = None
        self.is_setting_search_vertex = False
        self.is_setting_scale_edge = False
        self.scale_edge = None
        self.is_moving_canvas = False
        self.max_vertex_pickup_distance = 20
        self.max_edge_pickup_distance = 5

        # vertex images
        self.vertex_size = 20

        # start vertex / identity layer
        start_vertex_image = Image.open("images/StartVertex.png")
        start_vertex_image = start_vertex_image.resize((self.vertex_size, self.vertex_size), Image.ANTIALIAS)
        self.start_vertex_image = ImageTk.PhotoImage(start_vertex_image)
        self.identity_layer_image = self.start_vertex_image

        # unexplored vertex / sigmoid layer
        unexplored_vertex_image = Image.open("images/UnexploredVertex.png")
        unexplored_vertex_image = unexplored_vertex_image.resize((self.vertex_size, self.vertex_size), Image.ANTIALIAS)
        self.unexplored_vertex_image = ImageTk.PhotoImage(unexplored_vertex_image)
        self.sigmoid_layer_image = self.unexplored_vertex_image

        # frontier vertex / logarithmic layer
        frontier_vertex_image = Image.open("images/FrontierVertex.png")
        frontier_vertex_image = frontier_vertex_image.resize((self.vertex_size, self.vertex_size), Image.ANTIALIAS)
        self.frontier_vertex_image = ImageTk.PhotoImage(frontier_vertex_image)
        self.logarithmic_layer_image = self.frontier_vertex_image

        # explored vertex / relu layer
        explored_vertex_image = Image.open("images/ExploredVertex.png")
        explored_vertex_image = explored_vertex_image.resize((self.vertex_size, self.vertex_size), Image.ANTIALIAS)
        self.explored_vertex_image = ImageTk.PhotoImage(explored_vertex_image)
        self.relu_layer_image = self.explored_vertex_image

        # end vertex / exponential layer
        end_vertex_image = Image.open("images/EndVertex.png")
        end_vertex_image = end_vertex_image.resize((self.vertex_size, self.vertex_size), Image.ANTIALIAS)
        self.end_vertex_image = ImageTk.PhotoImage(end_vertex_image)
        self.exponential_layer_image = self.end_vertex_image

        # selected vertex image (red outline)
        self.selected_icon_size = int(1.25 * self.vertex_size)
        selected_vertex_image = Image.open("images/SelectedVertexIcon.png")
        selected_vertex_image = selected_vertex_image.resize((self.selected_icon_size, self.selected_icon_size), Image.ANTIALIAS)
        self.selected_vertex_image = ImageTk.PhotoImage(selected_vertex_image)

        # search playback control images
        self.search_image_width = 60
        self.search_image_height = 20

        # search step forward image
        step_forward_image = Image.open("images/StepForwardButton.png")
        step_forward_image = step_forward_image.resize((self.search_image_width, self.search_image_height), Image.ANTIALIAS)
        self.step_forward_image = ImageTk.PhotoImage(step_forward_image)

        # search step back image
        step_back_image = Image.open("images/StepBackButton.png")
        step_back_image = step_back_image.resize((self.search_image_width, self.search_image_height), Image.ANTIALIAS)
        self.step_back_image = ImageTk.PhotoImage(step_back_image)

        # search to end image
        search_to_end_image = Image.open("images/SearchToEndButton.png")
        search_to_end_image = search_to_end_image.resize((self.search_image_width, self.search_image_height), Image.ANTIALIAS)
        self.search_to_end_image = ImageTk.PhotoImage(search_to_end_image)

        # search to start image
        search_to_start_image = Image.open("images/SearchToStartButton.png")
        search_to_start_image = search_to_start_image.resize((self.search_image_width, self.search_image_height), Image.ANTIALIAS)
        self.search_to_start_image = ImageTk.PhotoImage(search_to_start_image)

        # legend
        self.legend = GraphyLegend(self)

        # controls
        self.tk.bind("<Configure>", self.resize)  # on resize
        self.can.bind("<Motion>", self.motion)  # on mouse movement over canvas
        self.can.bind("<Button-1>", self.click)  # left click to create
        self.can.bind("<Button-2>", self.mclick)  # middle click to select
        self.can.bind("<Button-3>", self.rclick)  # right click to move
        self.can.bind("<ButtonRelease-3>", self.rclick_release)  # let go of right click
        self.tk.bind("<Delete>", self.delete_selected)
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
        elif self.is_moving_canvas:
            self.move_canvas(event.x-self.mousex, event.y-self.mousey)
        self.mousex = event.x
        self.mousey = event.y

    def move_canvas(self, deltax, deltay):
        self.offset_x += deltax
        self.offset_y += deltay
        for vertex in self.vertices.values():
            vertex.translate(deltax, deltay)

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
                x, y = self.can.coords(item)
                distance = self.euclidean_distance(x, y, event.x, event.y)
                if distance <= self.vertex_size:
                    self.held_edge.attach_second_vertex(self.vertices[item])
                else:
                    self.held_edge.die()
            else:
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
                x, y = self.can.coords(item)
                distance = self.euclidean_distance(x, y, event.x, event.y)
                if distance <= self.vertex_size:
                    self.create_edge(self.vertices[item], event)

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
                x, y = self.can.coords(item)
                distance = self.euclidean_distance(x, y, event.x, event.y)
                if distance > self.max_vertex_pickup_distance:
                    self.is_moving_canvas = True
                else:
                    self.held_vertex = self.vertices[item]
            elif item in self.edges:
                ax, ay, bx, by = self.can.coords(item)
                distance = self.distance_to_line(ax, ay, bx, by, event.x, event.y)
                if distance > self.max_edge_pickup_distance:
                    self.is_moving_canvas = True
                else:
                    self.dragged_edge = self.edges[item]
                    self.dragged_edge_offsets = self.can.coords(item)
                    self.dragged_edge_offsets[0] -= event.x
                    self.dragged_edge_offsets[2] -= event.x
                    self.dragged_edge_offsets[1] -= event.y
                    self.dragged_edge_offsets[3] -= event.y
            else:
                self.is_moving_canvas = True

    def rclick_release(self, event):
        self.is_moving_canvas = False

    def create_unexplored_vertex(self, event):
        if not self.held_vertex:
            self.held_vertex = GraphyVertex(self,
                                            self.unexplored_vertex_image,
                                            "Unexplored",
                                            self.mousex,
                                            self.mousey)
            self.vertices[self.held_vertex.id] = self.held_vertex
            self.vertex_count += 1
            self.held_vertex.set_label(self.vertex_count)

    def open_file_create_vertex(self, x, y, label):
        new_vertex = GraphyVertex(self, self.unexplored_vertex_image, "Unexplored", x, y)
        self.vertices[new_vertex.id] = new_vertex
        new_vertex.set_label(label)
        self.vertex_count += 1
        return new_vertex.id

    def open_file_create_edge(self, vertex_id_1, vertex_id_2, label, weight):
        new_edge = GraphyEdge(self, None, None, start_vertex_id=vertex_id_1, end_vertex_id=vertex_id_2, label=label, weight=weight)
        return new_edge

    def set_search_vertex(self, vertex):
        if self.is_setting_search_vertex == "Start":
            if self.search.start_vertex:
                self.search.start_vertex.set_default()
            if vertex.status == "End":
                self.search.end_vertex = None
            vertex.set_status("Start")
            self.search.start_vertex = vertex
        elif self.is_setting_search_vertex == "End":
            if self.search.end_vertex:
                self.search.end_vertex.set_default()
            if vertex.status == "Start":
                self.search.start_vertex = None
            vertex.set_status("End")
            self.search.end_vertex = vertex
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

    def delete_selected(self, event):
        if self.selected:
            self.selected.delete()

    def get_focus(self):
        self.tk.focus_force()

    def reset_canvas(self):
        self.offset_x = 0
        self.offset_y = 0
        self.vertex_count = 0

    def delete_search(self):
        if self.search:
            self.search = None

    def set_mode(self, mode):
        self.mode = mode
        self.legend.set_mode(mode)
        self.inspector.set_mode(mode)

    def quit(self):
        self.isPlaying = False

    # take endpoints of line segment (ax, ay) and (bx, by) and distance from mousex, mousey to the segment
    def distance_to_line(self, ax, ay, bx, by, mousex, mousey):
        if self.dot(bx-ax, by-ay, mousex-bx, mousey-by) >= 0:
            return self.euclidean_distance(bx, by, mousex, mousey)
        elif self.dot(ax-bx, ay-by, mousex-ax, mousey-ay) >= 0:
            return self.euclidean_distance(ax, ay, mousex, mousey)
        else:
            return abs((ay-by)*mousex - (ax-bx)*mousey + ax*by - ay*bx) / self.euclidean_distance(ax, ay, bx, by)

    @staticmethod
    def euclidean_distance(x1, y1, x2, y2):
        return sqrt((x1-x2)**2 + (y1-y2)**2)

    @staticmethod
    def dot(x1, y1, x2, y2):
        return x1*x2 + y1*y2

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

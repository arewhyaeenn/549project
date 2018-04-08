# master class

from tkinter import *
from PIL import Image, ImageTk
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
        self.vertices = dict()
        self.edges = dict()
        self.vertex_spawn = GraphyVertexSpawnButton(self)

        # selection and movement tracking
        self.held_vertex = None
        self.held_edge = None
        self.dragged_edge = None
        self.dragged_edge_offsets = None
        self.selected = None
        self.selected_icon_id = None

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

        else:

            # drop the vertex being dragged
            if self.held_vertex:
                self.held_vertex = None

            # attempt to attach half-created edge to second endpoint
            elif self.held_edge:
                item = self.can.find_closest(event.x, event.y)[0]
                if item in self.vertices:
                    self.held_edge.attach_second_vertex(self.vertices[item])
                else:
                    print('unfinished edge deleted')
                    self.held_edge.die()
                self.held_edge = None
            else:
                item = self.can.find_closest(event.x, event.y)[0]
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

    def create_start_vertex(self, event):
        if not self.held_vertex:
            self.held_vertex = GraphyVertex(self,
                                            self.start_vertex_image,
                                            'Start',
                                            self.mousex,
                                            self.mousey)
            self.vertices[self.held_vertex.id] = self.held_vertex

    def create_end_vertex(self, event):
        if not self.held_vertex:
            self.held_vertex = GraphyVertex(self,
                                            self.end_vertex_image,
                                            'Destination',
                                            self.mousex,
                                            self.mousey)
            self.vertices[self.held_vertex.id] = self.held_vertex

    def create_edge(self, vertex, event):
        self.held_edge = GraphyEdge(self, vertex, event)

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

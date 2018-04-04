# master class

from tkinter import *
from PIL import Image, ImageTk
from GraphyMenuBar import GraphyMenuBar
from GraphyVertexSpawnButton import GraphyVertexSpawnButton
from GraphyVertex import GraphyVertex
from GraphyEdge import GraphyEdge


class Graphy:

    def __init__(self):

        self.tk = Tk()
        self.can = Canvas(self.tk)
        # self.frame = Frame(self.tk)
        self.can.pack()

        self.width = 1000
        self.height = 500
        self.can.config(width=self.width,
                        height=self.height,
                        background='white',
                        highlightthickness=0)

        self.menubar = GraphyMenuBar(self)

        self.vertices = dict()
        self.edges = dict()
        self.vertex_spawn = GraphyVertexSpawnButton(self)
        self.held_vertex = None
        self.held_edge = None
        self.dragged_edge = None
        self.dragged_edge_offsets = None
        self.selected = None
        self.selected_icon_id = None

        self.vertex_size = 20
        unexplored_vertex_image = Image.open("images/UnexploredVertex.png")
        unexplored_vertex_image = unexplored_vertex_image.resize((self.vertex_size,
                                                                  self.vertex_size),
                                                                 Image.ANTIALIAS)
        self.unexplored_vertex_image = ImageTk.PhotoImage(unexplored_vertex_image)

        self.selected_icon_size = 25
        selected_vertex_icon = Image.open("images/SelectedVertexIcon.png")
        selected_vertex_icon = selected_vertex_icon.resize((self.selected_icon_size,
                                                            self.selected_icon_size),
                                                           Image.ANTIALIAS)
        self.selected_vertex_icon = ImageTk.PhotoImage(selected_vertex_icon)

        self.tk.bind("<Configure>", self.resize)  # on resize
        self.can.bind("<Motion>", self.motion)  # on mouse movement over canvas
        self.can.bind("<Button-1>", self.click)  # left click to create
        self.can.bind("<Button-2>", self.mclick)  # middle click to select
        self.can.bind("<Button-3>", self.rclick)  # right click to move
        self.mousex = 0
        self.mousey = 0

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
        new_width = self.tk.winfo_width()
        new_height = self.tk.winfo_height()

        # get scale ratios
        width_scale = float(new_width) / self.width
        height_scale = float(new_height) / self.height

        # set new values
        self.width = new_width
        self.height = new_height

        # adjust canvas dimensions
        self.can.config(width=self.width, height=self.height)

        # scale objects in canvas
        #self.can.scale("all", 0, 0, width_scale, height_scale)

        # instead of scaling all items, only reposition the vertex button
        self.vertex_spawn.resize(self.width,self.height)

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

            # drop the vertex you're dragging
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

    def create_vertex(self, event):
        if not self.held_vertex:
            self.held_vertex = GraphyVertex(self,
                                            self.unexplored_vertex_image,
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

# master class

from tkinter import *
from PIL import Image, ImageTk
from GraphyMenuBar import GraphyMenuBar
from GraphyVertexSpawnButton import GraphyVertexSpawnButton
from GraphyVertex import GraphyVertex


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

        self.vertex_spawn = GraphyVertexSpawnButton(self)
        self.held_vertex = None

        self.vertex_size = 20
        unexplored_vertex_image = Image.open("images/UnexploredVertex.png")
        unexplored_vertex_image = unexplored_vertex_image.resize((self.vertex_size,
                                                                  self.vertex_size),
                                                                 Image.ANTIALIAS)
        self.unexplored_vertex_image = ImageTk.PhotoImage(unexplored_vertex_image)

        self.tk.bind("<Configure>", self.resize)
        self.can.bind("<Motion>", self.motion)
        self.can.bind("<Button-1>", self.click)
        self.mousex = 0
        self.mousey = 0

        self.tk.mainloop()

    def resize(self, event):
        # get scale ratios
        width_scale = float(event.width) / self.width
        height_scale = float(event.height) / self.height

        # set new values
        self.width = event.width
        self.height = event.height

        # adjust canvas dimensions
        self.can.config(width=self.width, height=self.height)

        # scale objects in canvas
        self.can.scale("all", 0, 0, width_scale, height_scale)

    def create_vertex(self, event):
        print('Clicked Vertex Spawn Button')
        if not self.held_vertex:
            self.held_vertex = GraphyVertex(self,
                                            'unexplored',
                                            self.unexplored_vertex_image,
                                            self.mousex,
                                            self.mousey)

    def motion(self, event):
        if self.held_vertex:
            self.can.coords(self.held_vertex.id, event.x, event.y)
        self.mousex = event.x
        self.mousey = event.y

    def click(self, event):
        if self.held_vertex:
            self.held_vertex = None


Graphy()

# Vertex Spawn Button, parent = Graphy
from PIL import ImageTk, Image
from tkinter import SW, Button


class GraphyVertexSpawnButton:

    def __init__(self, parent):

        self.parent = parent
        self.tk = self.parent.tk
        self.can = self.parent.can

        # Place Picture
        self.padding = 10
        self.button_size = 50
        self.button = Button(self.can)
        button_image = Image.open('images/VertexCreationButton.png')

        self.button_image = button_image.resize((self.button_size,
                                                 self.button_size),
                                                Image.ANTIALIAS)

        self.button_image = ImageTk.PhotoImage(image=self.button_image)

        self.button.config(image=self.button_image,
                           width=self.button_size,
                           height=self.button_size)
        self.button_window = self.can.create_window(self.padding,
                                                    parent.height - self.padding,
                                                    anchor=SW,
                                                    window=self.button)
        self.button.bind("<Button-1>", self.parent.create_vertex)

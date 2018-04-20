# Legend, parent = graphy
from tkinter import ttk, Frame, Canvas, Label


class GraphyLegend:

    def __init__(self, parent):

        self.parent = parent

        self.width = self.parent.right_frame_width
        self.padding = self.parent.right_frame_padding

        # frame
        self.frame = Frame(master=self.parent.right_frame, bg='pink')
        self.frame.pack(side='bottom', fill='both')

        # "Legend" title bar
        self.title_frame = ttk.Frame(master=self.frame)
        self.title_frame.pack(side='top')
        self.title_label = Label(master=self.title_frame,
                                 text="Legend",
                                 width=self.width,
                                 bg='lightgray')
        self.title_label.pack()

        # canvas
        self.canvas_width = self.parent.canvas_padding - self.padding
        self.vertex_size = self.parent.vertex_size
        self.canvas_height = 12 * self.vertex_size
        self.can = Canvas(master=self.frame,
                          width=self.canvas_width,
                          height=self.canvas_height,
                          bg='white')
        self.can.pack()

        self.texts = []
        self.images = []
        self.set_mode("Net")

    def set_mode(self, mode):
        if mode == "Graph":
            self.images = [self.parent.start_vertex_image,
                           self.parent.unexplored_vertex_image,
                           self.parent.frontier_vertex_image,
                           self.parent.explored_vertex_image,
                           self.parent.end_vertex_image,
                           self.parent.selected_vertex_image]

            self.texts = ["Start",
                          "Unexplored",
                          "Frontier",
                          "Explored",
                          "End",
                          "Selected"]

        elif mode == "Net":
            self.texts = ["Identity",
                          "Sigmoid",
                          "Logarithmic",
                          "ReLU",
                          "Exponential",
                          "Selected"]

            self.images = [self.parent.identity_layer_image,
                           self.parent.sigmoid_layer_image,
                           self.parent.logarithmic_layer_image,
                           self.parent.relu_layer_image,
                           self.parent.exponential_layer_image,
                           self.parent.selected_vertex_image]
        else:
            print("This will never actually happen.")

        self.update_display()

    def update_display(self):
        print('Canvas mode updated.')
        self.can.delete('all')
        i = 0
        x_image = int(self.canvas_width / 4)
        x_text = self.canvas_width - x_image
        y = self.vertex_size
        while i < len(self.images):
            self.can.create_image(x_image, y, image=self.images[i])
            self.can.create_text(x_text, y, text=self.texts[i])
            y += 2 * self.vertex_size
            i += 1

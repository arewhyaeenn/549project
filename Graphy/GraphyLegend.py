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

        # images
        '''self.start_vertex_id = None
        self.unexplored_vertex_id = None
        self.frontier_vertex_id = None
        self.explored_vertex_id = None
        self.end_vertex_id = None
        self.selected_vertex_id = None

        image_ids = [self.start_vertex_id,
                     self.unexplored_vertex_id,
                     self.frontier_vertex_id,
                     self.explored_vertex_id,
                     self.end_vertex_id,
                     self.selected_vertex_id]

        self.start_label_id = None
        self.unexplored_label_id = None
        self.frontier_label_id = None
        self.explored_label_id = None
        self.end_label_id = None
        self.selected_label_id = None
        
        label_ids = [self.start_label_id,
                     self.unexplored_label_id,
                     self.frontier_label_id,
                     self.explored_label_id,
                     self.end_label_id,
                     self.selected_label_id]'''

        images = [self.parent.start_vertex_image,
                  self.parent.unexplored_vertex_image,
                  self.parent.frontier_vertex_image,
                  self.parent.explored_vertex_image,
                  self.parent.end_vertex_image,
                  self.parent.selected_vertex_image]

        texts = ['Start',
                 'Unexplored',
                 'Frontier',
                 'Explored',
                 'End',
                 'Selected']

        i = 0
        x_image = int(self.canvas_width/4)
        x_text = self.canvas_width - x_image
        y = self.vertex_size
        while i < len(images):
            self.can.create_image(x_image, y, image=images[i])
            self.can.create_text(x_text, y, text=texts[i])
            y += 2 * self.vertex_size
            i += 1

        # right frame (for images)

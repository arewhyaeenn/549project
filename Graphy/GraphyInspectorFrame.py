# Inspector Frame, parent = Graphy
from tkinter import ttk, Label, StringVar, DoubleVar


class GraphyInspectorFrame:

    def __init__(self, parent):

        self.parent = parent

        self.width = self.parent.right_frame_width
        self.padding = 4

        self.frame = ttk.Frame(master=self.parent.right_frame)
        self.frame.pack(side='top', fill='y')

        # "Inspector" bar
        self.title_frame = ttk.Frame(master=self.frame)
        self.title_frame.pack(side='top')
        self.title_label = Label(master=self.title_frame,
                                 text="Inspector",
                                 width=self.width,
                                 bg='gray')
        self.title_label.pack()

        # identifier for type of object selected
        self.type_frame = ttk.Frame(master=self.frame, relief='sunken')
        self.type_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
        self.type_label1 = Label(master=self.type_frame,
                                 width=int(self.width/2)-self.padding,
                                 text='Type:')
        self.type_label1.pack(side='left', padx=self.padding, pady=self.padding)
        self.type_label2 = Label(master=self.type_frame,
                                 width=int(self.width / 2) - self.padding,
                                 text='',
                                 bg='white')
        self.type_label2.pack(side='right', padx=self.padding, pady=self.padding)

        # label of selected object (i.e. name user gives them, no canvas IDs here)
        self.label_frame = ttk.Frame(master=self.frame, relief='sunken')
        self.label_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
        self.label_label = Label(master=self.label_frame,
                                 width=int(self.width/2)-self.padding,
                                 text="Label:")
        self.label_label.pack(side='left', padx=self.padding, pady=self.padding)
        self.label_var = StringVar()
        self.label_var.set('')
        self.label_entry = ttk.Entry(self.label_frame,
                                     width=int(self.width/2)-self.padding,
                                     textvariable=self.label_var)
        self.label_entry.pack(side='right', padx=self.padding, pady=self.padding)

        # weight identifier (for edges only)
        self.weight_frame = ttk.Frame(master=self.frame, relief='sunken')
        self.weight_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
        self.weight_label = Label(master=self.weight_frame,
                                  width=int(self.width/2)-self.padding,
                                  text="Weight:")
        self.weight_label.pack(side='left', padx=self.padding, pady=self.padding)
        self.weight_var = DoubleVar()
        self.weight_entry = ttk.Entry(self.weight_frame,
                                      width=int(self.width / 2) - self.padding,
                                      textvariable=self.weight_var)
        self.weight_entry.pack(side='right', padx=self.padding, pady=self.padding)

        self.selected = None
        self.set_unselected()

        self.label_var.trace('w', lambda *args: self.set_selected_label())
        self.weight_var.trace('w', self.set_selected_weight)

    # object is a vertex or edge, type is 'vertex' or 'edge'...
    def set_selected(self, selected_object, selected_object_type):

        self.selected = selected_object

        if selected_object_type == 'vertex':

            self.type_label2.config(text='Vertex')
            self.type_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
            self.label_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)

            self.label_var.set(selected_object.label)

        elif selected_object_type == 'edge':

            self.type_label2.config(text='Edge')
            self.type_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
            self.label_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
            self.weight_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)

            self.label_var.set(selected_object.label)
            self.weight_var.set(selected_object.weight)

        else:
            print('dafuq is going on')

    # nothing is selected
    def set_unselected(self):
        self.type_frame.pack_forget()
        self.label_frame.pack_forget()
        self.weight_frame.pack_forget()
        self.selected = None

    # set label of selected object
    def set_selected_label(self, *args):
        self.selected.set_label(self.label_var.get())

    # set weight of selected object
    def set_selected_weight(self, *args):
        self.selected.set_weight(self.weight_var.get())

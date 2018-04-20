# Inspector Frame, parent = Graphy (master = Graphy.right_frame)
from tkinter import Label, StringVar, DoubleVar, IntVar, Entry, Frame, OptionMenu


class GraphyInspector:

    def __init__(self, parent):

        self.parent = parent

        self.width = self.parent.right_frame_width
        self.padding = self.parent.right_frame_padding

        self.frame = Frame(master=self.parent.right_frame)
        self.frame.pack(side='top', fill='y', )

        # "Inspector" title bar
        self.title_frame = Frame(master=self.frame)
        self.title_frame.pack(side='top')
        self.title_label = Label(master=self.title_frame, text="Inspector", width=self.width, bg='lightgray')
        self.title_label.pack()

        # identifier for type of object selected
        self.type_frame = Frame(master=self.frame, relief='sunken')
        self.type_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
        self.type_label1 = Label(master=self.type_frame, width=int(self.width/2)-self.padding, text='Object:')
        self.type_label1.pack(side='left', padx=self.padding, pady=self.padding)
        self.type_label2 = Label(master=self.type_frame, width=int(self.width / 2) - self.padding, text='', bg='white')
        self.type_label2.pack(side='right', padx=self.padding, pady=self.padding)

        # label of selected object (i.e. name user gives them, no canvas IDs here)
        self.label_frame = Frame(master=self.frame, relief='sunken')
        self.label_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
        self.label_label = Label(master=self.label_frame, width=int(self.width/2)-self.padding, text="Label:")
        self.label_label.pack(side='left', padx=self.padding, pady=self.padding)
        self.label_var = StringVar()
        self.label_var.set('')
        self.label_entry = Entry(self.label_frame, width=int(self.width/2)-self.padding, textvariable=self.label_var)
        self.label_entry.pack(side='right', padx=self.padding, pady=self.padding)
        self.label_entry.bind('<Button-1>', self.select_label_text)
        self.label_entry.bind('<Return>', self.drop_widget_focus)

        # status identifier (for vertices and layers)
        self.status_frame = Frame(master=self.frame, relief='sunken')
        self.status_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
        self.status_label1 = Label(master=self.status_frame, width=int(self.width/2)-self.padding, text='Status:')
        self.status_label1.pack(side='left', padx=self.padding, pady=self.padding)
        self.status_label2 = Label(master=self.status_frame, width=int(self.width/2)-self.padding, text='', bg='white')
        self.status_label2.pack(side='right', padx=self.padding, pady=self.padding)
        self.activation_var = StringVar()
        self.activation_menu = OptionMenu(self.status_frame, self.activation_var, "Identity", "Sigmoid", "ReLU", "Logarithmic", "Exponential")

        # weight identifier (for edges only)
        self.weight_frame = Frame(master=self.frame, relief='sunken')
        self.weight_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
        self.weight_label = Label(master=self.weight_frame, width=int(self.width/2)-self.padding, text="Weight:")
        self.weight_label.pack(side='left', padx=self.padding, pady=self.padding)
        self.weight_var = DoubleVar()
        self.weight_entry = Entry(self.weight_frame, width=int(self.width / 2) - self.padding, textvariable=self.weight_var)
        self.weight_entry.pack(side='right', padx=self.padding, pady=self.padding)
        self.weight_entry.bind('<Button-1>', self.select_weight_text)
        self.weight_entry.bind('<Return>', self.drop_widget_focus)

        # node count identifier (for layers only)
        self.node_frame = Frame(master=self.frame, relief='sunken')
        self.node_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
        self.node_label = Label(master = self.node_frame, width=int(self.width/2)-self.padding, text="Node Count:")
        self.node_label.pack(side='left', padx=self.padding, pady=self.padding)
        self.node_var = IntVar()
        self.node_entry = Entry(self.node_frame, width=int(self.width / 2) - self.padding, textvariable=self.node_var)
        self.node_entry.pack(side='right', padx=self.padding, pady=self.padding)
        self.node_entry.bind('<Button-1>', self.select_node_text)
        self.node_entry.bind('<Return>', self.drop_widget_focus)

        self.selected = None
        self.selected_type = None
        self.set_unselected()

        self.label_var.trace('w', self.set_selected_label)
        self.weight_var.trace('w', self.set_selected_weight)
        self.activation_var.trace('w', self.set_selected_activation)
        self.node_var.trace('w', self.set_selected_node_count)

        # mode
        self.mode = parent.mode
        self.set_mode(parent.mode)

    # object is a vertex or edge, type is 'vertex' or 'edge'...
    def set_selected(self, selected_object, selected_object_type):

        self.selected = selected_object
        self.selected_type = selected_object_type

        if self.mode == "Graph":
            if selected_object_type == 'vertex':

                self.type_label2.config(text="Vertex")
                self.status_label2.config(text=selected_object.status)

                self.type_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
                self.label_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
                self.status_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)

                self.label_var.set(selected_object.label)

            elif selected_object_type == 'edge':

                self.type_label2.config(text="Edge")

                self.type_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
                self.label_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
                self.weight_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)

                self.label_var.set(selected_object.label)
                self.weight_var.set(selected_object.weight)

            else:
                print('dafuq is going on')

        elif self.mode == "Net":
            if selected_object_type == 'vertex':
                self.type_label2.config(text="Layer")
                self.status_label2.config(text=selected_object.status)

                self.type_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
                self.label_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
                self.status_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)
                self.node_frame.pack(side='top', fill='x', pady=self.padding, padx=self.padding)

                self.label_var.set(selected_object.label)
                self.status_var.set(selected_object.status)
                self.node_var.set(selected_object.node_count)

        else:
            print('This will never happen.')

    # nothing is selected
    def set_unselected(self):
        self.type_frame.pack_forget()
        self.label_frame.pack_forget()
        self.status_frame.pack_forget()
        self.weight_frame.pack_forget()
        self.node_frame.pack_forget()
        self.selected = None
        self.selected_type = None

    # set label of selected object
    def set_selected_label(self, *args):
        self.selected.set_label(self.label_var.get())

    # set weight of selected object
    def set_selected_weight(self, *args):
        self.selected.set_weight(self.weight_var.get())

    def set_selected_activation(self, *args):
        self.selected.set_status(self.activation_var.get())

    def set_selected_node_count(self, *args):
        self.selected.set_node_count(self.node_var.get())

    def update(self):
        if self.selected:
            selected = self.selected
            type = self.selected_type
            self.set_unselected()
            self.set_selected(selected, type)

    def select_label_text(self, event):
        if event:
            # delay so the default click doesn't undo selection, then recall and fall through to "else"
            self.parent.tk.after(50, self.select_label_text, False)
        else:
            self.label_entry.select_range(0, 'end')
            self.label_entry.icursor(0)

    def select_weight_text(self, event):
        if event:
            # delay so the default click doesn't undo selection, then recall and fall through to "else"
            self.parent.tk.after(50, self.select_weight_text, False)
        else:
            self.weight_entry.select_range(0, 'end')
            self.weight_entry.icursor(0)

    def select_node_text(self, event):
        if event:
            self.parent.tk.after(50, self.select_node_text, False)
        else:
            self.node_entry.select_range(0, 'end')
            self.node_entry.icursor(0)

    def drop_widget_focus(self, event):
        self.frame.focus()

    def set_mode(self, mode):
        if mode == "Graph":
            self.mode = mode
            self.weight_label.config(text="Weight:")
            self.status_label1.config(text="Status:")
        elif mode == "Net":
            self.mode = mode
            self.weight_label.config(text="Initial Weight:")
            self.status_label_1.config(text="Activation:")
        else:
            print("This will never happen.")
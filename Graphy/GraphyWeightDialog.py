# Set weights, parent = GraphyMenuBar
from tkinter import *
from tkinter import ttk


class GraphyWeightDialog:

    def __init__(self, parent):

        # hierarchy references
        self.parent = parent
        self.graphy = parent.parent

        # window
        self.tk = Toplevel()
        self.tk.title("Weights")

        # main frame
        self.x_padding = 20
        self.button_padding = 2
        self.frame = Frame(self.tk)
        self.frame.pack(side='top', padx=self.x_padding, pady=self.button_padding)

        # auto-set weights based on canvas distance
        self.auto_button = Button(master=self.frame, text="Set Euclidean Weights", bg='lightblue', activebackground='lightskyblue')
        self.auto_button.grid(row=0, column=0, columnspan=2, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
        self.auto_button.bind('<Button-1>', self.auto_set)

        # manually set scale
        self.scale_label = Label(master=self.frame, text="Scale:")
        self.scale_label.grid(row=1, column=0, sticky=NSEW)
        self.scale_var = DoubleVar()
        self.scale_var.set(parent.weight_scale)
        self.scale_entry = Entry(self.frame, textvariable=self.scale_var)
        self.scale_entry.grid(row=1, column=1, sticky=NSEW)
        self.scale_entry.bind('<Button-1>', self.select_scale_text)
        self.scale_entry.bind('<Return>', self.drop_widget_focus)

        # get scale from existing edge
        self.scale_from_edge_button = Button(master=self.frame, text="Get Scale From Edge", bg='pink', activebackground='lightpink')
        self.scale_from_edge_button.grid(row=2, column=0, columnspan=2, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
        self.scale_from_edge_button.bind('<Button-1>', self.select_edge_for_scale)

        # set column widths equal
        self.frame.columnconfigure(0, weight=1, uniform='u')
        self.frame.columnconfigure(1, weight=1, uniform='u')

        # rebind exit button
        self.tk.protocol('WM_DELETE_WINDOW', self.quit)

        # bind scale variable
        self.scale_var.trace('w', self.set_parent_scale)

    def auto_set(self, event):
        self.graphy.set_edge_weights(self.scale_var.get())

    def select_scale_text(self, event):
        if event:
            # delay so the default click doesn't undo selection, then recall and fall through to "else"
            self.tk.after(50, self.select_scale_text, False)
        else:
            self.scale_entry.select_range(0, 'end')
            self.scale_entry.icursor(0)

    def set_scale(self, scale):
        self.scale_var.set(scale)

    def set_parent_scale(self, *args):
        print("setting parent scale")
        self.parent.weight_scale = self.scale_var.get()

    def select_edge_for_scale(self, event):
        print("selecting scale edge")
        self.graphy.is_setting_scale_edge = True
        self.graphy.get_focus()

    def get_focus(self):
        self.tk.focus_force()

    def drop_widget_focus(self, event):
        self.tk.focus()

    def quit(self):
        self.parent.weight_window = None
        self.tk.destroy()
        del self

# Search, parent = GraphyMenuBar

from tkinter import *


# todo this doesn't do much yet, just a window pops up
class GraphyRunSearchDialog:

    def __init__(self, parent):

        # hierarchy references
        self.parent = parent
        self.graphy = parent.parent

        # window
        self.tk = Toplevel()
        self.tk.title("Search")

        runSearchOption = Menu(self.tk, tearoff=0)
        runSearchOption.add_command(label="Undo", command=self.edit_options)

        # main frame
        self.x_padding = 20
        self.button_padding = 2
        self.frame = Frame(self.tk)
        self.frame.pack(side='top', padx=self.x_padding, pady=self.button_padding)

        # dummy for choosing start / end; states = None, 'Start', 'End'
        self.choosing = None

        # set up start vertex selection
        self.set_start_vertex_button = Button(self.frame, text='Set Start Vertex', bg='lightgreen', activebackground='palegreen')
        self.set_start_vertex_button.grid(row=0, column=0, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
        self.set_start_vertex_button.bind('<Button-1>', self.select_start_vertex)

        # set up end vertex selection
        self.set_end_vertex_button = Button(self.frame, text='Set End Vertex', bg='pink', activebackground='lightpink')
        self.set_end_vertex_button.grid(row=0, column=1, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
        self.set_end_vertex_button.bind('<Button-1>', self.select_end_vertex)

        # set up search type selection
        self.search_type_var = StringVar(self.frame)
        self.search_type_var.set('BFS')
        self.search_type_menu = OptionMenu(self.frame, self.search_type_var, 'Breadth-First','Depth-First','A*')
        self.search_type_menu.config(bg='wheat', activebackground='burlywood')
        self.search_type_menu['menu'].config(bg='wheat')
        self.search_type_menu.grid(row=1, column=0, columnspan=2, sticky=NSEW)

        # set up search start button
        self.start_search_button = Button(self.frame, text='Start Search', bg='lightblue', activebackground='lightskyblue')
        self.start_search_button.grid(row=2, column=0, columnspan=2, sticky=NSEW)
        self.start_search_button.bind('<Button-1>', self.start_search)

        # rebind exit button
        self.tk.protocol('WM_DELETE_WINDOW', self.quit)

        #
        self.tk.update()
        self.tk.minsize(self.tk.winfo_width(), self.tk.winfo_height())
        self.tk.maxsize(self.tk.winfo_width(), self.tk.winfo_height())

    def edit_options(self):
        print("hello")

    def get_focus(self):
        self.tk.focus_force()

    def select_start_vertex(self, event):
        print('selecting start vertex')
        self.graphy.is_setting_search_vertex = 'Start'
        self.graphy.get_focus()

    def select_end_vertex(self, event):
        self.graphy.is_setting_search_vertex = 'End'
        self.graphy.get_focus()

    def start_search(self, event):
        print('"Start Search" button pressed')

    def quit(self):
        self.parent.search_window = None
        self.tk.destroy()
        del self

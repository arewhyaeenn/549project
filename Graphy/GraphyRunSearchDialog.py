# Search, parent = GraphyMenuBar

from tkinter import *
from tkinter import messagebox
from GraphySearch import GraphySearch


class GraphyRunSearchDialog:

    def __init__(self, parent):

        # hierarchy references
        self.parent = parent
        self.graphy = parent.parent

        # window
        self.tk = Toplevel()
        self.tk.title("Search")

        # main frame
        self.x_padding = 20
        self.button_padding = 2
        self.frame = Frame(self.tk)
        self.frame.pack(side='top', padx=self.x_padding, pady=self.button_padding)

        # start GraphySearch
        self.search = GraphySearch(self)

        # dummy for choosing start / end; states = None, 'Start', 'End'
        self.choosing = None

        # set up start vertex selection
        self.set_start_vertex_button = Button(self.frame, text='Set Start Vertex', bg='lightgreen', activebackground='palegreen')
        self.set_start_vertex_button.grid(row=0, column=0, columnspan=2, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
        self.set_start_vertex_button.bind('<Button-1>', self.select_start_vertex)

        # set up end vertex selection
        self.set_end_vertex_button = Button(self.frame, text='Set End Vertex', bg='pink', activebackground='lightpink')
        self.set_end_vertex_button.grid(row=0, column=2, columnspan=2, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
        self.set_end_vertex_button.bind('<Button-1>', self.select_end_vertex)

        # set up search type selection
        self.search_type_var = StringVar(self.frame)
        self.search_type_menu = OptionMenu(self.frame, self.search_type_var,
                                           "Simple Breadth-First",
                                           "Simple Depth-First",
                                           "Weighted Breadth-First",
                                           "Weighted Depth-First",
                                           "A*")
        self.search_type_menu.config(bg='wheat', activebackground='burlywood')
        self.search_type_menu['menu'].config(bg='wheat')
        self.search_type_menu.grid(row=1, column=0, columnspan=4, sticky=NSEW)
        self.search_type_var.trace('w', self.set_search_type)
        self.search_type_var.set('Simple Breadth-First')

        # set up search start button
        self.start_search_button = Button(self.frame, text='Start Search', bg='lightblue', activebackground='lightskyblue')
        self.start_search_button.grid(row=2, column=0, columnspan=4, sticky=NSEW)
        self.start_search_button.bind('<Button-1>', self.start_search)

        # set up end search button
        self.end_search_button = Button(self.frame, text="End Search", bg='pink', activebackground='lightpink')
        self.end_search_button.bind('<Button-1>', self.end_search)

        # step forward button setup
        self.forward_button = Button(self.frame, image=self.graphy.step_forward_image)
        self.forward_button.bind('<Button-1>', self.search_step_forward)

        # step back button setup
        self.back_button = Button(self.frame, image=self.graphy.step_back_image)
        self.back_button.bind('<Button-1>', self.search_step_back)

        # search to end button setup
        self.search_to_end_button = Button(self.frame, image=self.graphy.search_to_end_image)
        self.search_to_end_button.bind('<Button-1>', self.set_search_to_end)

        # search to start button
        self.search_to_start_button = Button(self.frame, image=self.graphy.search_to_start_image)
        self.search_to_start_button.bind('<Button-1>', self.set_search_to_start)

        # slider setup
        self.number_of_steps = 0
        self.slider = Scale(self.frame, from_=0, to=5, tickinterval=1, orient=HORIZONTAL, command=self.update_search)
        self.current_step = 0

        # rebind exit button
        self.tk.protocol('WM_DELETE_WINDOW', self.quit)

        # lock window size
        self.tk.update()
        self.tk.resizable(width=False, height=False)

    def get_focus(self):
        self.tk.focus_force()

    def select_start_vertex(self, event):
        self.graphy.is_setting_search_vertex = 'Start'
        self.graphy.get_focus()

    def select_end_vertex(self, event):
        self.graphy.is_setting_search_vertex = 'End'
        self.graphy.get_focus()

    def set_search_type(self, *args):
        self.search.set_search_type(self.search_type_var.get())

    def start_search(self, event):
        if self.search.start_vertex and self.search.end_vertex:

            # allow resizing
            self.tk.resizable(width=True, height=True)

            # forget setup buttons
            self.set_end_vertex_button.grid_forget()
            self.set_start_vertex_button.grid_forget()
            self.search_type_menu.grid_forget()
            self.start_search_button.grid_forget()

            # setup search
            self.search.set_search_to_start()
            self.search.search_setup()

            # configure slider
            self.number_of_steps = len(self.search.forward_stack)
            self.slider.config(from_=0, to=self.number_of_steps, tickinterval=self.number_of_steps)
            self.slider.set(0)

            # place playback controls
            self.search_to_start_button.grid(row=0, column=0, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
            self.back_button.grid(row=0, column=1, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
            self.forward_button.grid(row=0, column=2, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
            self.search_to_end_button.grid(row=0, column=3, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
            self.slider.grid(row=2, column=0, columnspan=4, pady=self.button_padding, sticky=EW)
            self.end_search_button.grid(row=3, column=0, columnspan=4, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)

            # lock size
            self.tk.resizable(width=False, height=False)

        else:
            messagebox.showerror(parent=self.tk, title="Error", message="Searching requires a start vertex and an end vertex!")
            self.tk.after(50, self.raise_search_button)

    def end_search(self, event):

        # allow resizing
        self.tk.resizable(width=True, height=True)

        # reset search object
        self.search.end_search()

        # forget playback controls
        self.search_to_start_button.grid_forget()
        self.back_button.grid_forget()
        self.forward_button.grid_forget()
        self.search_to_end_button.grid_forget()
        self.slider.grid_forget()
        self.end_search_button.grid_forget()

        # place setup controls
        self.set_start_vertex_button.grid(row=0, column=0, columnspan=2, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
        self.set_end_vertex_button.grid(row=0, column=2, columnspan=2, padx=self.button_padding, pady=self.button_padding, sticky=NSEW)
        self.search_type_menu.grid(row=1, column=0, columnspan=4, sticky=NSEW)
        self.start_search_button.grid(row=2, column=0, columnspan=4, sticky=NSEW)

        # lock size
        self.tk.resizable(width=False, height=False)

    def search_step_forward(self, event=None):
        if self.search.forward_stack:
            self.increment_slider()
        self.search.search_step_forward()

    def increment_slider(self):
        self.current_step = self.slider.get()+1
        self.slider.set(self.current_step)

    def search_step_back(self, event=None):
        if self.search.back_stack:
            self.decrement_slider()
        self.search.search_step_back()

    def decrement_slider(self):
        self.current_step = self.slider.get()-1
        self.slider.set(self.current_step)

    def set_search_to_end(self, event):
        self.slider.set(self.number_of_steps)
        self.update_search()

    def set_search_to_start(self, event):
        self.slider.set(0)
        self.update_search()

    def update_search(self, event=None):
        new_step = self.slider.get()
        while new_step < self.current_step:
                self.search.search_step_back()
                self.current_step -= 1
        while new_step > self.current_step:
                self.search.search_step_forward()
                self.current_step += 1

    def raise_search_button(self):
        self.start_search_button.config(relief=RAISED)

    def quit(self):
        self.parent.search_window = None
        self.graphy.search = None
        self.search.set_search_to_start()
        if self.search.start_vertex:
            self.search.start_vertex.set_status("Unexplored")
            self.search.start_vertex = None
        if self.search.end_vertex:
            self.search.end_vertex.set_status("Unexplored")
            self.search.end_vertex = None
        self.tk.destroy()
        del self.search
        self.graphy.delete_search()
        self.parent.delete_search_window()
        del self

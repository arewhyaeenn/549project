# Menu Bar, parent = Graphy
from tkinter import Menu
from GraphyRunSearchDialog import GraphyRunSearchDialog


class GraphyMenuBar:

    def __init__(self, parent):

        self.parent = parent
        self.tk = parent.tk

        # Bar
        self.menubar = Menu(self.tk)
        self.tk.config(menu=self.menubar)

        # File Menu
        self.filemenu = Menu(self.menubar)
        self.filemenu.add_command(label="Run Search", command=self.start_search)  # TODO
        self.filemenu.add_command(label="Save As...", command=self.do_nothing)  # TODO
        self.filemenu.add_command(label="Save", command=self.do_nothing)  # TODO
        self.filemenu.add_command(label="Open", command=self.do_nothing)  # TODO
        self.filemenu.add_command(label="Quit", command=self.tk.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Edit Menu
        self.editmenu = Menu(self.menubar)
        self.editmenu.add_command(label="Preferences", command=self.do_nothing)  # TODO
        self.editmenu.add_command(label="Controls", command=self.do_nothing)  # TODO
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)  # TODO

        # View Menu
        self.viewmenu = Menu(self.menubar)
        self.viewmenu.add_command(label="Display Preferences", command=self.do_nothing)  # TODO
        self.viewmenu.add_command(label="Zoom In", command=self.do_nothing)  # TODO
        self.viewmenu.add_command(label="Zoom Out", command=self.do_nothing)  # TODO
        self.menubar.add_cascade(label="View", menu=self.viewmenu)

    def do_nothing(self):
        return

    # first choose start and end vertices
    def start_search(self):
        GraphyRunSearchDialog(self)
        print("running search")
        # top = self.top = Toplevel(parent)
        #
        # Label(top, text="Value").pack()
        #
        # self.e = Entry(top)
        # self.e.pack(padx=5)
        #
        # b = Button(top, text="OK", command=self.ok)
        # b.pack(pady=5)

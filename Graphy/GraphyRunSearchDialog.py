from tkinter import *


# todo this doesn't do much yet, just a window pops up
class GraphyRunSearchDialog:

    def __init__(self, parent):
        root = Tk()
        runSearchOption = Menu(root, tearoff=0)

        runSearchOption.add_command(label="Undo", command=self.edit_options)

    def edit_options(self):
        print("hello")


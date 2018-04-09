# Vertex, parent = Graphy (master = Graphy.can)


class GraphyVertex:

    def __init__(self, parent, image, status, mousex, mousey):

        self.parent = parent
        self.can = self.parent.can
        self.image = image
        self.id = self.can.create_image(mousex, mousey, image=self.image)
        self.edges = set()
        self.neighbors = set()
        self.selected = False
        self.label = ''
        self.status = status

    def update_position(self, x, y):
        self.can.coords(self.id, x, y)
        if self.selected:
            self.can.coords(self.parent.selected_icon_id, x, y)
        for edge in self.edges:
            edge.update_endpoint_at_id(self.id, x, y)

    def add_edge(self, edge, vertex_id):
        if vertex_id:
            if vertex_id in self.neighbors:
                edge.die()
                print('multi-edge deleted')
            else:
                self.add_neighbor(vertex_id)
                self.edges.add(edge)
                self.parent.vertices[vertex_id].add_neighbor(self.id)
                edge.update_trailing_end(*self.can.coords(self.id))
                print('edge completed')
        else:
            self.edges.add(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def add_neighbor(self, vertex_id):
        self.neighbors.add(vertex_id)

    def set_selected(self):
        if self.selected:
            self.set_unselected()
        else:
            print('vertex selected')
            self.selected = True
            self.parent.selected_icon_id = self.can.create_image(*self.can.coords(self.id),
                                                                 image=self.parent.selected_vertex_image)
            self.can.tag_lower(self.parent.selected_icon_id)
            self.parent.inspector.set_selected(self, 'vertex')

    def set_unselected(self):
        print('vertex unselected')
        self.selected = False
        self.can.delete(self.parent.selected_icon_id)
        self.parent.selected_icon_id = None
        self.parent.selected = None
        self.parent.inspector.set_unselected()

    def set_label(self, label):
        self.label = label

    def set_default(self):
        self.set_status('Unexplored')

    def set_status(self, status):
        self.status = status
        if status == 'Unexplored':
            self.can.itemconfig(self.id, image=self.parent.unexplored_vertex_image)
        elif status == 'Start':
            self.can.itemconfig(self.id, image=self.parent.start_vertex_image)
        elif status == 'Frontier':
            self.can.itemconfig(self.id, image=self.parent.frontier_vertex_image)
        elif status == 'Explored':
            self.can.itemconfig(self.id, image=self.parent.explored_vertex_image)
        elif status == 'End':
            self.can.itemconfig(self.id, image=self.parent.end_vertex_image)
        else:
            print('Vertex set to unsupported status.')

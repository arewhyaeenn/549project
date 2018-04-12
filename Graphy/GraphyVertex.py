# Vertex, parent = Graphy (master = Graphy.can)


class GraphyVertex:

    def __init__(self, parent, image, status, mousex, mousey):

        # hierarchy
        self.parent = parent
        self.can = self.parent.can

        # canvas setup
        self.image = image
        self.id = self.can.create_image(mousex, mousey, image=self.image)
        self.set_status(status)

        # graph utilities
        self.edges = set()
        self.neighbors = dict() #  neighbor id --> corresponding edge
        self.selected = False
        self.label = ''

        # global position without canvas offset
        self.pos_x = mousex - self.parent.offset_x
        self.pos_y = mousey - self.parent.offset_y

        self.display_text_id = None

    def update_position(self, x, y):
        self.can.coords(self.id, x, y)
        self.pos_x = x - self.parent.offset_x
        self.pos_y = y - self.parent.offset_y
        if self.selected:
            self.can.coords(self.parent.selected_icon_id, x, y)
        self.update_edge_positions(x, y)

    def translate(self, deltax, deltay):
        self.can.move(self.id, deltax, deltay)
        x, y = self.can.coords(self.id)
        self.update_edge_positions(x, y)

    def update_edge_positions(self, x, y):
        for edge in self.edges:
            edge.update_endpoint_at_id(self.id, x, y)

    def add_edge(self, edge, vertex_id):
        if vertex_id:
            if vertex_id in self.neighbors:
                edge.die()
            else:
                self.add_neighbor(vertex_id, edge)
                self.edges.add(edge)
                self.parent.vertices[vertex_id].add_neighbor(self.id, edge)
                edge.update_trailing_end(*self.can.coords(self.id))
        else:
            self.edges.add(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def add_neighbor(self, vertex_id, edge):
        self.neighbors[vertex_id] = edge

    def set_selected(self):
        if self.selected:
            self.set_unselected()
        else:
            self.selected = True
            self.parent.selected_icon_id = self.can.create_image(*self.can.coords(self.id),
                                                                 image=self.parent.selected_vertex_image)
            self.can.tag_lower(self.parent.selected_icon_id)
            self.parent.inspector.set_selected(self, 'vertex')

    def set_unselected(self):
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

    def display_weight(self, weight):
        if self.display_text_id:
            self.can.delete(self.display_text_id)
            self.display_text_id = None
        if weight:
            x, y = self.can.coords(self.id)
            x += self.parent.vertex_size // 2
            y += self.parent.vertex_size // 2
            self.display_text_id = self.can.create_text(x, y, text=round(weight,2))

    def delete(self):
        self.set_unselected()
        neighborhood = list(self.neighbors)
        i = 0
        while i < len(neighborhood):
            neighbor_id = neighborhood[i]
            self.neighbors[neighbor_id].delete()
            i += 1
        self.can.delete(self.id)
        self.display_weight(None)
        del self.parent.vertices[self.id]
        del self

    def remove_neighbor(self, neighbor_id):
        edge = self.neighbors[neighbor_id]
        del self.neighbors[neighbor_id]
        self.edges.remove(edge)

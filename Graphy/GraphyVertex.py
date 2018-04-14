# Vertex, parent = Graphy


class GraphyVertex:

    def __init__(self, parent, image, status, mousex, mousey):

        # hierarchy
        self.parent = parent
        self.can = self.parent.can

        # canvas setup
        self.image = image
        self.id = self.can.create_image(mousex, mousey, image=self.image)
        self.status = status

        # graph utilities
        self.edges = set()
        self.neighbors = dict()  # neighboring vertex id --> corresponding edge
        self.selected = False
        self.label = ''

        # global position without canvas offset
        self.pos_x = mousex - self.parent.offset_x
        self.pos_y = mousey - self.parent.offset_y

        self.display_text_id = []

    def update_position(self, x, y):
        self.can.coords(self.id, x, y)
        self.pos_x = x - self.parent.offset_x
        self.pos_y = y - self.parent.offset_y
        if self.selected:
            self.can.coords(self.parent.selected_icon_id, x, y)
        if len(self.display_text_id) == 1:
            self.can.coords(self.display_text_id[0], *self.get_display_coords(1))
        elif len(self.display_text_id) == 2:
            x1, y1, x2, y2 = self.get_display_coords(2)
            self.can.coords(self.display_text_id[0], x1, y1)
            self.can.coords(self.display_text_id[1], x2, y2)
        self.update_edge_positions(x, y)

    def translate(self, deltax, deltay):
        self.can.move(self.id, deltax, deltay)
        for id in self.display_text_id:
            self.can.move(id, deltax, deltay)
        if self.selected:
            self.can.move(self.parent.selected_icon_id, deltax, deltay)
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
                self.parent.vertices[vertex_id].add_neighbor(self.id, edge)
                edge.update_trailing_end(*self.can.coords(self.id))
        else:
            self.edges.add(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def add_neighbor(self, vertex_id, edge):
        self.neighbors[vertex_id] = edge
        self.edges.add(edge)

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
        self.label = str(label).replace(';', '').replace(',', '').replace('\n', '')

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

    def display_weight(self, weights):
        if self.display_text_id:
            for id in self.display_text_id:
                self.can.delete(id)
            self.display_text_id = []
        if len(weights) == 1:
            x, y = self.get_display_coords(1)
            self.display_text_id.append(self.can.create_text(x, y, text=round(weights[0], 2)))
        elif len(weights) == 2:
            x1, y1, x2, y2 = self.get_display_coords(2)
            self.display_text_id.append(self.can.create_text(x1, y1, text=round(weights[0], 2)))
            self.display_text_id.append(self.can.create_text(x2, y2, text=round(weights[1], 2)))
        elif len(weights) > 2:
            print('Unsupported number of display weights')

    def get_display_coords(self, number_of_pairs):
        x, y = self.can.coords(self.id)
        if number_of_pairs == 1:
            x += self.parent.vertex_size // 1.5
            y += self.parent.vertex_size // 1.5
            return x, y
        elif number_of_pairs == 2:
            x1 = x - self.parent.vertex_size // 1.5
            y1 = y - self.parent.vertex_size // 1.5
            x2 = x + self.parent.vertex_size // 1.5
            y2 = y + self.parent.vertex_size // 1.5
            return x1, y1, x2, y2
        else:
            print('Unsupported number of coordinates requested.')

    def delete(self):
        self.set_unselected()
        neighborhood = list(self.neighbors)
        i = 0
        while i < len(neighborhood):
            neighbor_id = neighborhood[i]
            self.neighbors[neighbor_id].delete()
            i += 1
        self.can.delete(self.id)
        self.display_weight([])
        del self.parent.vertices[self.id]
        del self

    def remove_neighbor(self, neighbor_id):
        edge = self.neighbors[neighbor_id]
        del self.neighbors[neighbor_id]
        self.edges.remove(edge)

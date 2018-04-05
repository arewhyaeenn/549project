# Edge, parent = Graphy (master = Graphy.can)


class GraphyEdge:

    def __init__(self, parent, vertex, event):

        self.width = 1
        self.selected_width = 3
        vertex_id = vertex.id
        self.parent = parent
        self.can = self.parent.can
        self.coords = [*self.can.coords(vertex_id), event.x, event.y]
        self.id = self.can.create_line(*self.coords)
        self.drop()

        self.vertices = {vertex_id: 0}  # vertex id to 0,2 for offsetting coordinate indices
        vertex.add_edge(self, None)
        self.parent.edges[self.id] = self

        self.selected = False
        self.label = ''
        self.weight = 0

    def update_endpoint_at_id(self, vertex_id, x, y):

        # indexing offset
        delta = self.vertices[vertex_id]

        # update coordinates
        self.coords[0+delta] = x
        self.coords[1+delta] = y

        # apply update to canvas
        self.can.coords(self.id, *self.coords)
        if self.selected:
            self.can.coords(self.parent.selected_icon_id, *self.coords)

    # for use when 1 end is connected to the mouse
    def update_trailing_end(self, x, y):
        self.coords[2] = x
        self.coords[3] = y
        self.can.coords(self.id, *self.coords)

    def attach_second_vertex(self, vertex):
        if vertex.id in self.vertices:
            print('loop deleted')
            self.die()
        else:
            vertex.add_edge(self, next(iter(self.vertices)))
            self.vertices[vertex.id] = 2

    # to background
    def drop(self):
        self.can.tag_lower(self.id)

    def update_position(self, x1, y1, x2, y2):
        for vertex_id in self.vertices:
            if self.vertices[vertex_id] > 0:
                self.parent.vertices[vertex_id].update_position(x2, y2)
            else:
                self.parent.vertices[vertex_id].update_position(x1, y1)
        if self.selected:
            self.can.coords(self.parent.selected_icon_id, x1, y1, x2, y2)

    def die(self):
        for vertex_id in self.vertices:
            self.parent.vertices[vertex_id].remove_edge(self)
        self.can.delete(self.id)
        del self.parent.edges[self.id]
        del self

    def set_selected(self):
        if self.selected:
            self.set_unselected()
        else:
            print('edge selected')
            self.selected = True
            self.parent.selected_icon_id = self.can.create_line(*self.coords,
                                                                width=self.selected_width,
                                                                fill=self.parent.hex_from_rgb((255, 50, 50)))
            self.can.tag_lower(self.parent.selected_icon_id)
            self.parent.inspector.set_selected(self, 'edge')

    def set_unselected(self):
        print('edge unselected')
        self.selected = False
        self.can.delete(self.parent.selected_icon_id)
        self.parent.selected_icon_id = None
        self.parent.selected = None
        self.parent.inspector.set_unselected()

    def set_label(self, label):
        self.label = label

    def set_weight(self, weight):
        self.weight = weight

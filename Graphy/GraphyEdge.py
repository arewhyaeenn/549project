# Edge, parent = Graphy (master = Graphy.can)
from math import sqrt


class GraphyEdge:

    def __init__(self, parent, vertex, event, start_vertex_id=None, end_vertex_id=None, label='', weight=1):

        self.width = 1
        self.selected_width = 3
        self.parent = parent
        self.can = self.parent.can
        if event:
            vertex_id = vertex.id
            self.coords = [*self.can.coords(vertex_id), event.x, event.y]
            self.vertices = {vertex_id: 0}
            vertex.add_edge(self, None)
        else:
            self.vertices = {start_vertex_id: 0, end_vertex_id: 2}
            self.coords = [*self.can.coords(start_vertex_id), *self.can.coords(end_vertex_id)]
        self.id = self.can.create_line(*self.coords)
        self.drop()
        self.parent.edges[self.id] = self

        self.selected = False
        self.label = ''
        self.set_label(label)
        self.weight = weight

    def update_endpoint_at_id(self, vertex_id, x=None, y=None):

        # indexing offset
        delta = self.vertices[vertex_id]

        # get coords if not given
        if not x:
            x, y = self.can.coords(vertex_id)

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

    def delete(self):
        self.set_unselected()
        vertex_1_id, vertex_2_id = tuple(self.vertices)
        self.parent.vertices[vertex_1_id].remove_neighbor(vertex_2_id)
        self.parent.vertices[vertex_2_id].remove_neighbor(vertex_1_id)
        self.can.delete(self.id)
        del self.parent.edges[self.id]
        del self

    def set_selected(self):
        if self.selected:
            self.set_unselected()
        else:
            self.selected = True
            self.parent.selected_icon_id = self.can.create_line(*self.coords, width=self.selected_width, fill=self.parent.hex_from_rgb((255, 50, 50)))
            self.can.tag_lower(self.parent.selected_icon_id)
            self.parent.inspector.set_selected(self, 'edge')

    def set_unselected(self):
        self.selected = False
        self.can.delete(self.parent.selected_icon_id)
        self.parent.selected_icon_id = None
        self.parent.selected = None
        self.parent.inspector.set_unselected()

    def set_label(self, label):
        self.label = str(label).replace(';', '').replace(',', '').replace('\n', '')

    def set_weight(self, weight):
        self.weight = weight
        if self.selected:
            self.parent.inspector.update()

    def set_status(self, state):
        if state == "Default":
            self.can.itemconfig(self.id, fill='black', width=1)
        elif state == "Highlighted":
            self.can.itemconfig(self.id, fill='green', width=6)
        else:
            print('edge set to invalid state')

    def get_weight_scale(self):
        distance = self.get_euclidean_distance()
        return self.weight / distance

    def set_weight_from_scale(self, scale):
        self.set_weight(self.get_euclidean_distance() * scale)

    def get_euclidean_distance(self):
        return self.euclidean_distance(*self.coords)

    @staticmethod
    def euclidean_distance(x1, y1, x2, y2):
        return sqrt((x1-x2)**2 + (y1-y2)**2)

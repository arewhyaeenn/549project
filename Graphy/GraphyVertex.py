# Vertex, parent = Graphy


class GraphyVertex:

    def __init__(self, parent, vertex_type, image, mousex, mousey):

        self.parent = parent
        self.can = self.parent.can
        self.type = vertex_type
        self.image = image

        self.id = self.can.create_image(mousex, mousey, image=self.image)

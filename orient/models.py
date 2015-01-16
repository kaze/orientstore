from schematics.models import Model


class OrientModel(Model):

    _parentclass = 'V'

    pass


class VertexModel(OrientModel):

    _parentclass = 'V'

    pass


class EdgeModel(OrientModel):

    _parentclass = 'E'

    pass

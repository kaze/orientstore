import re

from pyorient.types import OrientRecordLink
from schematics.exceptions import ValidationError
from schematics.types import StringType
from schematics.types.compound import ListType, ModelType


class RIDType(StringType):

    def validate_rid(self, value):

        rid_re = re.compile('^#\d+:\d+$')

        if not rid_re.match(value).group(0) == value:
            raise ValidationError('Invalid RID value')


class LinkType(RIDType):
    pass


class LinkSetType(ListType):
    pass


class EmbeddedType(ModelType):
    pass

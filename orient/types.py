import re

from pyorient.types import OrientRecordLink
from schematics.exceptions import ValidationError
from schematics.types import (StringType, URLType, DateTimeType, DecimalType,
                              LongType, IntType, EmailType, UUIDType, IPv4Type,
                              BooleanType)
from schematics.types.compound import ListType, ModelType
from schematics.types.temporal import TimeStampType


class RIDType(StringType):

    def validate_rid(self, value):

        rid_re = re.compile('^#\d+:\d+$')

        if not rid_re.match(value).group(0) == value:
            raise ValidationError('Invalid RID value')


class EmbeddedType(ModelType):
    pass


class EmbeddedListType(ModelType):
    pass


class EmbeddedSetType(ModelType):
    pass


class EmbeddedMapType(ModelType):
    pass


class LinkType(RIDType):
    pass


class LinkListType(ListType):
    pass


class LinkSetType(ListType):
    pass


class LinkMapType(ListType):
    pass

import re

from pyorient.types import OrientRecordLink
from schematics.exceptions import ValidationError
from schematics.types import (StringType, URLType, DateTimeType, DecimalType,
                              LongType, IntType, EmailType, UUIDType, IPv4Type,
                              BooleanType)
from schematics.types.compound import ListType, ModelType
from schematics.types.temporal import TimeStampType

# schematics.types.base module
# BaseType(TypeMeta('BaseTypeBase', (object, ), {}))
# UUIDType(BaseType), IPv4Type(BaseType), StringType(BaseType), NumberType(BaseType),
# DecimalType(BaseType), HashType(BaseType), BooleanType(BaseType), DateType(BaseType)
# DateTimeType(BaseType), GeoPointType(BaseType), MultilingualStringType(BaseType)
# URLType(StringType), EmailType(StringType)
# IntType(NumberType), FloatType(NumberType)
# MD5Type(HashType), SHA1Type(HashType)
#
# schematics.types.temporal module
# TimeStampType(DateTimeType)
#
# schematics.types.compound module
# MultiType(BaseType)
# ModelType(MultiType), ListType(MultiType), DictType(MultiType), PolyModelType(MultiType)

# type options are:
# - boolean
# - integer
# - short
# - long
# - float
# - double
# - date
# - string
# - binary
# - embedded
# - embeddedlist, an ordered collection of items that supports duplicates. Optionally accepts the parameter linked-type or linked-class to specify the collection's content
# - embeddedset, an unordered collection of items that does not support duplicates. Optionally accepts the parameter linked-type or linked-class to specify the collection's content
# - embeddedmap, a map of key/value entries. Optionally accepts the parameter linked-type or linked-class to specify the map's value content
# - link
# - linklist, an ordered collection of items that supports duplicates. Optionally accepts the parameter linked-class to specify the linked record's class
# - linkset, an unordered collection of items that does not support duplicates. Optionally accepts the parameter linked-class to specify the linked record's class
# - linkmap, this is a map of key/value entries. Optionally accepts the parameter linked-class to specify the map's value record class
#   - byte
#   - linked-type, the contained type in EMBEDDEDSET, EMBEDDEDLIST and EMBEDDEDMAP types (see above). See also Types. Valid options are:
#   - boolean
#   - integer
#   - short
#   - long
#   - float
#   - double
#   - date
#   - string
#   - binary
#   - embedded
#   - link
#   - byte
# - linked-class, the contained class


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

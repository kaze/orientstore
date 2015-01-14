import json
import re

from pyorient.types import OrientRecordLink, OrientRecord
from pyorient.exceptions import PyOrientCommandException
from schematics.exceptions import ValidationError, ModelValidationError
import schematics

from .connection import db_client


class OrientStore(object):

    _models = {}

    @classmethod
    def register_model_module(cls, modelmodule):

        new_models = dict([(name, {'class':clsp}) \
            for name, clsp in modelmodule.__dict__.items() \
                if isinstance(clsp, type) \
                    and type(clsp) == schematics.models.ModelMeta
        ])

        cls._collect_fields(new_models)

        cls._models.update(new_models)

    @classmethod
    def _collect_fields(cls, models):

        for model, attrs in models.items():

            fields = []

            for m in attrs['class']._fields.items():
                typestring = m[1].__class__.__name__
                orient_type = typestring.replace('Type','').upper()
                if orient_type == 'URL':
                    orient_type = 'STRING'

                fields.append({'name': m[0],
                               'type': typestring,
                               'orient_type': orient_type})

            attrs['fields'] = fields

    @classmethod
    def unregister_model(cls, model_name):

        del cls.models[model_name]

    @classmethod
    def to_model(cls, model, orient_object):

        model = model()
        model.rid = orient_object.__dict__['_OrientRecord__rid']
        data_dict = orient_object.__dict__['_OrientRecord__o_storage']

        for key, value in data_dict.items():

            if type(value) == OrientRecordLink:

                value = value.get_hash()

            if type(value) == list:

                value = [v.get_hash() if type(v) == OrientRecordLink else value for v in value]

            model.__dict__['_data'][key] = value

        return model

    @classmethod
    def command(cls, expression):

        try:
            return db_client.command(expression)

        except PyOrientCommandException as e:

            return e

    @classmethod
    def query(cls, expression):

        try:
            return db_client.query(expression)

        except PyOrientCommandException as e:

            return e

    # create
    # ----------------------------------------------------------------------- #
    @classmethod
    def create(cls, model, data):

        item = model(**data)

        try:
            item.validate()
            itemjson = json.dumps(item.to_primitive())
            command = 'insert into {} content {}'.format(model.__name__, itemjson)

            return cls.command(command)

        except ModelValidationError as e:

            return e.messages

    # read
    # ----------------------------------------------------------------------- #
    @classmethod
    def get(cls, model, rid):

        orient_object = cls.query('select from {}'.format(rid))[0]

        return cls.to_model(model, orient_object=orient_object) if type(orient_object) == OrientRecord else None

    @classmethod
    def where(cls, model, expression):

        command = "select from {} where {}".format(model.__name__, expression)

        return [cls.to_model(model, orient_object=c) for c in cls.query(command) if type(c) == OrientRecord]

    @classmethod
    def find_by(cls, model, field, value):

        expression = "{} = '{}'".format(field, value)

        return cls.where(model, expression)

    # update
    # ----------------------------------------------------------------------- #
    @classmethod
    def update(cls, model, data): pass

    # delete
    # ----------------------------------------------------------------------- #
    @classmethod
    def delete(cls, model, rid): pass

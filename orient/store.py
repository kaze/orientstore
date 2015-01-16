import json
import re

from pyorient.types import OrientRecordLink, OrientRecord
from pyorient.exceptions import PyOrientCommandException
from schematics.exceptions import ValidationError, ModelValidationError
from schematics.datastructures import OrderedDict
import schematics

from .client import OrientClient


class OrientStore(object):

    def __init__(self, config):

        self.models = {}
        self.db_client = OrientClient(config).connect()

    def init_structure(self):

        for m in self.models:

            model = self.models[m]

            self.create_class_for(model)
            self.create_fields_for(model)

    def create_class_for(self, model):
        try:

            command = 'create class {} extends {}'.format(
                    model['name'],
                    model['parentclass']
                )

            self.command(command)
            print command

        except PyOrientCommandException:

            print e

    def create_fields_for(self, model):

        for field in model['fields']:

            try:

                command = 'create property {}.{} {}'.format(
                    model['name'],
                    field['name'],
                    field['orient_type']
                )

                linked = field.get('linked', None)

                if linked:

                    command = '{} {}'.format(command, linked)

                self.command(command)

            except PyOrientCommandException:

                print e

    def create_index_for(self, model):
        # CREATE INDEX <name> [ON <class-name> (prop-names)] <type> [<key-type>]
        #   METADATA [{<json-metadata>}]
        pass

    def register_model_module(self, modelmodule):

        newmodels = dict([(name, {'class':selfp,
                                   'name': name,
                                   'parentclass':selfp._parentclass}) \
            for name, selfp in modelmodule.__dict__.items() \
                if isinstance(selfp, type) \
                    and type(selfp) == schematics.models.ModelMeta
        ])

        self._collect_fields(newmodels)
        self.models.update(newmodels)

    def _collect_fields(self, models):

        for model, attrs in models.items():

            fields = []

            for m in attrs['class']._fields.items():
                orient_type = m[1].__class__.__name__.replace('Type','').upper()

                if orient_type in ['URL', 'UUID', 'IPV4']:

                    orient_type = 'STRING'

                fields.append({'name': m[0],
                               'type': m[1].__class__,
                               'orient_type': orient_type})

            attrs['fields'] = fields

    def unregister_model(self, model_name):

        del self.models[model_name]

    def model_class_for(self, model_name):

        return self.models[model_name]['class']

    def to_model(self, model, orient_object):

        model = self.model_class_for(model)()
        model.rid = orient_object.__dict__['_OrientRecord__rid']
        data_dict = orient_object.__dict__['_OrientRecord__o_storage']

        for key, value in data_dict.items():

            if type(value) == OrientRecordLink:

                value = value.get_hash()

            if type(value) == list:

                value = [v.get_hash() if type(v) == OrientRecordLink else value for v in value]

            model.__dict__['_data'][key] = value

        return model

        # try:
        #     if model.validate():

        #         return model

        # except ModelValidationError as e:

        #     return e.messages

    def command(self, expression):

        try:

            return self.db_client.command(expression)

        except PyOrientCommandException as e:

            return e

    def query(self, expression):

        try:

            return self.db_client.query(expression)

        except PyOrientCommandException as e:

            return e

    # traversal commands
    # ----------------------------------------------------------------------- #
    def traverse(self):
        # TRAVERSE <[class.]field>|*|any()|all()
        #           [FROM <target>]
        #           [LET <Assignment>*]
        #           WHILE <condition>
        #           [LIMIT <max-records>]
        #           [STRATEGY <strategy>]
        pass

    def find_references(self):
        # FIND REFERENCES <rid|(<sub-query>)> [class-list]
        pass

    # create
    # ----------------------------------------------------------------------- #
    def create(self, model, data):
        # INSERT INTO [class:]<class>|cluster:<cluster>|index:<index>
        #   [(<field>[,]*) VALUES (<expression>[,]*)[,]*]|
        #   [SET <field> = <expression>|<sub-command>[,]*]|
        #   [CONTENT {<JSON>}]|
        #   [RETURN <expression>]
        #   [FROM <query>]

        item = self.model_class_for(model)(data)

        try:

            item.validate()
            itemjson = json.dumps(item.to_primitive())
            command = 'insert into {} content {}'.format(model, itemjson)

            return self.command(command)

        except ModelValidationError as e:

            return e.messages

    def create_link(self):
        # CREATE LINK <link-name>
        #   TYPE [<link-type>]
        #   FROM <source-class>.<source-property>
        #   TO <destination-class>.<destination-property>
        #   [INVERSE]
        pass

    # read
    # ----------------------------------------------------------------------- #
    def get(self, model, rid):

        orient_object = self.query('select from {}'.format(rid))[0]

        return self.to_model(model, orient_object=orient_object) if type(orient_object) == OrientRecord else None

    def where(self, model, expression):

        command = "select from {} where {}".format(model, expression)

        return [self.to_model(model, orient_object=c) for c in self.query(command) if type(c) == OrientRecord]

    def find_by(self, model, field, value):

        expression = "{} = '{}'".format(field, value)

        return self.where(model, expression)

    # update
    # ----------------------------------------------------------------------- #
    def update(self, model, data):
        # UPDATE <class>|cluster:<cluster>|<recordID>
        #   [SET|INCREMENT|ADD|REMOVE|PUT <field-name> = <field-value>[,]*]|[CONTENT|MERGE <JSON>]
        #   [UPSERT]
        #   [RETURN <returning> [<returning-expression>]]
        #   [WHERE <conditions>]
        #   [LOCK default|record]
        #   [LIMIT <max-records>] [TIMEOUT <timeout>]
        pass

    # delete
    # ----------------------------------------------------------------------- #
    def delete(self, model, rid): pass

    def delete_vertext(self):
        # DELETE VERTEX <rid>|<class>|FROM (<subquery>)
        #   [WHERE <conditions>]
        #   [LIMIT <MaxRecords>>]
        pass

    def delete_edge(self):
        # DELETE EDGE <rid>|FROM <rid>|TO <rid>|[<class>]
        #   [WHERE <conditions>]>
        #   [LIMIT <MaxRecords>]
        pass


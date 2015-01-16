import json

from pyorient.types import OrientRecordLink, OrientRecord
from pyorient.exceptions import PyOrientCommandException
from schematics.exceptions import ModelValidationError

from .client import OrientClient
from .migrator import OrientMigrator


class OrientStore(object):

    def __init__(self, config):

        self.db_client = OrientClient(config).connect()
        self.migrator = OrientMigrator(store=self)

    def init_database(self, model_module):

        self.migrator.register_model_module(model_module)
        self.migrator.init_structure()

    def to_model(self, model, orient_object):

        model = self.migrator.model_class_for(model)()
        rid = orient_object.rid

        if rid:

            model.rid = rid

        data_dict = orient_object.oRecordData or {}

        for key, value in data_dict.items():

            if type(value) == OrientRecordLink:

                value = value.get_hash()

            if type(value) == list:

                value = [v.get_hash() if type(v) == OrientRecordLink else value for v in value]

            model.__dict__['_data'][key] = value

        return model

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
    def insert(self, model, data):

        # INSERT INTO [class:]<class>|cluster:<cluster>|index:<index>
        #   [(<field>[,]*) VALUES (<expression>[,]*)[,]*]|
        #   [SET <field> = <expression>|<sub-command>[,]*]|
        #   [CONTENT {<JSON>}]|
        #   [RETURN <expression>]
        #   [FROM <query>]

        item = self.migrator.model_class_for(model)(data)

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

    def delete_vertex(self):

        # DELETE VERTEX <rid>|<class>|FROM (<subquery>)
        #   [WHERE <conditions>]
        #   [LIMIT <MaxRecords>>]

        pass

    def delete_edge(self):

        # DELETE EDGE <rid>|FROM <rid>|TO <rid>|[<class>]
        #   [WHERE <conditions>]>
        #   [LIMIT <MaxRecords>]

        pass


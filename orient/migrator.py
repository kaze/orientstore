from pyorient.exceptions import PyOrientCommandException
import schematics


class OrientMigrator(object):

    def __init__(self, store):

        self.models = {}
        self.store = store

    def init_structure(self):

        for m in self.models:

            model = self.models[m]

            self.create_class_for(model)
            self.create_fields_for(model)

    def create_class_for(self, model):

        command = 'create class {} extends {}'.format(
                model['name'],
                model['parentclass']
            )

        self.store.command(command)

    def create_fields_for(self, model):

        for field in model['fields']:

            self.create_property(model_name=model['name'],
                                 field_name=field['name'],
                                 orient_type=field['orient_type'],
                                 linked=field.get('linked', None))

    def create_property(self, model_name, field_name, orient_type=None, linked=None):

        command = 'create property {}.{}'.format(model_name, field_name)

        if orient_type:

            command = '{} {}'.format(command, orient_type)

        if linked:

            command = '{} {}'.format(command, linked)

        self.store.command(command)

    def alter_property(self, model_name, field_name, attribute_name, attribute_value):

        command = 'alter property {}.{} {} {}'.format(model_name,
                                                      field_name,
                                                      attribute_name,
                                                      attribute_value)

        self.store.command(command)

    def create_index_for(self, model):

        # CREATE INDEX <name> [ON <class-name> (prop-names)] <type> [<key-type>]
        #   METADATA [{<json-metadata>}]

        pass

    def register_model_module(self, modelmodule):

        newmodels = dict([(name, {'class':cls,
                                  'name': name,
                                  'parentclass':cls._parentclass}) \
            for name, cls in modelmodule.__dict__.items() \
                if isinstance(cls, type) \
                    and type(cls) == schematics.models.ModelMeta
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

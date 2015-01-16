from pyorient import OrientDB


class OrientClient(object):

    def __init__(self, config):

        self.host = config.get('DB_HOST')
        self.port = int(config.get('DB_PORT'))
        self.user = config.get('DB_USER')
        self.password = config.get('DB_PASS')
        self.db_name = config.get('DB_NAME')
        self.db_type = config.get('DB_TYPE')
        self.db_storage_type = config.get('DB_STORAGE_TYPE')

    def ensure_database(self):

        if not self.db_client.db_exists(self.db_name, self.db_storage_type):

            self.db_client.db_create(self.db_name,
                                     self.db_type,
                                     self.db_storage_type)

    def init_database(self):

        self.db_client = OrientDB(self.host, self.port)
        self.db_client.connect(self.user, self.password)
        self.ensure_database()

    def connect(self):

        self.init_database()
        self.db_client.db_open(self.db_name, self.user, self.password)

        return self.db_client

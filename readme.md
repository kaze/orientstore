I'm just hacking on python and [OrientDB](http://www.orientechnologies.com/) to see, how, and to what, could I use a graph database. The code in this repo is not even alpha, or pre-alpha, only an experiment yet.

## good to know

OrientStore uses the [`schematics`](https://github.com/schematics/schematics) module to describe the models, and [`pyorient`](https://github.com/mogui/pyorient) to communicate with the database over the binary protocol. OrientStore automatically get the model names and their fields from the module which contains them, and, on startup, creates the database, classes, edges, whatever needed:

    config = {
      'DB_HOST': 'localhost',
      'DB_PORT': 2424,
      'DB_USER': 'root',
      'DB_PASS': 'root_password',
      'DB_NAME': 'example',
      'DB_TYPE': 'graph',           # could be 'graph' or 'document'
      'DB_STORAGE_TYPE': 'plocal'   # could be 'plocal' or 'memory'
    }

    db = OrientStore(config)
    db.register_model_module(models)
    db.init_structure()

The code currently only knows how to create and simply get back records, so there is not much to say about functionality. :)

More on the usage/development/test later.

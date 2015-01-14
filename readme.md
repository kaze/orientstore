I'm just hacking on python and orientdb to see, how, and to what, could I use a graph database. The code in this repo is not even alpha, or pre-alpha, only an experiment yet.

## good to know

This code is used with my own [`pyenv`](https://github.com/kaze/pyenv) to set and get variables from the environment. An example .env file is added to the repo

I'm using the clever [`schematics`](https://github.com/schematics/schematics) module to describe my models. OrientStore automatically get the model names and their fields from the module, which contains them:

    OrientStore.register_model_module(module.submodule.models)

To connect with the database, I use [`pyorient`](https://github.com/mogui/pyorient)

The code currently only knows how to create and simply get back records, so there is not much to say about functionality. :)

More on the usage/development/test later.

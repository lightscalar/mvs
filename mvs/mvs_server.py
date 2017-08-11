from mvs.module import *
from pymongo import MongoClient
from master_controller import *
from pyro.basics import *


AVAILABLE_MODULES = [0]
DATABASE_NAME = 'mvs_database'

client = MongoClient()
database = client[DATABASE_NAME]

# Instantiate available models.
modules = {}
for module_id in AVAILABLE_MODULES:
    modules[module_id] = Module(module_id)

# Construct a MasterController for each module.
controllers = {}
for module_id, module in modules.items():
    controllers[module_id] = MasterController(module, database)
    controllers[module_id].start()


# Attach the database.
Pyro.attach_db(database)


class Experiment(Pyro):
    pass


class Command(Pyro):
    pass


class Target(Pyro):
    pass


# Define relationships.
Experiment.has_many(Target)


# Launch the server
app = Application(Pyro)
app.run()


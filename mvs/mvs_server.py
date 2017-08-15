from mvs.module import *
from pymongo import MongoClient
from master_controller import *
from pyro.basics import *


AVAILABLE_MODULES = [('Module-01', 0)]
DATABASE_NAME = 'mvs_database'

client = MongoClient()
database = client[DATABASE_NAME]

# Instantiate available models.
modules = {}
for _, module_id in AVAILABLE_MODULES:
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

class Unit(Pyro):
    pass

class Target(Pyro):
    pass

# Define relationships.
Experiment.has_many(Target)

# Register Modules,
Unit.delete_all()
for name, module_id in AVAILABLE_MODULES:
    unit = {}
    unit['name'] = name
    unit['module_id'] = module_id
    unit['position'] = {'x': 0, 'y': 0,'z': 0}
    unit['camera_status'] = 'active'
    unit['motor_status'] = 'active'
    unit['is_translating'] = False
    unit['last_calibration'] = 0
    unit['image_url'] = 'http://localhost:{}'.format(unit['module_id'] + 1493)
    Unit.create(unit)

# Launch the server.
app = Application(Pyro)
app.run()

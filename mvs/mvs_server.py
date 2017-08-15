from mvs.unit import *
from pymongo import MongoClient
from master_controller import *
from pyro.basics import *


AVAILABLE_UNITS = [('Unit-01', 0)]
DATABASE_NAME = 'mvs_database'

client = MongoClient()
database = client[DATABASE_NAME]

# Instantiate available models.
modules = {}
for _, unit_id in AVAILABLE_UNITS:
    units[unit_id] = Module(unit_id)

# Construct a MasterController for each module.
controllers = {}
for unit_id, unit in unit.items():
    controllers[unit_id] = MasterController(unit, database)
    controllers[unit_id].start()

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

class Image(Pyro):
    pass


# Define relationships.
Experiment.has_many(Target)
Target.has_many(Image)

# Register Modules,
Unit.delete_all()
for name, unit_id in AVAILABLE_UNITS:
    unit = {}
    unit['name'] = name
    unit['unit_id'] = unit_id
    unit['position'] = {'x': 0, 'y': 0,'z': 0}
    unit['integer_position'] = {'x': 0, 'y': 0,'z': 0}
    unit['camera_status'] = 'active'
    unit['motor_status'] = 'active'
    unit['is_translating'] = False
    unit['last_calibration'] = 0
    unit['image_url'] = 'http://localhost:{}'.format(unit['unit_id'] + 1493)
    Unit.create(unit)

# Launch the server.
app = Application(Pyro)
app.run()


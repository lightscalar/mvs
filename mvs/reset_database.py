from pymongo import MongoClient
from pyro.basics import *



# Connect to the database.
DATABASE_NAME = 'mvs_database'
client = MongoClient()
database = client[DATABASE_NAME]
Pyro.attach_db(database)

# Define resources.
class Experiment(Pyro):
    pass


class Command(Pyro):
    pass


class Target(Pyro):
    pass

# Verify we actually want to nuke the database.
proceed = input('> Are you sure you want to proceed? (y/n) ')
if proceed == 'y':
    Experiment.delete_all()
    Command.delete_all()
    Target.delete_all()
    print('> It is done.')
else:
    print('> Chicken.')






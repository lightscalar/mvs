import threading
from time import sleep, time

class MasterController(threading.Thread):

    def __init__(self, module, database):

        # We'll run in a separate thread.
        threading.Thread.__init__(self)

        # Attach modules, etc.
        self.module = module
        self.db = database
        self.keep_going = True

    def run(self):
        '''Start the controller.'''
        while self.keep_going:
            self.execute_command()
            sleep(1)

    def execute_command(self):
        '''Look for an active command in the database.'''
        commands = self.db.commands
        query = {'active': True, 'module_id': self.module.module_id}
        command_queue = commands.find(query)
        # for command in command_queue:
            # if command['type'] == 'move':
            #     # Assume we have: 'delta' as [dx, dy, dz]
            #     self.module.move(command['delta'])

    def update_schedule(self):
        '''Go to database; find targets; construct schedule.'''
        pass

    def stop(self):
        '''Stop the thread loop.'''
        print('Stopping master controller for module {}'.\
                format(self.module.module_id))
        self.keep_going = False

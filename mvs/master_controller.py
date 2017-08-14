import threading
from time import sleep, time
from scheduler import Scheduler

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
        # Add all available targets to the current schedule.
        targets = self.db.targets
        query = {
            'active': True,
            'module_id': self.module.module_id,
            'end_time': { '$gt': time() }
        }
        cursor = targets.find(query)

        for target in cursor:
            # Create a list containing all of the times
            # to take images at the targets location.
            total_time = target['end_time'] - target['start_time']
            times = []
            i = 0
            for _ in range(total_time / target['update_freq']):
                image_time = target['start_time'] + (target['update_freq'] * i)
                times.append((image_time, target['_id']))

            self.scheduler.add_location(times)



    def stop(self):
        '''Stop the thread loop.'''
        print('Stopping master controller for module {}'.\
                format(self.module.module_id))
        self.keep_going = False

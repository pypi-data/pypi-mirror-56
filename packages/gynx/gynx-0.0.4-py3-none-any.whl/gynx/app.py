#!/usr/bin/python3.6

from gynx.settings import environment as settings
from gynx.core import Gynx
from gynx.core.scheduler import GynxScheduler
from gynx.files.readers import *
from gynx.files.differences import *
from gynx.files.operations import *


class GynxApp(object):
    '''
    Core app class to define and run the main program thread.
    '''

    @property
    def verbose(self):
        return 'verbose' in sys.argv or settings.DEBUG

    @property
    def dry_run(self):
        return 'dry' in sys.argv

    @property
    def schedule(self):
        return 'schedule' in sys.argv

    def run(self):
        '''
        Run program thread:
            1. gynx.core                initialize and authenticate
            2. gynx.files.readers       read local and remote directories
            3. gynx.files.differences   calculate differences between directories
            4. gynx.files.operations    Run sync operations
        '''
        gynx = Gynx()
        if self.verbose:
            print(gynx)
            gynx.print_info()
        local_reader = LocalFileReader(src=gynx.appdir, rootdir=gynx.root, quiet=gynx.quiet)
        local = local_reader.files
        remote_reader = RemoteFileReader(src=gynx.appdir, service=gynx.service, info=gynx.get_info(), quiet=gynx.quiet)
        remote = remote_reader.files
        differences = Differences(
            remote_files=remote,
            local_files=local,
            previous=remote_reader.load(),
            root=gynx.root,
            initial=remote_reader.initial
        )
        if self.dry_run:
            differences.print_all()
        else:
            operations = SyncOperations(
                service=gynx.service,
                changes=differences.all(),
                remote=remote,
                local=local,
                root=gynx.root,
                rf=remote_reader.remote_folders
            )
            operations.run()

if __name__ == '__main__':
    app = GynxApp()
    if app.schedule:
        print('Running sync every %d minutes' % duration)
        duration = sys.argv[sys.argv.index('schedule') + 1]
        scheduler = GynxScheduler(duration=duration)
        scheduler.add_job(app.run)
        scheduler.start()
    else:
        app.run()

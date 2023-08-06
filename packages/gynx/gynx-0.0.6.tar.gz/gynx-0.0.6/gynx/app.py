#!/usr/bin/python3.6

from gynx.settings import environment as settings
from gynx.core import Gynx
from gynx.core.scheduler import GynxScheduler
from gynx.files.readers import *
from gynx.files.differences import *
from gynx.files.operations import *
from gynx.files.changes import *


class GynxApp(object):
    '''
    Core app class to define and run the main program thread.
    '''

    def __init__(
        self,
        verbose=False,
        dry_run=False,
        schedule=False,
        start=False
    ):
        self._verbose = verbose
        self._dry_run = dry_run
        self._schedule = schedule
        self._start = start

    @property
    def verbose(self):
        return 'verbose' in sys.argv or settings.DEBUG or self._verbose

    @property
    def dry_run(self):
        return 'dry' in sys.argv or self._dry_run

    @property
    def schedule(self):
        return 'schedule' in sys.argv or self._schedule

    @property
    def duration(self):
        if self.schedule or self.start:
            si = sys.argv.index('schedule') if 'schedule' in sys.argv else None
            return sys.argv[si+1] if si else 10
        return None

    @property
    def start(self):
        return 'start' in sys.argv or self._start

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
            if self.start:
                local_changes = LocalChanges(
                    rootdir=gynx.root, duration=self.duration, cache=remote
                )
                local_changes.watch()

    def execute(self):
        if self.schedule:
            print('Running sync every %d minutes' % self.duration)
            scheduler = GynxScheduler(duration=self.duration, hours=self._schedule)
            scheduler.add_job(self.run)
            scheduler.start()
        else:
            self.run()

if __name__ == '__main__':
    GynxApp().execute()

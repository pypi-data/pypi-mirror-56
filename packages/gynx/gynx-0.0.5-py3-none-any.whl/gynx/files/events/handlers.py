from watchdog.events import LoggingEventHandler
from gynx.files.readers import RemoteFileReader
from gynx.files.operations import SyncOperations
from gynx.files.events import GynxEvent
import mimetypes
import os


class GynxEventHandler(LoggingEventHandler):

    def __init__(self, gynx, cache=None, rootdir=None, events=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gynx = gynx
        self.service = gynx.service
        self.cache = cache
        self.rootdir = rootdir
        self.operations = SyncOperations(
            service=gynx.service,
            changes=[],
            root=rootdir
        )
        self.events = events

    def find_event(self, search):
        result = []
        for event in self.events:
            valid = True
            for key, value in search.items():
                if getattr(event, key) != value:
                    valid = False
            if valid:
                result.append(event)
        return result

    def read_remote(self):
        self.cache = RemoteFileReader(
            src=self.gynx.appdir,
            service=self.gynx.service,
            info=self.gynx.get_info(),
            quiet=True
        ).files
        return self.cache

    def get_remote_id(self, path):
        '''
        Locate a file in a nested folder dictionary and return file properties.
        Return None if file not found.
        '''
        d = self.cache['drive']
        try:
            path = path.split(self.rootdir)[1]
        except IndexError:
            return (None, None)
        for section in path.split('/'):
            if len(section) > 0:
                try:
                    d = d[section]
                except:
                    return (None, None)
        return (d.get('child_id'), d.get('parent_id'))

    def get_local_mimetype(self, path):
        return mimetypes.guess_type(path)[0]

    def is_lockfile(self, path):
        return (
            path.lower().endswith('.swp') or
            path.lower().endswith('.swx') or
            path.lower().endswith('.lock')
        )

    def handle_upload(self, ge):
        child_path = ge.dest if ge.action == 'MOVE' else ge.path
        parent_path = os.path.split(child_path)[0]
        folder_events = self.find_event(search={
            'ftype': 'folder',
            'path': parent_path
        })
        if folder_events:
            ge.parent_id = folder_events[0].remote_id
        if ge.ftype == 'folder':
            ge.remote_id = self.operations.create_folder(
                name=ge.path.split('/')[-1],
                target='remote',
                path=ge.path,
                parent=ge.parent_id
            )
        else:
            ge.remote_id = self.operations.upload(
                mimetype=self.get_local_mimetype(ge.path),
                local_path=ge.path if ge.action != 'MOVE' else ge.dest,
                folder=ge.parent_id
            )

    def on_created(self, event):
        ge = GynxEvent(
            action='CREATE',
            ftype='folder' if event.is_directory else 'file',
            path=event.src_path
        )
        if not self.is_lockfile(ge.path):
            print(ge)
            self.events.append(ge)
            self.handle_upload(ge)
            self.read_remote()

    def on_deleted(self, event):
        ge = GynxEvent(
            action='DELETE',
            ftype='folder' if event.is_directory else 'file',
            path=event.src_path,
            remote_id=self.get_remote_id(event.src_path)[0]
        )
        if not self.is_lockfile(ge.path):
            print(ge)
            self.events.append(ge)
            self.operations.delete(
                remote_id=ge.remote_id
            )
            self.read_remote()

    def on_modified(self, event):
        ge = GynxEvent(
            action='MODIFY',
            ftype='folder' if event.is_directory else 'file',
            path=event.src_path,
            remote_id=self.get_remote_id(event.src_path)[0],
            parent_id=self.get_remote_id(event.src_path)[1]
        )
        parent_path = os.path.split(ge.path)[0]
        folder_events = self.find_event(search={
            'ftype': 'folder',
            'path': parent_path,
            'action': 'CREATE'
        })
        if folder_events and ge.ftype == 'folder':
            ge.parent_id = folder_events[0].remote_id
            return
        if os.path.exists(ge.path):
            if os.path.samefile(ge.path, self.rootdir):
                return
        print(ge)
        self.events.append(ge)
        self.operations.delete(
            remote_id=ge.remote_id
        )
        self.handle_upload(ge)
        self.read_remote()

    def on_moved(self, event):
        ge = GynxEvent(
            action='MOVE',
            ftype='folder' if event.is_directory else 'file',
            path=event.src_path,
            dest=event.dest_path,
            remote_id=self.get_remote_id(event.src_path)[0],
            parent_id=self.get_remote_id(event.dest_path)[1]
        )
        print(ge)
        self.events.append(ge)
        self.operations.delete(
            remote_id=ge.remote_id
        )
        self.handle_upload(ge)
        self.read_remote()

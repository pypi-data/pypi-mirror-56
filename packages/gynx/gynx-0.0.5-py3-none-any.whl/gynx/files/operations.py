#!/usr/bin/python3.6

import io, os
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.errors import HttpError
from gynx.files.events import GynxEvent


class SyncOperations(object):

    def __init__(
        self, service, changes, remote=None, local=None, root='.', rf=None,
        events=[], testing=False, *args, **kwargs
    ):
        self.service = service
        self.changes = changes
        self.remote = remote
        self.local = local
        self.root = root
        self.current = None
        self.rf = rf
        self.events = events
        self.testing = testing

    def get_relative_path(self, path):
        return path.split(self.root)[-1]

    def get_file_by_path(self, path, files):
        '''
        Locate a file in a nested folder dictionary and return file properties.
        Return None if file not found.
        '''
        d = files['drive']
        for section in path.split('/'):
            if len(section) > 0:
                try:
                    d = d[section]
                except:
                    return None
        return d

    def get_id(self, f):
        try:
            return f['child_id']
        except:
            return None

    def download(self, path, file_id):
        '''
        Download a file from remote drive using the API client
        '''
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print('Download %d%%.' % int(status.progress() * 100))
        return done

    def upload(self, mimetype, local_path, folder=None):
        '''
        Upload a file to a remote drive using the API client
        '''
        file_metadata = {'name': local_path.split('/')[-1]}
        if folder:
            file_metadata['parents'] = [folder]
        try:
            media = MediaFileUpload(local_path, mimetype=mimetype, resumable=True)
        except FileNotFoundError:
            print("Error uploading file:", local_path, '- file does not exist')
            return False
        try:
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
        except HttpError:
            print("Error uploading file:", local_path, '- file is empty')
            return False
        else:
            return file.get('id')

    def delete(self, remote_id=None, local_path=None):
        if remote_id:
            try:
                self.service.files().delete(fileId=remote_id).execute()
            except HttpError:
                print(u'Remote file not found: %s' % (remote_id))
                return False
            else:
                return True
        elif local_path:
            try:
                os.remove(local_path)
            except FileNotFoundError:
                print(
                    u'Local file not found: %s' % u'/' +
                    local_path.split(self.root)[-1]
                )
                return False
            else:
                return True
        else:
            print("Must specify remote ID or local path")
            return False

    def create_folder(self, name, target, path, parent=None):
        '''
        Create a folder in either a local or remote filepath location.
        '''
        if target == 'remote':
            data = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent:
                data['parents'] = [parent]
            folder = self.service.files().create(body=data, fields='id').execute()
            return folder.get('id')
        else:
            os.mkdir(path)
            return None

    def run(self):
        '''
        Run relevant sync operations on all merged differences.
        '''
        current = self.current
        for change in self.changes:
            if change['type'] in ['rename', 'change']:
                action='MODIFY'
            elif change['type'] == 'add':
                action='CREATE'
            elif change['type'] == 'remove':
                action = 'DELETE'
            else:
                action='MOVE'
            event = GynxEvent(
                action=action,
                ftype='folder' if change['folder'] else 'file',
                path=change['local_path'],
                target=change['target']
            )
            print(change['message'])
            if change['target'] == 'remote':
                if change['type']  == 'rename':
                    continue
                f = self.get_file_by_path(self.get_relative_path(change['local_path']), self.local)
                try:
                    if f:
                        parent_name = f['path'].split('/')[-2]
                    else:
                        parent_name = None
                except KeyError or IndexError:
                    parent_name = None
                if parent_name and f:
                    local_parent = self.get_file_by_path(
                        self.get_relative_path('/'.join(f['path'].split('/')[:-1])[1:]),
                        self.local
                    )
                    remote_parent = self.get_file_by_path(
                        self.get_relative_path('/'.join(f['path'].split('/')[:-1])[1:]),
                        self.remote
                    )
                    if local_parent:
                        folder_path = '/'.join(f['path'].split('/')[:-1])
                        if self.rf.get(folder_path):
                            current = self.rf.get(folder_path)
                    elif remote_parent:
                        if len(remote_parent.values()) > 0:
                            current = remote_parent.values()[0].get('parent_id')
                    else:
                        current = None
                else:
                    current = None
                event.parent_id = current
                if f or f == {}:
                    # If file type is folder, create folder
                    if change['folder']:
                        folder = self.create_folder(
                            name=change['local_path'].split('/')[-1],
                            target='remote',
                            path=None,
                            parent=current
                        )
                        event.remote_id = folder
                        current = folder
                    else:
                        # File created in local, upload remote
                        if change['type'] == 'change':
                            # File changed in local, delete first
                            self.delete(remote_id=change['remote_id'])
                        if f:
                            event.remote_id = self.upload(
                                mimetype=f['mimetype'],
                                local_path=change['local_path'],
                                folder=current
                            )
                else:
                    # File deleted in local, delete remote
                    if change.get('remote_id'):
                        rid = change.get('remote_id')
                    else:
                        rid = self.rf.get(u'/'+change['local_path'].split(self.root)[-1])
                    try:
                        self.service.files().delete(fileId=rid).execute()
                    except HttpError:
                        print(u'Remote file not found: %s' % u'/'+change['local_path'].split(self.root)[-1])
                    else:
                        event.remote_id = rid
            else:
                if change['type']  == 'rename':
                    continue
                f = self.get_file_by_path(self.get_relative_path(change['local_path']), self.remote)
                if f or f == {}:
                    # If file type is folder, create folder
                    if change['folder']:
                        event.parent_id = self.create_folder(
                            name=change['local_path'].split('/')[-1],
                            target='local',
                            path=change['local_path']
                        )
                    else:
                        # File created/updated in remote, download to local
                        self.download(change['local_path'], change['remote_id'])
                        event.remote_id = change['remote_id']
                else:
                    # File deleted in remote, delete local
                    try:
                        os.remove(change['local_path'])
                    except FileNotFoundError:
                        print(
                            u'Local file not found: %s' % u'/' +
                            change['local_path'].split(self.root)[-1]
                        )
            self.events.append(event)

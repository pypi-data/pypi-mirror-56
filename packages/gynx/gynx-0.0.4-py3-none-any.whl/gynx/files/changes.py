#!/usr/bin/python3.6

import os
import sys
import time
import logging
from watchdog.observers import Observer
from .handlers import GynxEventHandler


class RemoteChanges:

    def __init__(self, service, *args, **kwargs):
        self.service = service

    def get(self):
        '''
        Full list of changes to remote file system.
        '''
        #fields = 'nextPageToken, changes(time, removed)'
        fields = '*'
        ptr = self.service.changes().getStartPageToken().execute()
        page_token = ptr['startPageToken']
        changes = []
        while page_token is not None:
            response = self.service.changes().list(
                pageToken=page_token, spaces='drive', fields=fields
            ).execute()
            for change in response.get('changes'):
                changes.append(change)
                print('Change found for file: %s' % change.get('fileId'))
            page_token = response.get('nextPageToken')
        return changes

    def watch(self):
        fields = 'nextPageToken, changes(time, removed)'
        ptr = self.service.changes().getStartPageToken().execute()
        page_token = ptr['startPageToken']
        changes = []
        while page_token is not None:
            response = self.service.changes().watch(
                pageToken=page_token, spaces='drive', fields=fields, body={}
            ).execute()
            print(response)

class LocalChanges:

    def __init__(self, rootdir, testing=False, *args, **kwargs):
        self.rootdir=rootdir
        self.testing = testing
        self.observer = Observer()
        self.event_handler = GynxEventHandler()

    def watch(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        path = self.rootdir if os.path.exists(self.rootdir) else "."
        self.observer.schedule(self.event_handler, path, recursive=True)
        self.observer.start()
        count = 0
        try:
            while True:
                time.sleep(1)
                count += 1
                if self.testing and count > 5:
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

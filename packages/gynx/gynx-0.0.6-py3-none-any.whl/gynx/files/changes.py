#!/usr/bin/python3.6

import os
import shutil
import sys
import time
import logging
from watchdog.observers import Observer
from gynx.files.events.handlers import GynxEventHandler


class Changes:

    def __init__(self, gynx, cache=None, testing=False, duration=None, *args, **kwargs):
        self.gynx = gynx
        self.service = gynx.service
        self.cache = cache
        self.testing = testing
        self.duration = duration


class RemoteChanges(Changes):

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

class LocalChanges(Changes):

    def __init__(self, rootdir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rootdir=rootdir
        self.observer = Observer()
        self.event_handler = GynxEventHandler(
            gynx=self.gynx, cache=self.cache, rootdir=self.rootdir
        )

    def test_changes(self, count):
        testfolderpath = os.path.join(self.rootdir, 'testfolder')
        testfilepath = os.path.join(self.rootdir, 'testfile.txt')
        newfilepath = os.path.join(testfolderpath, 'testfile.txt')
        if count == 1:
            os.mkdir(testfolderpath)
            with open(testfilepath, 'w') as testfile:
                testfile.write('test text.')
        if count == 2:
            with open(testfilepath, 'a') as testfile:
                testfile.write('more text.')
        if count == 3:
            os.rename(testfilepath, newfilepath)
        if count == 4:
            os.remove(newfilepath)
            try:
                shutil.rmtree(testfolderpath)
            except OSError:
                pass
        if count > 5:
            raise KeyboardInterrupt

    def watch(self):
        print('Starting local file monitoring...')
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
                if self.testing:
                    self.test_changes(count)
                if self.duration:
                    if count > self.duration * 60:
                        raise KeyboardInterrupt
        except KeyboardInterrupt:
            print('Stopping local file monitoring...')
            self.observer.stop()
        self.observer.join()

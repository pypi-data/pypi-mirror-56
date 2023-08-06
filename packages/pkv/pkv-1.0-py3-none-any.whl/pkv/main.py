import os
import threading
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

__version__ = 1.0

class PKV(object):

    def __init__(self, db='pkv.db'):
        self._data = None
        self._db = db
        self._lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        if not os.path.exists(self._db):
            open(self._db, 'w+').close()

    def _dump(self):
        f = open(self._db, 'w')
        dump(self._data, f, Dumper=Dumper)
        f.close()

    def _load(self):
        f = open(self._db, 'r')
        self._data = load(f.read(), Loader=Loader)
        f.close()

    def set(self, key, value):
        self._lock.acquire()
        self._load()
        self._data[key] = value
        self._dump()
        self._lock.release()

    def get(self, key):
        self._load()
        return self._data.get(key, None)

    def erase(self, key):
        self._lock.acquire()
        self._load()
        res = self._data.pop(key, None)
        self._dump()
        self._lock.release()
        return res

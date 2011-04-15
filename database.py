import os, sys, bsddb3
import xml.etree.ElementTree as xml
import cPickle as pickle

class Game(object):
    def __init__(self, name, info={}):
        self.title = info.get('description', '(no title)')
        self.year = info.get('year', '')
        self.manufacturer = info.get('manufacturer', '')

class Database(object):
    def __init__(self, path):
        self._metadata = bsddb3.db.DB()
        self._metadata.open(path, "metadata", 
            dbtype=bsddb3.db.DB_BTREE, flags=bsddb3.db.DB_CREATE)
        self._supported = bsddb3.db.DB()
        self._supported.open(path, "supported",
            dbtype=bsddb3.db.DB_BTREE, flags=bsddb3.db.DB_CREATE)
        self._available = bsddb3.db.DB()
        self._available.open(path, "available",
            dbtype=bsddb3.db.DB_BTREE, flags=bsddb3.db.DB_CREATE)

    def close(self):
        self._metadata.close()
        self._metadata = None
        self._supported.close()
        self._supported = None
        self._available.close()
        self._available = None

    def __getitem__(self, name):
        if self._supported.has_key(name):
            item = pickle.loads(self._supported[name])
            if self._available.has_key(name):
                item['status'] = 'available'
            else:
                item['status'] = 'supported'
            return Game(name, item)
        raise KeyError

    def add(self, name):
        if not self._supported.has_key(name):
            raise KeyError("game %s is not supported" % name)
        self._available[name] = ''

    def __iter__(self):
        class _Iterator(object):
            def __init__(self, cursor, available):
                self.cursor = cursor
                self.available = available
            def __iter__(self):
                return self
            def next(self):
                if not self.cursor:
                    raise StopIteration()
                try:
                    name,_ = self.cursor.next()
                    item = pickle.loads(self.available[name])
                    item['name'] = name
                    return item
                except:
                    pass
                raise StopIteration()
            def close(self):
                self.cursor.close()
                self.cursor = None
                self.available = None
        return _Iterator(self._supported.cursor(), self._available)

    def resync(self, xmlpath):
        with file(xmlpath, 'r') as infile:
            tree = xml.parse(infile)
            root = tree.getroot()
            self._metadata['build'] = str(root.attrib['build'])
            for element in root.findall("game"):
                game = dict()
                name = element.attrib['name']
                try:
                    game['description'] = element.find("description").text
                except:
                    pass
                try:
                    game['year'] = element.find("year").text
                except:
                    pass
                try:
                    game['manufacturer'] = element.find("manufacturer").text
                except:
                    pass
                self._supported[name] = pickle.dumps(game)

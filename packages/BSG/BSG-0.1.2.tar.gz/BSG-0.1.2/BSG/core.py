#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys
import random, json, time
import inspect

this_dir, this_filename = os.path.split(__file__)
_defaultData = os.path.join(this_dir, "default.json")
class bullShit():
    '''An object that can generate random bullShit.
    
    Arguments:
    -------------
    theme       - str. 
                  The main theme you want to discuss about
    jsonFile    - str, Optional, default None. 
                  A file that stores the famous words and boshes. By default, 
                  a basic data package would be loaded internally from this 
                  package.
    repeatLevel - int, Optional, default 2. 
    wordLimit   - int, Optional, default 1000.
    
    Returns:
    -------------
    Try print(bullShit(<theme>) to see what happens.
    '''
    def __init__(self, theme, JSON = None, BSDB = None, BSDBPath = None, 
                 repeatLevel = 2, wordLimit = 1000):
        if JSON == None and BSDB == None:
            JSON = _defaultData
            self.data = json.loads(open(JSON, 'r', encoding = "utf-8").read())
        elif JSON != None and BSDB == None:
            self.data = json.loads(open(JSON, 'r', encoding = "utf-8").read())
        elif JSON == None and BSDB != None:
            if BSDBPath == None:
                BSDBPath = ''
            self.data = bsDatabase(name = BSDB, dbPath = BSDBPath)
        else:
            raise ValueError('Only one type of data source is supported for now')
        self.dbType, self.dbName = _getNotNone(JSON, BSDB)
        self.before = self.data['before']
        self.after = self.data['after']
        self.bible = self.data['Bible']
        self.theme = theme
        self._wordLimit = wordLimit
        self.repeatLevel = repeatLevel
        self.famousGen = self._sentence('famous')
        self.boshGen = self._sentence('bosh')
        self.POOPOO(wordLimit)

    def POOPOO(self, wordLimit = None):
        '''Generate new paragraphs of bullShit. Is run once by default when 
        initializing, but can be applied whenever you what to get new stuffs.

        Argument:
        ------------
        wordLimit - int. Optional, default None. By default, it will use the 
                    intrinsic value specified when initializing this object.

        Returns:
        -----------
        Update the essay stored in the object. 
        '''
        self.essay = '　　'
        if wordLimit == None:
            wordLimit = self._wordLimit
        while len(self.essay) < wordLimit:
            dice = random.randint(0, 100)
            if dice < 5:
                self._nextParagraph()
            elif dice < 20:
                self._addFullSentence()
            else:
                self._addBosh()
        self.essay = self.essay.replace('x', self.theme)

    def unlimitedPOOPOO(self, intervalTime, interruptPENALTY = 10):
        '''BE CAREFUL WHEN USING THIS!
        Press Ctrl + Z to really stop it
        Arguments:
        -------------
        intervalTime - int.
                       In the unit of second.
        interruptPENALTY - int.
                           In the unit of second.'''
        assert type(intervalTime) == int
        while True:
            try:
                self.essay = '　　'
                for i in range(3):
                    self._addFullSentence()
                self._addBosh()
                for i in range(2):
                    self._addFullSentence()
                self.essay += '\r\n'
                self.essay = self.essay.replace('x', self.theme)
                sys.stdout.write(self.essay)
                time.sleep(intervalTime)
            except KeyboardInterrupt:
                self._throwSXC(wait = interruptPENALTY)

    def _throwSXC(self, wait = 10):
        assert type(wait) == int, "I only want to wait for <int> second(s)"
        try:
            dirt = random.choice(self.bible)
            sys.stdout.write('\n\n　　'+dirt+'\n　　给老子等%d秒\n'%wait)
            time.sleep(wait)
        except KeyboardInterrupt:
            self._throwSXC(wait + 1) 

    def _sentence(self, Type):
        pool = list(self.data[Type]) * self.repeatLevel
        while True:
            random.shuffle(pool)
            for i in pool:
                yield i

    def _addFullSentence(self):
        sentence = next(self.famousGen)
        sentence = sentence.replace('a', random.choice(list(self.before)))
        sentence = sentence.replace('b', random.choice(list(self.after)))
        self.essay += sentence

    def _addBosh(self):
        self.essay += next(self.boshGen)

    def _nextParagraph(self):
        self.essay += '\r\n'
        self.essay += '　　'

    def __str__(self):
        return self.essay

    def __repr__(self):
        return 'NMSL'

class bsDatabase(object):
    """Manage the database, by either creating your customized new database, 
    or modifying already existing database. 
    PLANNING to place the database like this:
    <NAMEofDB>
    |__.BSDBID
       famous.json
       before.json
       after.json
       bosh.json
    In .dbID, say some BS. """
    # Examine existing database first
    def __init__(self, name = 'BSDB', dbPath = '', overwrite = False):
        self.famous = set()
        self.before = set()
        self.after = set()
        self.bosh = set()
        self.overwrite = overwrite
        self.name = name
        self.dbPath = dbPath
        if _dbExists(os.path.join(self.dbPath, name)):
            if not overwrite:
                self.readDB(name)
        self.written = False
        self.Dict = {'famous': self.famous, 'before': self.before, 
                         'after': self.after, 'bosh': self.bosh}

    def readDB(self, name, overwrite = False):
        '''Parse a database folder by giving a name. Absolute or relative path 
        can be added at the start. 
        Arguments:
        -------------
        name      - str. 
                    The name of the BS database
        overwrite - Boolean. Optional, default False.
                    Whether to overwrite the already existing content inside 
                    this object. If True, it dose; otherwise, it makes the 
                    union.
        Returns:
        -----------
        Update the bsDatabase object content.
        '''
        famousPath = os.path.join(self.dbPath, name, 'famous.json')
        beforePath = os.path.join(self.dbPath, name, 'before.json')
        afterPath = os.path.join(self.dbPath, name, 'after.json')
        boshPath = os.path.join(self.dbPath, name, 'bosh.json')

        famous = json.loads(open(famousPath, 'r', encoding = "utf-8").read())
        before = json.loads(open(beforePath, 'r', encoding = "utf-8").read())
        after = json.loads(open(afterPath, 'r', encoding = "utf-8").read())
        bosh = json.loads(open(boshPath, 'r', encoding = "utf-8").read())

        if overwrite:
            self.famous = set(famous['famous'])
            self.before = set(before['before'])
            self.after = set(after['after'])
            self.bosh = set(bosh['bosh'])
        else:
            self.famous = self.famous.union(set(famous['famous']))
            self.before = self.before.union(set(before['before']))
            self.after = self.after.union(set(after['after']))
            self.bosh = self.bosh.union(set(bosh['bosh']))

    def changePath(self, newPath, newName = None):
        self.dbPath = newPath
        if newName != None:
            self.name = newName

    def addBS(self, data, bsType):
        '''Add new BS words to the database, with bsType in {'famous', 
        'before', 'after', 'bosh'} specified.'''
        if type(data) == str:
            data = [data]
        elif type(data) == list:
            pass
        else:
            raise TypeError('Only accept a single sentence or a list of \
                             sentences.')
        if bsType == 'famous':
            data = set([s+'b' for s in data])
        else:
            data = set(data)
        self.Dict[bsType] = self.Dict[bsType].union(data)

    def save(self, name = None, path = None, comment = ''):
        '''save the database. You still got a chance to rename the object, or 
        change the place to save it. '''
        if path == None:
            path = self.dbPath
        else:
            self.dbPath = path
        if name == None:
            name = self.name
        else:
            self.name = name
        path = os.path.join(path, name)
        self.written = True
        if not os.path.exists(path):
            os.makedirs(path)
        for t, data in self.Dict.items():
            filePath = os.path.join(path, t+'.json')
            with open(filePath, 'w', encoding = "utf-8") as outFile:
                json.dump({t: list(data)}, outFile, sort_keys = True, indent = 2)
            outFile.close()
        bsdbid = open(os.path.join(path, '.BSDBID'), 'w', encoding = "utf-8")
        bsdbid.write(comment)
        bsdbid.close()
            

    def nContents(self):
        '''Returns the total number of sentences included in the database'''
        return len(self.famous) + len(self.before) + len(self.after) \
               + len(self.bosh)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.written:
            w = 'Written'
        else:
            w = 'Untouched yet'
        info = '<bsDatabase at %s, with %d contents inside. %s>' % \
               (os.path.join(self.dbPath, self.name), self.nContents(), w)
        return info

    def __getitem__(self, key):
        return self.Dict[key]       

def _dbExists(name):
    return os.path.isdir(name) and \
           os.path.exists(os.path.join(name, '.BSDBID'))

def _getNotNone(*args):
    '''Take multiple variables and return the first one that is not NoneType 
    with both its variable name while inputing and the value.
    Method referencing: https://stackoverflow.com/a/18425523
    Example:
    -----------
    >>> a = None
    >>> b = 2
    >>> c = 'NMSL'
    >>> _getNotNone(c, a, b)
    ('c', 'NMSL')
    '''
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    for var in args:
        if var != None:
            #print(callers_local_vars)
            names = [var_name for var_name, var_val in callers_local_vars if var_val is var]
            return names[0], var

if __name__ == '__main__':
    '''DEBUG region'''
    pass
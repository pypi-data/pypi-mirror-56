"""Simple database module.


Authors: Valentyn Stadnytskyi
Date created: 2019-11-21

Python Version: 2.7 and 3.7
"""
from logging import debug,info,warning,error

__version__ = "1.5.6" # Issue: WindowsError in remove(settings_file)
from pdb import pm
from threading import RLock
lock = RLock()

from os import getcwd

class DataBase():
    def __init__(self,root,name):
        """
        initializes the connection to the database.

        Parameters
        ----------
        root :: (string)
            path or environment variable
        name :: (string)
            name of the database

        Returns
        -------

        Examples
        --------
        >>> write()
        """
        self.filename, self.root, self.name = self.get_filename(root,name)
        self.database = self.read()

    def get_filename(self,root,name):
        """
        generates filename based on input root and name. There are few special keywords like $TEMPDIR, $LOCALDIR that will obtain the locations of temporary and local directories.

        Parameters
        ----------
        root :: (string)
            path or environment variable
        name :: (string)
            name of the database

        Returns
        -------
        filename :: (string)
            full path from the home directory, including the name of the file.

        Examples
        --------
        >>> filename = get_filename(root, 'name')
        """
        from platform import system
        if system() == 'Darwin':
            bracket = '/'
        if system() == 'Windows':
            bracket = '\\'


        if root == "$TEMPDIR":
            from tempfile import gettempdir
            root = gettempdir() + bracket +'SavedProperty' + bracket
        elif root == "$LOCALDIR" or root == "":
            from os import getcwd
            root = getcwd() + bracket+'SavedProperty'+ bracket
        else:
            root = root + bracket+ 'SavedProperty' + bracket
        filename = root + name + '_db.py'
        return filename, root, name

    def read(self):
        """
        reads the database file

        Parameters
        ----------

        Returns
        -------
        dictionary :: (dictionary)
            returns a dictionary of all data in the database file.

        Examples
        --------
        >>> data = read()
        """
        import yaml
        from os.path import exists
        if exists(self.filename):
            with lock:
                with open(self.filename) as handle:
                    try:
                        data = yaml.safe_load(handle.read())  # (2)
                        return data
                    except yaml.YAMLError:
                        return {}  # (3)
        else:
            return {}

    def write(self):
        """
        writes current dictionary saved in memory to the database file

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        >>> write()
        """
        import yaml
        data = self.database
        with lock:
            with open(self.filename, 'w') as handle:
                yaml.dump(data, handle)

    def sync(self):
        """
        reads the database file and updates the self.database variable accordingly.

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        >>> sync()
        """
        self.database = self.read()


    def close(self):  # (4)
        pass

class SavedProperty():
    def __init__(self,db,name,value):
        self.name = name
        self.db = db
        self.default_value = value

    def init(self):
        """
        wrapper that returns property object with get and set functions.

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        >>> from saved_property import DataBase, SavedProperty
        >>> db = DataBase(root = '', name = 'simpledb')
        >>> d = SavedProperty(db,'d',5.0).init()
        """
        return property(self.get,self.set)

    def set(self,name,value) :
        """
        setter for SavedProperty. sets value  in the database

        Parameters
        ----------
        name :: (string)
            name of the entry in the database.
        value :: (object)
            value saved to the database.

        Returns
        -------

        Examples
        --------
        >>>
        """
        self.db.database[self.name] = value
        self.db.write()

    def get(self,name):
        """
        getter for SavedProperty. returns saved value if it exists in the database, otherwise returns default_value

        Parameters
        ----------
        name :: (string)
            name of the entry in the database.

        Returns
        -------
        value :: (object)
            returns a value stored with the selected key in the database

        Examples
        --------
        >>>
        """
        if self.name in list(self.db.database.keys()):
            return self.db.database[self.name]
        else:
            return self.default_value

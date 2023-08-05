import os
import json

class CrudlDB():
    """Base class for all CRUDL DB implementations.

    It provides common management of configuration arguments
    for a db connection that can also be retrieved from env vars.
    The configuration is specified via non-positional arguments.
    For any None config value, the values is (attempted to be)
    read from the environment variables. The config value's key
    is appended to cfg_prefix (if set) and transformed to upper
    case letters if cfg_upper is True. If an environment variable
    with that name exists, the config is set to it. If none is found
    the value is left as None.

    In addition, CridlDB implements __enter__ and __exit__ methods
    that can be used to initialize database connections.

    Any child must implement the following methods:

    - _open (open db connection, used by __enter__)
    - _close (close db connection, used by __exit__)
    - create (create an entry)
    - read (read the complete list of entries)
    - read_one (read a single entry)
    - update (update entries)
    - delete (delete entries)
    - list (list entries with pagination)
    - count (count entries)
    - execute (execute a specific command)
    - commit (commit current operations to database)

    For details on their expected signature see the docstring
    of each method.

    Parameters
    ----------
    cfg_prefix: str, default: None
        prefix of environment variables holding config
    cfg_upper: bool, default: True
        Should the cfg keys be transformed to upper case
        when checking environment variables?
    **cfg: dict, default: None
        config arguments

    Examples
    --------
    os.environ["MY_DB_HOST"] = "localhost"
    os.environ["MY_DB_BLA"] = "dummy value"
    db = CrudlDB("MY_DB_", host=None, port=None, bla="fasel")
    assert db.host == "localhost"
    assert db.port == None
    assert db.bla == "fasel"
    """
    def __init__(self, cfg_prefix=None, cfg_upper=True, **cfg):
        self.cfg_prefix = cfg_prefix
        self.cfg_upper = cfg_upper
        for k,v in cfg.items():
            if v is None:
                v = self._from_env(k)
            setattr(self, k, v)

    def _from_env(self, k):
        """Read config parameters from environment variables."""
        if self.cfg_upper:
            k = k.upper()
        if self.cfg_prefix is not None:
            name = "{}{}".format(self.cfg_prefix, k)
        return os.getenv(name, None)

    def __enter__(self):
        """Create and open a database connection."""
        self._open()
        return self

    def __exit__(self, type, value, traceback):
        """Close the database connection."""
        self._close()

    def __str__(self):
        return "{}:{}@{}:{}/{}".format(
            self.username, self.password,
            self.host, self.port,
            self.db_name
        )

    def _open(self):
        """Open the database connection."""
        raise NotImplementedError("_open not implemented for {}".format(type(self).__name__))

    def _close(self):
        """Close the database connection."""
        raise NotImplementedError("_close not implemented for {}".format(type(self).__name__))

    def create(self, table, values, commit=True):
        """Create a new entry.

        Parameters
        ----------
        table: str
            name of the table or collection
        values: dict
            specification of entry properties
        commit: bool, default True
            should the changes to the db be immediately commited?
        """
        raise NotImplementedError("create not implemented for {}".format(type(self).__name__))

    def read(self, table, props=None, filters=None, order_by=None):
        """Read the complete list of entries.

        Parameters
        ----------
        table: str
            name of the table or collection
        props: list, default None
            list of properties to retrieve, None for all
        filters: list of tuples/triples, default None
            list of filters in the form (prop, value, comp=None)
            - prop is the property to filter
            - value is the value used for comparison
            - comp is the comparator string, if None equality is used
        order_by: list of tuples, default None
            list of order statements where each statement
            is a pair in the form (prop, order) where
            order is either asc or desc
        """
        raise NotImplementedError("read not implemented for {}".format(type(self).__name__))

    def read_one(self, table, props=None, filters=None, order_by=None):
        """Read a single entry.

        If the filters result in more than a single entry, the first one
        is returned.

        Parameters
        ----------
        table: str
            name of the table or collection
        props: list, default None
            list of properties to retrieve, None for all
        filters: list of tuples/triples, default None
            list of filters in the form (prop, value, comp=None)
            - prop is the property to filter
            - value is the value used for comparison
            - comp is the comparator string, if None equality is used
        order_by: list of tuples, default None
            list of order statements where each statement
            is a pair in the form (prop, order) where
            order is either asc or desc
        """
        raise NotImplementedError("read_one not implemented for {}".format(type(self).__name__))

    def update(self, table, values, filters=None, commit=True):
        """Update one or more entries.

        Parameters
        ----------
        table: str
            name of the table or collection
        values: dict
            specification of new entry properties
        filters: list of tuples/triples, default None
            list of filters in the form (prop, value, comp=None)
            - prop is the property to filter
            - value is the value used for comparison
            - comp is the comparator string, if None equality is used
        commit: bool, default True
            should the changes to the db be immediately commited?
        """
        raise NotImplementedError("update not implemented for {}".format(type(self).__name__))

    def delete(self, table, filters=None, commit=True):
        """Delete one or more entries.

        Parameters
        ----------
        table: str
            name of the table or collection
        filters: list of tuples/triples, default None
            list of filters in the form (prop, value, comp=None)
            - prop is the property to filter
            - value is the value used for comparison
            - comp is the comparator string, if None equality is used
        commit: bool, default True
            should the changes to the db be immediately commited?
        """
        raise NotImplementedError("delete not implemented for {}".format(type(self).__name__))

    def list(self, table, props=None, filters=None, order_by=None, limit=None, offset=None, paging=True):
        """Retrieve a list of entries using/with pagination.

        Parameters
        ----------
        table: str
            name of the table or collection
        props: list, default None
            list of properties to retrieve, None for all
        filters: list of tuples/triples, default None
            list of filters in the form (prop, value, comp=None)
            - prop is the property to filter
            - value is the value used for comparison
            - comp is the comparator string, if None equality is used
        order_by: list of tuples, default None
            list of order statements where each statement
            is a pair in the form (prop, order) where
            order is either asc or desc
        limit: int, default None
            maximum number of entries to return
        offset: int, default None
            index of entry in resulting list to start from
        paging: bool, default True
            should paging information be added to the result?
            True: return dict with paging (total, limit, offset) and data (entries)
            False: return only list of entries
        """
        raise NotImplementedError("list not implemented for {}".format(type(self).__name__))

    def read_query(self, query):
        """Retrieve a list of entries from a query.

        Parameters
        ----------
        query: str
            query to execute
        """
        raise NotImplementedError("read_query not implemented for {}".format(type(self).__name__))

    def count(self, table, filters=None):
        """Return total number of entries.

        Parameters
        ----------
        table: str
            name of the table or collection
        filters: list of tuples/triples, default None
            list of filters in the form (prop, value, comp=None)
            - prop is the property to filter
            - value is the value used for comparison
            - comp is the comparator string, if None equality is used
        """
        raise NotImplementedError("count not implemented for {}".format(type(self).__name__))

    def execute(self, query):
        """Execute the query in the database."""
        raise NotImplementedError("execute not implemented for {}".format(type(self).__name__))

    def commit(self):
        """Commit all open changes to the database."""
        raise NotImplementedError("commit not implemented for {}".format(type(self).__name__))

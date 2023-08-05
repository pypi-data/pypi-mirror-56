import sqlite3
import logging

from .mysql_db import MysqlDB

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SqliteDB(MysqlDB):
    """CRUDL wrapper for an sqlite3 database.

    Parameters
    ----------
    db_name: str, default None
        database to use (determines filename for persistence)
    cfg_prefix: str, default "MYSQL_SERVICE_"
        prefix of environment variables holding config
    cfg_upper: bool, default: True
        Should the cfg keys be transformed to upper case
        when checking environment variables?
    """
    def __init__(self, db_name=None, cfg_prefix="SQLITE_", cfg_upper=True):
        super().__init__(cfg_prefix=cfg_prefix,
                         cfg_upper=cfg_upper,
                         db_name=db_name)

    def _open(self):
        self.connection = sqlite3.connect("{}.db".format(self.db_name))
        self.connection.row_factory = dict_factory

    def _close(self):
        self.connection.close()

    def _cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

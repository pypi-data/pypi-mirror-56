import mysql.connector
import logging

from .crudl_db import CrudlDB

class MysqlDB(CrudlDB):
    """CRUDL wrapper for a MySQL database.

    Parameters
    ----------
    host: str, default None
        database host
    port: int, default None
        database port
    username: str, default None
        database username
    password: str, default None
        database password
    db_name: str, default None
        database to select
    cfg_prefix: str, default "MYSQL_SERVICE_"
        prefix of environment variables holding config
    cfg_upper: bool, default: True
        Should the cfg keys be transformed to upper case
        when checking environment variables?
    """
    def __init__(self, host=None, port=None, username=None, password=None, db_name=None, cfg_prefix="MYSQL_", cfg_upper=True):
        super().__init__(cfg_prefix=cfg_prefix,
                         cfg_upper=True,
                         host=host,
                         port=port,
                         username=username,
                         password=password,
                         db_name=db_name)

    def _open(self):
        self.db = mysql.connector.connect(
            host=self.host,
            port=int(self.port),
            user=self.username,
            passwd=self.password,
            database=self.db_name
        )

    def _close(self):
        self.db.close()

    def _cursor(self):
        return self.db.cursor(dictionary=True)

    def _wrap_table(self, name):
        return "`{}`".format(name)

    def _wrap_column(self, col):
        return "`{}`".format(col)

    def _wrap_value(self, value):
        if type(value) is str:
            return "'{}'".format(value.replace("'", "\\'"))
        elif type(value) in [int, float, bool]:
            return str(value)
        elif type(value) is dict or type(value) is list:
            return "'{}'".format(json.dumps(value).replace("'", "\\'"))
        else:
            return "'{}'".format(value)

    def _filter(self, column, value, comparator="="):
        return "{}{}{}".format(self._wrap_column(column),
                               comparator,
                               self._wrap_value(value))

    def _filters(self, filters):
        where = "" if filters is None else " WHERE {}".format(
                        " AND ".join([self._filter(*f) for f in filters])
                    )
        return where

    def _order_by(self, order_by):
        if order_by is None:
            return ""
        else:
            return " ORDER BY {}".format(
                ", ".join(["{} {}".format(self._wrap_column(o[0]), o[1])
                           for o in order_by])
            )

    def _limit(self, limit, offset):
        if limit is not None and offset is not None:
            return " LIMIT {},{}".format(offset, limit)
        elif limit is not None:
            return " LIMIT {}".format(limit)
        else:
            return ""

    def _create_query(self, table, values):
        query = "INSERT INTO {} ({}) VALUES ({});".format(
            self._wrap_table(table),
            ",".join([self._wrap_column(k) for k in values.keys()]),
            ",".join([self._wrap_value(v) for v in values.values()])
        )
        return query

    def _update_query(self, table, values, filters=None):
        query = "UPDATE {} SET {}{};".format(
            self._wrap_table(table),
            ",".join(["{}={}".format(self._wrap_column(k),
                                     self._wrap_value(v)) for k,v in values.items()]),
            self._filters(filters)
        )
        return query

    def _delete_query(self, table, filters=None):
        query = "DELETE FROM {}{};".format(
            self._wrap_table(table),
            self._filters(filters)
        )
        return query

    def _list_query(self, table, props=None, filters=None, order_by=None, limit=None, offset=None):
        what = "*" if props is None else ",".join([self._wrap_column(p) for p in props])
        query = "SELECT {} FROM {}{}{}{};".format(
            what,
            self._wrap_table(table),
            self._filters(filters),
            self._order_by(order_by),
            self._limit(limit, offset)
        )
        return query

    def _count_query(self, table, filters=None):
        query = "SELECT COUNT(*) as `count` FROM {}{};".format(
            self._wrap_table(table),
            self._filters(filters)
        )
        return query

    def _fetch_all(self, query):
        cursor = self._cursor()
        cursor.execute(query)
        res = [x for x in cursor.fetchall()]
        return res

    def create(self, table, values, commit=True):
        query = self._create_query(table, values)
        logging.debug("ADD: {}".format(query))
        cursor = self._cursor()
        result  = cursor.execute(query)
        if commit:
            self.commit()
            new_id = cursor.lastrowid
            logging.debug("ADD: new id is {}".format(new_id))
            return new_id
        else:
            return None

    def read(self, table, props=None, filters=None, order_by=None):
        query = self._list_query(table, props=props, filters=filters, order_by=order_by)
        logging.debug("READ_ONE: {}".format(query))
        res = self._fetch_all(query)
        return res

    def read_one(self, table, props=None, filters=None, order_by=None):
        query = self._list_query(table, props=props, filters=filters, order_by=order_by, limit=1, offset=0)
        logging.debug("READ_ONE: {}".format(query))
        res = self._fetch_all(query)
        if len(res) < 1:
            raise KeyError("No entry in {} found with filters {}".format(table, filters))
        return res[0]

    def read_query(self, query):
        logging.debug("READ_QUERY: {}".format(query))
        data = self._fetch_all(query)
        return data

    def update(self, table, values, filters=None, commit=True):
        query = self._update_query(table, values, filters=filters)
        logging.debug("PATCH: {}".format(query))
        cursor = self._cursor()
        cursor.execute(query)
        if commit:
            self.commit()
        else:
            pass

    def delete(self, table, filters=None, commit=True):
        query = self._delete_query(table, filters)
        logging.debug("DROP: {}".format(query))
        cursor = self._cursor()
        cursor.execute(query)
        if commit:
            self.commit()
        else:
            pass

    def list(self, table, props=None, filters=None, order_by=None, limit=None, offset=None, paging=True):
        query = self._list_query(table, props=props, filters=filters, order_by=order_by, limit=limit, offset=offset)
        logging.debug("LIST: {}".format(query))
        data = self._fetch_all(query)
        if not paging:
            return data
        else:
            total = self.count(table, filters=filters)
            return {
                "paging": {
                    "total": total,
                    "limit": limit,
                    "offset": offset
                },
                "data": data
            }

    def count(self, table, filters=None):
        query = self._count_query(table, filters=filters)
        logging.debug("COUNT: {}".format(query))
        res = self._fetch_all(query)
        return res[0]["count"]

    def execute(self, query):
        cursor = self._cursor()
        return cursor, cursor.execute(query)

    def commit(self):
        self.db.commit()

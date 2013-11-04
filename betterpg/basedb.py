# coding: utf-8
"""
psycopg2 wrapper
"""
import psycopg2
import traceback
from .utils import make_query_string

class BetterPgException(Exception):
    pass

class BaseDB(object):
    """
    Wrapper for psycopg2
    """
    def __init__(self, dbconfig):
        self.cx = psycopg2.connect(**dbconfig)
        self.cu = self.cx.cursor()

    def execute(self, sql, params=[], auto_commit=True):
        try:
            self.cu.execute(sql, params)
            if auto_commit:
                self.cx.commit()
        except:
            print traceback.format_exc()
            self.cx.rollback()

    def commit(self):
        self.cx.commit()

    def dict_query(self, sql, params=[]):
        """
        Query and fetch the result as dict
        """
        self.cu.execute(sql, params)
        desc = self.cu.description
        return (
            dict(zip([col[0] for col in desc], row))
            for row in self.cu.fetchall()
        )

    def query(self, sql, params=[]):
        self.cu.execute(sql, params)
        return self.cu.fetchall()

    def insert_dict(self, table, item):
        placeholders = ",".join(("%s",) * len(item))
        statement = '''
        INSERT INTO %s (%s) VALUES (%s)
        ''' % (
            table, 
            " ,".join(item.keys()), 
            placeholders
        )
        self.execute(statement, item.values())

    def exists(self, table, query="", params={}):
        if params:
            query = make_query_string(params)
        assert query, BetterPgException("need query string or params.")
        return bool(self.query("select 1 from %s where %s limit 1" % (table, query)))

    def delete(self, table, query="", params={}):
        if params:
            query = make_query_string(params)
        assert query, BetterPgException("need query string or params.")
        self.execute("delete from %s where %s" % (table, query))

    def close(self):
        self.cu.close()
        self.cx.close()


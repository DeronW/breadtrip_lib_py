#coding: utf-8
from psycopg2.extensions import adapt

def make_query_string(params):
    s = []
    for k, v in params.items():
        s.append("%s = %s" % (k, adapt(v)))
    return " and ".join(s)


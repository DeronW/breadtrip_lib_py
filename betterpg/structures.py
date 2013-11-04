#coding: utf-8
from psycopg2.extensions import adapt, register_adapter, AsIs

class Point(object):
    """
    y -> lat, x -> lon
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "<Point (%s,%s)>" % (self.x, self.y)

def adapt_point(point):
    return AsIs("ST_GeomFromText('POINT(%s %s)', 4326)" % (point.x, point.y))

register_adapter(Point, adapt_point)

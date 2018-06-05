#!/usr/bin/env python
import psycopg2
import psycopg2.extras

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

class MsploitPostgres(object):

    def __init__(self,user,password,db,cursorfactory=psycopg2.extras.DictCursor):
        self._user = user
        self._password = password
        self._db = db
        self._cursorfactory = cursorfactory
        self._cur = self._connect()

    def _connect(self):
        try:
            conn = psycopg2.connect("dbname='{}' user='{}' host='localhost' password='{}'".format(self._db,self._user,self._password))
        except Exception:
            print "I am unable to connect to the database"
        else:
            return conn.cursor(cursor_factory=self._cursorfactory)

    def getAllHosts(self):
        self._cur.execute("SELECT * FROM public.hosts")
        return self._cur.fetchall()

    def getHost(self):
        self._cur.execute("SELECT * FROM public.hosts")
        yield self._cur.fetchone()

    def getLootforHost(self,host):
        self._cur.execute("SELECT hosts.address,hosts.id,loots.* FROM public.hosts, public.loots WHERE hosts.id = loots.host_id and hosts.address = '{}'".format(host))
        return self._cur.fetchall()

    def getforHost(self,host,table):
        self._cur.execute("SELECT hosts.address,hosts.id,{}.* FROM public.hosts, public.{} WHERE hosts.id = {}.host_id and hosts.address = '{}'".format(table,table,table,host))
        return self._cur.fetchall()
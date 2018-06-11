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
        # try:
        # conn = psycopg2.connect("dbname='{}' user='{}' host='localhost' password='{}'".format(self._db,self._user,self._password))
        conn = psycopg2.connect(dbname=self._db, user=self._user, host="localhost", password=self._password)
        # except Exception:
        #     print "I am unable to connect to the database"
        # else:
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

    def getForAllHosts(self,table):
        self._cur.execute(
            "SELECT hosts.address,hosts.id,{}.* FROM public.hosts, public.{} WHERE hosts.id = {}.host_id".format(table, table, table))
        return self._cur.fetchall()

    def getSessionDetails(self,sessionid):
        self._cur.execute("SELECT sessions.id,session_events.* FROM public.sessions, public.session_events WHERE sessions.id = session_events.session_id and sessions.id = '{}'".format(sessionid))
        return self._cur.fetchall()

    def getCredentials(self):
        self._cur.execute("SELECT metasploit_credential_privates.id, metasploit_credential_privates.type, metasploit_credential_privates.data, metasploit_credential_privates.jtr_format, metasploit_credential_publics.id,   metasploit_credential_publics.username, metasploit_credential_cores.origin_type FROM   public.metasploit_credential_privates, public.metasploit_credential_publics, public.metasploit_credential_cores WHERE   metasploit_credential_cores.private_id = metasploit_credential_privates.id AND metasploit_credential_cores.public_id = metasploit_credential_publics.id;")
        return self._cur.fetchall()

    def getwebpagesforhost(self,host):
        sql = "SELECT web_sites.vhost, web_sites.comments, web_sites.options, web_sites.id as websiteid,web_pages.web_site_id,web_pages.path,web_pages.query,web_pages.code,web_pages.cookie,web_pages.headers,  web_pages.body,web_sites.service_id,services.id as serviceid,services.port,services.proto,services.state,   services.name as protoname, services.info FROM public.web_sites, public.web_pages, public.services WHERE   web_sites.service_id = services.id AND web_sites.id = web_pages.web_site_id AND web_sites.vhost = '{}';".format(host)
        self._cur.execute(sql)
        return self._cur.fetchall()

    def getwebformsforhost(self,host):
        sql = "SELECT web_forms.web_site_id, web_forms.created_at, web_forms.id, web_forms.path, web_forms.method,   web_forms.params, web_forms.query, web_sites.id, web_sites.vhost, web_sites.options, web_sites.comments,  services.port, services.proto, services.name as protoname, services.info FROM public.web_forms, public.web_sites,   public.services WHERE web_sites.id = web_forms.web_site_id AND web_sites.service_id = services.id AND web_sites.vhost = '{}';".format(host)
        self._cur.execute(sql)
        return self._cur.fetchall()

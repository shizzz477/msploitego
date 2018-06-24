#!/usr/bin/env python
import psycopg2
import psycopg2.extras

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
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

    def getAllHosts(self,wid):
        self._cur.execute("SELECT hosts.* FROM public.workspaces, public.hosts WHERE workspaces.id = hosts.workspace_id AND workspaces.id = {};".format(wid))
        return self._cur.fetchall()

    def getLootforHost(self,host):
        self._cur.execute("SELECT hosts.address,hosts.id,loots.* FROM public.hosts, public.loots WHERE hosts.id = loots.host_id and hosts.id = '{}'".format(host))
        return self._cur.fetchall()

    def getforHost(self,hostid,table):
        self._cur.execute("SELECT hosts.address,hosts.id,{}.* FROM public.hosts, public.{} WHERE hosts.id = {}.host_id and hosts.id = '{}'".format(table,table,table,hostid))
        return self._cur.fetchall()

    def getVulnsForHost(self,hostid):
        sql = "SELECT hosts.id as hostid, workspaces.id as workspaceid, workspaces.name as workspace, vulns.id as vulnid, services.name as servicename, services.proto, services.port, services.info as serviceinfo, services.id as serviceid, vulns.created_at, vulns.name as vulnname, vulns.updated_at, vulns.info as vulninfo, vulns.exploited_at,   vulns.vuln_detail_count, vulns.vuln_attempt_count, vulns.origin_id, vulns.origin_type FROM public.hosts,   public.workspaces, public.vulns, public.services WHERE hosts.id = vulns.host_id AND workspaces.id = hosts.workspace_id AND vulns.service_id = services.id AND hosts.id = {};".format(hostid)
        self._cur.execute(sql)
        return self._cur.fetchall()

    def getForAllHosts(self,table):
        self._cur.execute(
            "SELECT hosts.address,hosts.id,{}.* FROM public.hosts, public.{} WHERE hosts.id = {}.host_id".format(table, table, table))
        return self._cur.fetchall()

    def getServices(self,hostid):
        sql = "SELECT hosts.workspace_id as workspaceid, hosts.id as hostid, services.id as serviceid,  services.created_at, services.port, services.proto, services.state, services.name as servicename,   services.updated_at, services.info, workspaces.id as workspaceid, workspaces.name as workspace FROM public.hosts,   public.workspaces, public.services WHERE hosts.id = services.host_id AND workspaces.id = hosts.workspace_id AND  hosts.id = {};".format(hostid)
        self._cur.execute(sql)
        return self._cur.fetchall()

    def getSessions(self,wid):
        sql = "SELECT sessions.id as sessionid, sessions.host_id, sessions.stype, sessions.via_exploit, sessions.via_payload,   sessions.desc as sessiondescription, sessions.port, sessions.platform,sessions.opened_at, sessions.closed_at, sessions.close_reason, sessions.local_id, sessions.last_seen, sessions.module_run_id, hosts.workspace_id as workspaceid, hosts.address as ip FROM public.sessions, public.hosts, public.workspaces WHERE hosts.id = sessions.host_id AND workspaces.id = hosts.workspace_id AND hosts.workspace_id = {};".format(wid)
        self._cur.execute(sql)
        return self._cur.fetchall()

    def getSessionsForHost(self,hostid):
        sql = "SELECT hosts.address AS ip, sessions.host_id AS hostid, sessions.stype AS sessiontype, sessions.via_exploit, sessions.via_payload, sessions.desc AS sessiondescription, sessions.port,  sessions.platform, sessions.opened_at, sessions.closed_at, sessions.close_reason,   sessions.local_id AS localid, sessions.last_seen, sessions.module_run_id, sessions.id AS sessionid FROM   public.hosts, public.sessions WHERE hosts.id = sessions.host_id AND hosts.id = {};".format(hostid)
        self._cur.execute(sql)
        return self._cur.fetchall()

    def getSessionDetails(self,sessionid):
        self._cur.execute("SELECT sessions.id,session_events.* FROM public.sessions, public.session_events WHERE sessions.id = session_events.session_id and sessions.id = '{}'".format(sessionid))
        return self._cur.fetchall()

    def getCredentials(self,wid):
        self._cur.execute("SELECT workspaces.name as workspace, metasploit_credential_cores.id as coreid, metasploit_credential_cores.origin_id, metasploit_credential_cores.origin_type, metasploit_credential_cores.realm_id,  metasploit_credential_cores.workspace_id as workspaceid, metasploit_credential_cores.logins_count, metasploit_credential_privates.type as privtype, metasploit_credential_privates.data as privdata,   metasploit_credential_privates.jtr_format, metasploit_credential_publics.username, metasploit_credential_publics.type as pubtype FROM public.workspaces, public.metasploit_credential_cores, public.metasploit_credential_privates,  public.metasploit_credential_publics WHERE workspaces.id = metasploit_credential_cores.workspace_id AND   metasploit_credential_cores.private_id = metasploit_credential_privates.id AND metasploit_credential_cores.public_id = metasploit_credential_publics.id AND workspaces.id = {};".format(wid))
        return self._cur.fetchall()

    def getwebpagesforhost(self,hostid):
        sql = "SELECT web_sites.id AS websiteid, web_sites.service_id, web_sites.created_at, web_sites.updated_at,   web_sites.vhost, web_sites.comments, web_sites.options, web_pages.path, web_pages.query, web_pages.code,   web_pages.cookie, web_pages.ctype, web_pages.auth, web_pages.mtime, web_pages.location, web_pages.headers,   web_pages.body, web_pages.request, services.port, services.proto, services.host_id, services.name as protoname  FROM public.web_sites, public.services, public.web_pages WHERE web_sites.id = web_pages.web_site_id AND web_sites.service_id = services.id AND services.host_id = {};".format(hostid)
        self._cur.execute(sql)
        return self._cur.fetchall()

    def getwebformsforhost(self,hostid):
        sql = "SELECT web_sites.id AS websiteid, web_sites.service_id, web_sites.created_at, web_sites.updated_at,   web_sites.vhost, web_sites.comments, web_sites.options, web_forms.id AS formid, web_forms.web_site_id,   web_forms.created_at, web_forms.updated_at, web_forms.path, web_forms.method, web_forms.query, web_forms.params,   services.port, services.proto, services.host_id, services.name as protoname FROM public.web_sites, public.services, public.web_forms WHERE   web_sites.service_id = services.id AND  web_sites.id = web_forms.web_site_id AND services.host_id = {};".format(hostid)
        self._cur.execute(sql)
        return self._cur.fetchall()

    def queryModules(self,plat, searchstring):
        sql = "SELECT module_details.id AS detailid, module_details.mtime, module_details.file, module_details.mtype,  module_details.refname AS detailrefname, module_details.fullname, module_details.name AS detailname,   module_details.rank, module_details.description, module_details.disclosure_date, module_details.default_target,   module_details.default_action, module_details.stance, module_details.ready FROM public.module_details,   public.module_platforms WHERE module_details.id = module_platforms.detail_id AND module_details.mtype IN ('exploit','auxiliary') AND module_platforms.name = '{}' AND module_details.fullname LIKE '{}';".format(plat,searchstring)
        self._cur.execute(sql)
        return self._cur.fetchall()

    def getWorkspaces(self):
        sql = "SELECT workspaces.id, workspaces.name FROM public.workspaces;"
        self._cur.execute(sql)
        return self._cur.fetchall()
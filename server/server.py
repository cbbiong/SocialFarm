from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from templatemapper import templatemapper
import httplib2, urllib, json

src_server = ('127.0.0.1', 8080)
dst_server = ('127.0.0.1', 5984)

patterns = {
'businesses'             : templatemapper('/businesses{}',                   '/socialfarm/_design/business/_list/basic_html/all{}'),
'business'               : templatemapper('/business/{bid}' ,                '/socialfarm/_design/business/_show/basic_html/{bid}'), 
'business.members'       : templatemapper('/business/{bid}/members' ,        '/{bid}/_design/info/_list/members_basic_html/all_members'), 
'business.member'        : templatemapper('/business/{bid}/member/{mid}' ,   '/{bid}/_design/info/_show/member_basic_html/{mid}'), 
'business.actions'       : templatemapper('/business/{bid}/actions' ,        '/{bid}/_design/info/_list/actions_basic_html/all_actions'), 
'business.action'        : templatemapper('/business/{bid}/action/{aid}' ,   '/{bid}/_design/info/_show/action_basic_html/{aid}'), 
'business.jobs'          : templatemapper('/business/{bid}/jobs' ,           '/{bid}/_design/info/_list/jobs_basic_html/all_jobs'), 
'business.job'           : templatemapper('/business/{bid}/job/{jid}' ,      '/{bid}/_design/info/_show/job_basic_html/{jid}'), 
'business.tasks'         : templatemapper('/business/{bid}/tasks' ,          '/{bid}/_design/info/_list/tasks_basic_html/all_tasks'), 
'business.task'          : templatemapper('/business/{bid}/task/{tid}' ,     '/{bid}/_design/info/_show/task_basic_html/{tid}'), 

'api.businesses'         : templatemapper('/api/businesses{}',               '/socialfarm/_design/business/_view/all{}'),
'api.business'           : templatemapper('/api/business/{bid}' ,            '/socialfarm/{bid}'),
'api.business.members'   : templatemapper('/api/business/{bid}/members' ,    '/{bid}/_design/info/_view/all_members'), 
'api.business.actions'   : templatemapper('/api/business/{bid}/actions' ,    '/{bid}/_design/info/_view/all_actions'), 
'api.business.jobs'      : templatemapper('/api/business/{bid}/jobs' ,       '/{bid}/_design/info/_view/all_jobs'), 
'api.business.tasks'     : templatemapper('/api/business/{bid}/tasks' ,      '/{bid}/_design/info/_view/all_tasks'), 
#'api.business.id'       : templatemapper('/api/business/{bid}/{id}' ,       '/{bid}/{id}'), 
}

reserved = [ 'api', 'businesses', 'business', 'members', 'member', 'actions', 'action', 'jobs', 'job', 'tasks', 'task' ]

#function strips a path to a dotted string of the reserved words it contained
def path_to_key(path):
    parts = filter(lambda x: x in reserved, path.split('/'))
    key = reduce(lambda x, y: '%s.%s' % (x, y), parts)
    if key == 'api.business' and len(path.split('/')) == 4:
        key == 'api.business.id'
    return key

class Adapter(BaseHTTPRequestHandler) :  
     
    def do_GET(self):
        url = 'http://%s:%s' % dst_server + patterns[path_to_key(self.path)].replace(self.path) 
        response, content = httplib2.Http().request(url, "GET")
        self.write_response(response, content)

    def do_PUT(self):
        url = 'http://%s:%s' % dst_server + patterns[path_to_key(self.path)].replace(self.path) 
        headers = { "content-type": "application/json" }

        #this is where it is getting stuck
        # maybe relevant? http://www.gossamer-threads.com/lists/python/python/847985
        print "right here..."
        data = self.rfile.read()
        print data
       
        response, content = httplib2.Http().request(url, "PUT", body = data, headers = headers)
        print content
        self.write_response(response, content)
      
    def write_response(self, response, content):
   
        self.send_response(int(response['status']))
        self.send_header('content-type', response['content-type'])
        self.end_headers()
        self.wfile.write(content)
        
if __name__ == '__main__':
    try:
        server = HTTPServer(src_server, Adapter)
        print 'started httpserver at %s:%s' % src_server
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

   



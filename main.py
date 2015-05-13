import base64
import cherrypy
import json
import csv

def script_path(include_name=False):
    # returns the full path of the script containing this snippet
    # by: Cody Kochmann
    from os import path
    full_path = path.realpath(__file__)
    if include_name:
        return(full_path)
    else:
        full_path = "/".join( full_path.split("/")[0:-1] ) + "/"
        return(full_path)

def write_to_csv(input_array):
  with open( script_path() + '/note_database.csv', 'a') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter='|')
      # Uncomment this if you need verbose logging to debug anything
      # print "appending %s to clipboard_watcher.csv" % (input_array)
      spamwriter.writerow(input_array)

def read_file(path):
  with open(path,"r") as f:
    output = f.read()
    return(output)

class Root(object):
    @cherrypy.expose
    def update(self):
        cl = cherrypy.request.headers['Content-Length']
        b64_body = cherrypy.request.body.read(int(cl))
        message=json.loads(base64.b64decode(b64_body))
        message["content"]=base64.b64encode(message["content"])
        write_to_csv([message["id"],message["content"]])
        # do_something_with(body)
        return "Content Recieved"

    @cherrypy.expose
    def index(self):
        return(read_file("index.html"))


cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8080,
                       })
cherrypy.quickstart(Root())

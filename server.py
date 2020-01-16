import http.server
import socketserver
import sqlite3
import contextlib
from urllib.parse import urlparse

PORT = 8002

db = sqlite3.connect('db.db')

class DBLoggingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        path = urlparse(self.path).path
        print(path)
        if 'api' not in path:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)


        db.execute("CREATE TABLE IF NOT EXISTS answers(user INTEGER, obj1 TEXT, obj2 TEXT, question TEXT, answer TEXT)")

        if 'get_user' in path:
            cursor = db.cursor()
            cursor.execute('SELECT COUNT(DISTINCT user) from answers')
            row = cursor.fetchone()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str.encode(str(row[0]+1)))
            cursor.close()
            return


        query = urlparse(self.path).query
        components = {}
        for arg in query.split('&'):
            k, v = arg.split('=')
            components[k] = v
        if set(components.keys()) != set(['user', 'obj1', 'obj2','question','answer']):
            print('Wrong request')
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str.encode("Wrong request"))
            return

        db.execute("INSERT INTO answers (user, obj1, obj2, question, answer) VALUES (?, ?, ?, ?, ?)",
                        (components['user'], components['obj1'], components['obj2'], components['question'], components['answer']))

        db.commit()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(str.encode('OK'))
        return

Handler = DBLoggingHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
with contextlib.closing(db):
    httpd.serve_forever()

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from markupsafe import escape

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path).path
        path_components = parsed_path.split('/')

        text = b""
        if len(path_components) <= 1:
            text = 'Index Page'
        elif path_components[1] == 'hello':
            text = 'Hello World'
        elif len(path_components) >= 3:
            match path_components[1]:
                case 'user':
                    text = f'User: {escape(path_components[2])}'
                case 'post':
                    text = f'Post {escape(path_components[2])}'
                case 'path':
                    text = f'Subpath {"/".join([escape(component) for component in path_components[2:]])}'
                case _:
                    text = 'No page found'
        else:
            text = 'No page found'

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(f'<html><body><h1>{text}</h1></body></html>'.encode('utf-8'))
    
def run(server_class=HTTPServer, handler_class=MyHandler, port = 8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Server running...")

    httpd.serve_forever()

if __name__ == "__main__":
    run()
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from markupsafe import escape

def write_to_wfile(handler: BaseHTTPRequestHandler, text: str) -> None:
    '''
    Formats text to be displayed on webpage. Should be called as response to client GET request.
    
    Keyword arguments:
    handler -- handler that is processing GET request
    text -- text to be displayed on webpage
    '''
    handler.wfile.write(f'<html><body><h1>{text}</h1></body></html>'.encode('utf-8'))

def index(handler: BaseHTTPRequestHandler) -> None:
    '''
    Displays appropriate message on webpage when no path is specified.
    
    Keyword arguments:
    handler -- handler that is processing GET request
    '''
    write_to_wfile(handler, 'Index Page') 

def hello(handler: BaseHTTPRequestHandler) -> None:
    '''
    Displays 'Hello World' on webpage when path is /hello.

    Keyword arguments:
    handler -- handler that is processing GET request
    '''
    write_to_wfile(handler, 'Hello World')

def show_user_profile(handler: BaseHTTPRequestHandler, username: str) -> None:
    '''
    Displays username when path is in the form /user/<username>.
    
    Keyword arguments:
    handler -- handler that is processing GET request
    username -- username to be displayed
    '''
    write_to_wfile(handler, f'User: {escape(username)}')

def show_post(handler: BaseHTTPRequestHandler, post_id: int) -> None:
    '''
    Displays post_id when path is in the form of /post/<post_id>

    Keyword arguments:
    handler -- handler that is processing GET request
    post_id -- post id number to be displayed
    '''
    write_to_wfile(handler, f'Post: {escape(post_id)}')

def show_subpath(handler: BaseHTTPRequestHandler, subpath: str) -> None:
    '''
    Displays subpath when path is in the form of /path/<subpath>

    Keyword arguments:
    handler -- handler that is processing GET request
    subpath -- rest of the path to be displayed
    '''
    write_to_wfile(handler, subpath)

def not_valid_path(handler: BaseHTTPRequestHandler) -> None:
    '''
    Displays appropriate message on webpage for all undefined cases.
    
    Keyword arguments:
    handler -- handler that is processing GET request
    '''
    write_to_wfile(handler, 'No page found')

class MyHandler(BaseHTTPRequestHandler):
    '''
    Custom HTTP request handler.

    ...

    Methods
    -------
    do_GET():
        Processes GET request and displays appropriate message on webpage.
    '''

    def do_GET(self):
        '''
        Processes GET request and displays appropriate message on webpage.

        If no path is specified, 'Index Page' is displayed.
        If path is /hello, 'Hello World' is displayed.
        If path is in the form of /user/<username>, 'User: <username>' is displayed.
        If path is in the form of /post/<post_id>, 'Post <post_id>' is displayed.
        If path is in the form of /path/<subpath>, 'Subpath <subpath>' is displayed.
        If none of the above are true then 'No page found' is displayed.
        '''
        parsed_path = urlparse(self.path).path
        path_components = parsed_path.split('/')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if len(path_components) <= 1:
            index(self)
        elif path_components[1] == 'hello':
            hello(self)
        elif len(path_components) >= 3:
            match path_components[1]:
                case 'user':
                   show_user_profile(self, path_components[2])
                case 'post':
                    show_post(self, path_components[2])
                case 'path':
                    show_subpath(self, "/".join([escape(component) for component in path_components[2:]]))
                case _:
                    not_valid_path(self)
        else:
            not_valid_path(self)
    
def run(server_class=HTTPServer, handler_class=MyHandler, port = 8000):
    '''Runs the HTTP Server using the custom handler.'''
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Server running...")

    httpd.serve_forever()

if __name__ == "__main__":
    run()
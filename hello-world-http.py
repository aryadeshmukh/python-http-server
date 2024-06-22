from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from markupsafe import escape

class ResponseInfo:
    '''
    Response Information for GET requests.

    ...

    Attributes
    ----------
    code : int
        http response code
    content_type : str
        content type
    body : str
        message to be displayed
    '''
    def __init__(self, code: int, content_type: str, body: str) -> None:
        self.code = code
        self.content_type = content_type
        self.body = body

def handle_root() -> ResponseInfo:
    '''Specifies response information for root url.'''
    return ResponseInfo(200, 'text/plain', 'Index Page')

def handle_hello() -> ResponseInfo:
    '''Specifies response information for url path /hello.'''
    return ResponseInfo(200, 'text/html', '<html><body><h1>Hello World</h1></body></html>')

def handle_user(username: str) -> ResponseInfo:
    '''
    Specifies repsonse information for url path /user/<username>.

    Keyword arguments:
    username -- username of user to be handled
    '''
    return ResponseInfo(200, 'text/plain', f'User: {escape(username)}')

def handle_path(subpath: str) -> ResponseInfo:
    '''
    Specifies response information for url path /path/<subpath>.

    Keyword arguments:
    subpath -- subpath of the url path
    '''
    return ResponseInfo(200, 'text/plain', f'Subpath {escape(subpath)}')

def handle_404() -> ResponseInfo:
    '''Specifies response information for page not found.'''
    return ResponseInfo(404, 'text/plain', 'Page not found')

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
        If path is in the form of /path/<subpath>, 'Subpath <subpath>' is displayed.
        If none of the above are true then 'No page found' is displayed.
        '''
        routes = {
            "" : handle_root,
            "hello" : handle_hello,
            "user" : handle_user,
            "path" : handle_path
        }

        try:
            parsed_path = urlparse(self.path).path.strip('/')
            path_components = parsed_path.split('/')

            if len(path_components) == 1:
                response_func = routes[path_components[0]]
                response = response_func()
            elif len(path_components) == 2:
                response_func = routes[path_components[0]]
                response = response_func(path_components[1])
            else:
                response_func = routes[path_components[0]]
                response = response_func("/".join(path_components[1:]))  
        except Exception:
            response = handle_404()

        self.send_response(response.code)
        self.send_header('Content-type', response.content_type)
        self.end_headers()
        self.wfile.write(bytes(response.body, 'utf-8'))

def run(server_class=HTTPServer, handler_class=MyHandler, port = 8000):
    '''Runs the HTTP Server using the custom handler.'''
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Server running...")

    httpd.serve_forever()

if __name__ == "__main__":
    run()
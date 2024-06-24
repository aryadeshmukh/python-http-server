from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from markupsafe import escape
from typing import Callable

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

def handle_400() -> ResponseInfo:
    '''Specifies response information for bad request.'''
    return ResponseInfo(400, 'text/plain', 'Bad Request')

def handle_403() -> ResponseInfo:
    '''Specifies response information for access denied.'''
    return ResponseInfo(403, 'text/plain', 'Access Denied')

def raise_400() -> None:
    '''Raises a 400 error.'''
    raise BadRequest()

def raise_403() -> None:
    '''Raises a 403 error.'''
    raise AccessDenied()

def create_response(response_func: Callable, *arg) -> ResponseInfo:
    '''
    Returns the response of a one argument response_func
    
    Keyword arguments:
    response_func -- function whose return values should be returned
    arg -- arguments to response_func
    '''
    return response_func(*arg)

class BadRequest(Exception):
    '''Error type for error code 400.'''
    pass

class AccessDenied(Exception):
    '''Error type for error code 403'''
    pass

# Mapping of url path to function with specification of variable rules
routes = {
    '' : (handle_root, None),
    'hello' : (handle_hello, None),
    'user' : (handle_user, 'str'),
    'path' : (handle_path, 'path'),
    'bad-request' : (raise_400, None),
    'access-denied' : (raise_403, None)
}

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

        Handles variable rules for str, int, path, and no variable type GET requests.
        '''
        try:
            parsed_path = urlparse(self.path).path.strip('/')
            path_components = parsed_path.split('/')

            curr_path_depth = 0
            curr_path = None

            while curr_path not in routes and curr_path_depth < len(path_components):
                curr_path_depth += 1
                curr_path = '/'.join(path_components[:curr_path_depth])
            
            response = None

            match routes[curr_path][1]:
                case 'str':
                    print(curr_path_depth)
                    if curr_path_depth == len(path_components) - 1:
                        response = create_response(routes[curr_path][0], path_components[curr_path_depth])
                    else:
                        response = handle_404()
                case 'int':
                    if curr_path_depth == len(path_components):
                        response = create_response(routes[curr_path][0], int(path_components[curr_path_depth]))
                    else:
                        response = handle_404()
                case 'path':
                    response = create_response(routes[curr_path][0], '/'.join(path_components[curr_path_depth:]))
                case None:
                    if curr_path_depth == len(path_components):
                        response = create_response(routes[curr_path][0])
                    else:
                        response = handle_404()

        except BadRequest:
            response = handle_400()
        except AccessDenied:
            response = handle_403()
        except:
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
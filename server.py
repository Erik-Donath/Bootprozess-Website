from wsgiref.simple_server import make_server
from app import app


def application(environ, start_response):
    response = app(environ, start_response)
    return response


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 80

    httpd = make_server(host, port, application)
    print(f"Server on {host}:{port}")
    httpd.serve_forever()

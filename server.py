from wsgiref.simple_server import make_server
from app import app


def application(environ, start_response):
    response = app(environ, start_response)
    return response


if __name__ == '__main__':

    # Current Address at port 80 (Standard Http Port)
    host = '0.0.0.0'
    port = 80

    print("Starting Server...")
    httpd = make_server(host, port, application)
    address = httpd.server_address

    try:
        print(f"Server on {address[0]}:{address[1]}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        httpd.server_close()
        print("Server stopped")
    print("Done")

from wsgiref.simple_server import make_server
from app import app


# Diese Funktion wird als WSGI-Anwendung verwendet
def application(environ, start_response):
    # Rufe die Flask-Anwendung auf
    response = app(environ, start_response)
    return response


if __name__ == '__main__':
    host = '10.254.1.223'  # Host, auf dem der Server lauschen soll (alle verfügbaren Netzwerkschnittstellen)
    port = 80      # Port, auf dem der Server lauschen soll
    httpd = make_server(host, port, application)
    print(f"Server on {host}:{port}")
    httpd.serve_forever()
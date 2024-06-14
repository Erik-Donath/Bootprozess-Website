from app import app

# This will not run when used with "python3 -m flask run"
# Otherwise it will always be the developer server. DO NOT USE THIS IN PRODUCTION!
# Use server.py instead
if __name__ == '__main__':
    app.run(debug=True, threaded=True)

import urlparse, os

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = 'BPQ4kMHJPaC6bCzC'
    MONGOLAB_URI = os.environ.get('MONGOLAB_URI')
    if MONGOLAB_URI:
        url = urlparse.urlparse(MONGOLAB_URI)
        MONGODB_USER = url.username
        MONGODB_PASSWORD = url.password
        MONGODB_HOST = url.hostname
        MONGODB_PORT = url.port
        MONGODB_DB = url.path[1:]
    else:
        MONGODB_HOST = 'localhost'
        MONGODB_PORT = 27017
        MONGODB_DB = 'mapme'

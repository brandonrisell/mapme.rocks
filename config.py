import urlparse, os

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = 'BPQ4kMHJPaC6bCzC'
    MONGOLAB_URI = os.environ.get('MONGOLAB_URI')
    if MONGOLAB_URI:
        url = urlparse.urlparse(MONGOLAB_URI)
        MONGOLAB_DB = url.path[1:]
    else:  #if no env settings, use localhost (for dev)
        MONGOLAB_URI = 'mongodb://localhost:27017/mapme'
        MONGOLAB_DB = 'mapme'
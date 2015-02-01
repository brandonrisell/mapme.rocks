import urlparse, os

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = 'BPQ4kMHJPaC6bCzC'
    MONGOLAB_URI = os.environ.get('MONGOLAB_URI')
    if not MONGOLAB_URI:
        MONGOLAB_URI = 'mongodb://localhost:27017'
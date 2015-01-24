import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SECRET_KEY = 'BPQ4kMHJPaC6bCzC'
	# SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/'
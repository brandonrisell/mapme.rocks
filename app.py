#!/usr/bin/env python
from flask import Flask, request, jsonify, render_template, flash, g
import json, socket, geoip2.database, geoip2.errors, ipaddr, os
from flask_bootstrap import Bootstrap
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
import config

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.from_object(config.Config)

# GeoIP DB Reader
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

RDB_HOST =  os.environ.get('RDB_HOST') or '127.0.0.2'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
RDB_NAME = 'mapme'

# db setup; only run once
def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(RDB_NAME).run(connection)
        r.db(RDB_NAME).table_create('queries').run(connection)
        print 'Database setup completed'
    except RqlRuntimeError:
        print 'Database already exists.'
    finally:
        connection.close()
dbSetup()

@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_NAME)
    except RqlDriverError:
        abort(503, "No database connection could be established.")

@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass

def get_traits(ip_addr):

	try:
		ipaddr.IPAddress(ip_addr)
		domain_name = socket.gethostbyaddr(ip_addr)[0]
	except (ValueError, ipaddr.AddressValueError) as e:
		domain_name = ip_addr
		ip_addr = socket.gethostbyname(domain_name)

	traits = reader.city(ip_addr)

	details = {
			'IP Address': ip_addr,
			'City': traits.city.name,
			'Subdivision' : traits.subdivisions.most_specific.name,
			'Country': traits.country.name,
			'Country Code' : traits.country.iso_code,
			'Latitude' : traits.location.latitude,
			'Longitude' : traits.location.longitude,
			'Domain Name' : domain_name
			}

	# store query for history
	inserted = r.table('queries').insert(details).run(g.rdb_conn)

	return details

@app.route('/')
def home():

	return render_template('home.html')

@app.route('/dest/<destination>')
def home_dest(destination):

	try:
		ip_traits = get_traits(destination)
	except ValueError as e:
		return jsonify({'Error': e.message}), 400

	try:
		return render_template('home.html', destination=get_traits(destination))		
	except ValueError as e:
		flash(e.message, 'danger')
		return render_template('home.html')		

@app.route('/feed/')
def feed():

	try:
		limit = int(request.args.get('limit')) or 20
	except TypeError:
		limit = 20
		
	points = [x for x in r.table('queries').limit(limit).run(g.rdb_conn)]

	return render_template('tail.html', points=points, limit=limit)

@app.route('/findme')
def findme():

	return render_template('findme.html')

@app.route('/features')
def features():

	return render_template('features.html')

@app.route('/geoip/<ip_addr>', methods=['GET', 'POST'])
def geoip_lookup(ip_addr):
	
	try:
		details = get_traits(ip_addr)
	except Exception as e:
		return jsonify({"Error": "'" + ip_addr + "' is not a valid domain name or IP address."}), 400

	return jsonify(details), 200


if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True, port=5000)
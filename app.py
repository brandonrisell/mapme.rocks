#!/usr/bin/env python
from flask import Flask, request, jsonify, render_template, flash
import json, socket, geoip2.database, geoip2.errors, ipaddr
from flask_bootstrap import Bootstrap
import config

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.from_object(config.Config)

# GeoIP DB Reader
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

def get_traits(ip_addr):

	return reader.city(ip_addr)

@app.route('/')
def home():

	return render_template('home.html')

@app.route('/findme')
def findme():

	return render_template('findme.html')


@app.route('/geoip/<ip_addr>', methods=['GET', 'POST'])
def geoip_lookup(ip_addr):
	
	# test if valid IP(4/6) address
	try:
		ipaddr.IPAddress(ip_addr)
	except (ValueError, ipaddr.AddressValueError) as e:
		try:
			ip_addr = socket.gethostbyname(ip_addr)
		except socket.gaierror as er:
			return jsonify({'Error': er.message}), 400
		# else:
		# 	return jsonify({'Error': e.message}), 400

	try:
		ip_traits = get_traits(ip_addr)
	except ValueError as e:
		return jsonify({'Error': e.message}), 400

	country = ip_traits.country.name
	city = ip_traits.city.name
	
	return jsonify({
		'IP Address': ip_addr,
		'City': ip_traits.city.name,
		'Subdivision' : ip_traits.subdivisions.most_specific.name,
		'Country': ip_traits.country.name,
		'Latitude' : ip_traits.location.latitude,
		'Longitude' : ip_traits.location.longitude,
		}), 200


if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True, port=5000)
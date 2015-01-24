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


@app.route('/findme')
def findme():

	return render_template('findme.html')


@app.route('/geoip/<ip_addr>', methods=['GET', 'POST'])
def geoip_lookup(ip_addr):
	
	try:
		details = get_traits(ip_addr)
	except ValueError as e:
		return jsonify({'Error': e.message}), 400

	return jsonify(details), 200


if __name__ == '__main__': 
	app.run(host='0.0.0.0', debug=True, port=5000)
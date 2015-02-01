#!/usr/bin/env python
from flask import Flask, request, jsonify, render_template, flash, g, redirect, url_for
import json, socket, geoip2.database, geoip2.errors, ipaddr, os
from flask_bootstrap import Bootstrap
from mongokit import Connection, Document
import config

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.from_object(config.Config)

# GeoIP DB Reader
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

#DB Query Model
class Domain_Lookup(Document):
    structure = {
        'IP Address': str,
        'City': str,
        'Subdivision': str,
        'Country': str,
        'Country Code': str,
        'Latitude': str,
        'Longitude': str,
        'Domain Name': str,
    }
    use_dot_notation = True
    def __repr__(self):
        return '<Domain Lookup %r>' % (self['Domain Name'])

# register the User document with our current connection
connection = Connection(app.config['MONGOLAB_URI'])
connection.register([Domain_Lookup])
collection = connection[app.config['MONGOLAB_DB']].lookups

def get_traits(ip_addr):

    try:
        ipaddr.IPAddress(ip_addr)
        domain_name = socket.gethostbyaddr(ip_addr)[0]
    except (ValueError, ipaddr.AddressValueError) as e:
        domain_name = ip_addr
        ip_addr = socket.gethostbyname(domain_name)

    traits = reader.city(ip_addr)

    lookup = collection.Domain_Lookup()
    lookup['IP Address'] = str(ip_addr)
    lookup['City'] = str(traits.city.name)
    lookup['Subdivision'] = str(traits.subdivisions.most_specific.name)
    lookup['Country'] = str(traits.country.name)
    lookup['Country Code'] = str(traits.country.iso_code)
    lookup['Latitude'] = str(traits.location.latitude)
    lookup['Longitude'] = str(traits.location.longitude)
    lookup['Domain Name'] = str(domain_name)
            
    # store query for history
    lookup.save()

    details = {
        'IP Address': lookup['IP Address'],
        'City': lookup['City'],
        'Subdivision': lookup['Subdivision'],
        'Country': lookup['Country'],
        'Country Code': lookup['Country Code'],
        'Latitude': lookup['Latitude'],
        'Longitude': lookup['Longitude'],
        'Domain Name': lookup['Domain Name'],
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
        return render_template('home.html', destination=get_traits(destination), orig_query=destination)        
    except ValueError as e:
        flash(e.message, 'danger')
        return render_template('home.html')     

@app.route('/feed/')
def feed():

    try:
        limit = int(request.args.get('limit')) or 20
    except TypeError:
        limit = 20
        
    points = [x for x in collection.Domain_Lookup.find()] or [None]

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

@app.errorhandler(404)
def page_not_found(e):
    flash('The page you requested does not exist', 'warning')
    return redirect(url_for('home'))

if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True, port=5000)
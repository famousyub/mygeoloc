
from flask import Flask, render_template, request,jsonify, make_response

import requests
import ipaddress
import pygeoip, json
app = Flask(__name__)
 
app.config['DEBUG'] = True
 
 


def get_country(ip_address):
    try:
        response = requests.get("http://ip-api.com/json/{}".format(ip_address))
        js = response.json()
        country = js['countryCode']
        return country
    except Exception as e:
        return "Unknown"


geo = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

@app.route('/')
def index():
    client_ip = request.remote_addr 
    client_ip = "192.168.1.47"
    geo_data = geo.record_by_addr(client_ip)
    return json.dumps(geo_data, indent=2) + '\n'


@app.route("/home")
def home():
    ip_address = request.remote_addr
    country = get_country(ip_address)
    # number of countries where the largest number of speakers are French
    # data from http://download.geonames.org/export/dump/countryInfo.txt
    if country in ('BL', 'MF', 'TF', 'BF', 'BI', 'BJ', 'CD', 'CF', 'CG', 'CI', 'DJ', 'FR', 'GA', 'GF', 'GN', 'GP', 'MC', 'MG', 'ML', 'MQ', 'NC'):
        return "Bonjour"
    return "Hello"

@app.route('/ip')
def index2():
    return 'Flask is Awesome!'
 
 
@app.route('/geolocation', methods=['GET'])
def get_geolocation():
        return render_template('index.html')


@app.route('/fetch-gelocation', methods=['POST'])
def post_geolocation():
    try:
        ipaddress.ip_address(request.form['ip_address'])
        req = requests.get('https://ipgeolocation.abstractapi.com/v1/?ip_address=' + request.form['ip_address'] + '&api_key=<YOUR_API_KEY>')
        return make_response(jsonify(req.json()))
    except ValueError:
        return make_response(jsonify({'error': 'Invalid IP Address'}))
    except Exception as e:
        return make_response(jsonify({'error': str(e)}))

        
 
if __name__ == "__main__":
    app.run(debug=True)
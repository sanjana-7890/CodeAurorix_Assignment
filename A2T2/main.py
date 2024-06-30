from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import requests
import socket
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins

# Store the URL for the current session
current_session_url = None

@app.route('/')
def analyze_website():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        # Extract domain from the URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        if not domain:
            raise ValueError("Invalid URL")

        # Fetch and process domain information
        domain_info = get_domain_info(domain)
        
        # Fetch and process subdomain information
        subdomains = get_subdomains(domain)
        
        # Fetch and process asset domains
        asset_domains = get_asset_domains(url)
        
        # Arrange the output
        response = {
            "info": domain_info,
            "subdomains": subdomains,
            "asset_domains": asset_domains
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_domain_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        ip_info = requests.get(f'https://ipinfo.io/{ip}/json').json()
        
        # Fetch ASN info using ip-api.com
        asn_info = requests.get(f'http://ip-api.com/json/{ip}').json()
        
        domain_info = {
            "ip": ip_info.get("ip"),
            "isp": ip_info.get("org"),
            "organization": ip_info.get("org"),
            "asn": asn_info.get("as") if 'as' in asn_info else "N/A",
            "location": ip_info.get("country")
        }
        return domain_info

    except socket.gaierror:
        raise ValueError("Failed to resolve domain")

def get_subdomains(domain):
    api_key = 'vysMaTptAMadrB8bIfJiwRMraqmFRKSN'  # SecurityTrails API key
    url = f'https://api.securitytrails.com/v1/domain/{domain}/subdomains'
    headers = {'APIKEY': api_key}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        subdomains = data.get('subdomains', [])
        return [f"{sub}.{domain}" for sub in subdomains]
    else:
        print(f"Error fetching subdomains: {response.status_code} - {response.text}")
        return []

def get_asset_domains(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract domains
    asset_domains = {
        "javascripts": [],
        "stylesheets": [],
        "images": [],
        "iframes": [],
        "anchors": []
    }
    
    # Populate asset_domains by parsing soup
    for script in soup.find_all('script', src=True):
        asset_domains['javascripts'].append(script['src'])
    
    for link in soup.find_all('link', rel="stylesheet"):
        asset_domains['stylesheets'].append(link['href'])
    
    for img in soup.find_all('img', src=True):
        asset_domains['images'].append(img['src'])
    
    for iframe in soup.find_all('iframe', src=True):
        asset_domains['iframes'].append(iframe['src'])
    
    for anchor in soup.find_all('a', href=True):
        asset_domains['anchors'].append(anchor['href'])
    
    return asset_domains

@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected to WebSocket'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message):
    global current_session_url

    try:
        message = json.loads(message)
    except json.JSONDecodeError:
        emit('message', {'data': 'Invalid message format'})
        return

    if 'url' in message:
        current_session_url = message['url']
        emit('message', {'data': f'Session created for {current_session_url}'})
    elif 'operation' in message:
        if not current_session_url:
            emit('message', {'data': 'No session URL provided'})
            return
        
        domain = urlparse(current_session_url).netloc

        if message['operation'] == 'get_info':
            domain_info = get_domain_info(domain)
            emit('message', {'data': domain_info})
        elif message['operation'] == 'get_subdomains':
            subdomains = get_subdomains(domain)
            emit('message', {'data': subdomains})
        elif message['operation'] == 'get_asset_domains':
            asset_domains = get_asset_domains(current_session_url)
            emit('message', {'data': asset_domains})
        else:
            emit('message', {'data': 'Unknown operation'})

if __name__ == '__main__':
    socketio.run(app, debug=True)

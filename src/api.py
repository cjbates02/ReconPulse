from flask import Flask
from views import NetworkAPI

api = Flask(__name__)
api.add_url_rule('/network', view_func=NetworkAPI.as_view('network_api', '10.0.97.0/24'))

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0')

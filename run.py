import os
import certifi

os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

from app import app

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify
import requests
from json import JSONDecodeError


app = Flask(__name__)
catalog_data = {}
# Mock data for front-end
catalog_server_url = "http://localhost:5002"  # Replace with actual URL
order_server_url = "http://localhost:5003"  # Replace with actual URL

@app.route('/search/<topic>', methods=['GET'])
def search(topic):
    
    response = requests.get(f"{catalog_server_url}/query/{topic}")
    
    #return response.json()
    # Check if the response status code is OK
    if response.status_code == 200:
            print("Ok")
            catalog_data = response.json()
            
            return jsonify(catalog_data)

    else:
        return jsonify({'error': f'Error from catalog server: {response.status_code}'}), 500



@app.route('/info/<int:item_number>', methods=['GET'])
def info(item_number):
    response = requests.get(f"{catalog_server_url}/query/{item_number}")
    item_data = response.json()
    print("Yes this is info")

    return jsonify(item_data)

@app.route('/purchase/<int:item_number>', methods=['POST'])
def purchase(item_number):
   
    # Check if item is in stock by querying the catalog server
    purchase_response = requests.post(f"{order_server_url}/purchase/{item_number}")
    
    if purchase_response.status_code == 200:
        return jsonify(purchase_response.json())
    else:
        return jsonify(purchase_response.json()),404
    
if __name__ == '__main__':
    app.run(port=5000)
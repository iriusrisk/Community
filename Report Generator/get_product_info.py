import requests
import json

# Read configuration values from file

with open("credentials.json", "r") as f:
    cred = json.load(f)
    api_token = cred["api_token"]

with open("tmp_config.json", "r") as f:
    config = json.load(f)
    base_url = config["base_url"]
    product_id = config["product_id"]

# Define headers with authorization token
headers = {"api-token": api_token}

# Make GET request to /api/v1/products/:product-id endpoint, that has full info about the product
product_url = f"{base_url}/api/v1/products/{product_id}"
response = requests.get(product_url, headers=headers)

# Save received JSON array to local file "product_info.json"
with open("product_info.json", "w") as f:
    json.dump(response.json(), f)
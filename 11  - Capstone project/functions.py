import os
import logging
import requests
from config import EXTERNAL_API_URL, LOG_FILE

# ✅ Configure Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_external_data(params):
    """Fetches data from an external API securely."""
    try:
        response = requests.get(EXTERNAL_API_URL, params=params, timeout=10)
        response.raise_for_status()  # ✅ Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"External API request failed: {e}")
        return {"error": "Failed to fetch data from external API."}

# ✅ Example Usage
if __name__ == "__main__":
    sample_params = {"query": "top 10 countries by GDP"}
    print(fetch_external_data(sample_params))

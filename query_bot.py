import requests
from urllib.parse import quote

# Define the URL of the FastAPI server
FASTAPI_SERVER_URL = "http://localhost:8000/"

def scrape_data_from_url(url):
    """Send a request to the FastAPI server to scrape data from the given URL."""
    encoded_url = quote(url, safe='')
    try:
        response = requests.get(f"{FASTAPI_SERVER_URL}?url={encoded_url}")
        response.raise_for_status()
        data = response.json()
        
        if "scraped_text" in data:
            result = f"Visible text successfully scraped!\n\n{data['scraped_text']}"
            # Provide download links for the CSV and JSON files
            if "csv_file" in data:
                csv_file_url = f"{FASTAPI_SERVER_URL}static/{data['csv_file']}"
                result += f"\n\nDownload CSV file: {csv_file_url}"
            if "json_file" in data:
                json_file_url = f"{FASTAPI_SERVER_URL}static/{data['json_file']}"
                result += f"\nDownload JSON file: {json_file_url}"
        elif "error" in data:
            result = f"Error: {data['error']}"
        else:
            result = "Failed to scrape visible text from the URL."
        
        return result
    
    except requests.RequestException as e:
        return f"Failed to connect to the FastAPI server. Error: {e}"

def handle_user_request(user_query):
    """Handles user queries and provides responses."""
    if 'income tax' in user_query.lower():
        url = 'https://www.incometax.gov.in/iec/foportal/'  # Replace with the actual URL
        result = scrape_data_from_url(url)
        return result
    # Add other query handling logic here
    return "I'm sorry, I didn't understand your query."

def main():
    while True:
        user_query = input("Ask me something: ")
        if user_query.lower() == 'exit':
            print("Exiting the bot.")
            break
        response = handle_user_request(user_query)
        print(response)

if __name__ == '__main__':
    main()

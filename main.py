from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from bs4 import BeautifulSoup
import requests
import os
import csv
import json
import re
from urllib.parse import urlparse

app = FastAPI()

# Mount the static directory to serve files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create the static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

def sanitize_filename(filename: str) -> str:
    """Sanitize file names by replacing spaces with underscores."""
    return re.sub(r'\s+', '_', filename.strip())

def get_unique_filename(base_name: str, ext: str, directory: str) -> str:
    """Generate a unique file name by appending a number."""
    count = 1
    while os.path.isfile(os.path.join(directory, f"{base_name}_{count}{ext}")):
        count += 1
    return f"{base_name}_{count}{ext}"

@app.get("/")
def scrape(url: str):
    try:
        # Make a request to the given URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching the URL: {e}")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    visible_text = soup.get_text(separator=" ").strip()

    # Prepare file names with unique identifiers
    domain = urlparse(url).netloc.split('.')[0]
    base_filename = sanitize_filename(f"scraped_data_{domain}")
    csv_file = get_unique_filename(base_filename, ".csv", "static")
    json_file = get_unique_filename(base_filename, ".json", "static")

    # Save the scraped text to CSV
    with open(f"static/{csv_file}", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Text"])
        writer.writerow([visible_text])

    # Save the scraped text to JSON
    with open(f"static/{json_file}", mode="w", encoding="utf-8") as file:
        json.dump({"text": visible_text}, file, ensure_ascii=False, indent=4)

    # Return the scraped text and file names
    return {
        "scraped_text": visible_text,
        "csv_file": csv_file,
        "json_file": json_file
    }

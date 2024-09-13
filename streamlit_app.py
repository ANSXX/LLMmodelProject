import streamlit as st
import requests
from urllib.parse import quote

def create_download_link(file_url: str, file_label: str):
    """Generate a download link for a file."""
    return f'<a href="{file_url}" download>{file_label}</a>'

def main():
    st.title("Web Data Scraper")

    url_to_scrape = st.text_input("Enter URL:", "https://www.incometax.gov.in/iec/foportal/")
    
    # Option to overwrite existing data
    replace_existing = st.checkbox("Replace existing data", value=True)

    if st.button("Scrape Visible Text"):
        if url_to_scrape:
            encoded_url = quote(url_to_scrape, safe='')
            try:
                # Make a GET request to the FastAPI server with the URL and overwrite flag
                api_url = f"http://localhost:8000/?url={encoded_url}&replace={replace_existing}"
                server_response = requests.get(api_url)
                server_response.raise_for_status()

                json_data = server_response.json()
                if "scraped_text" in json_data:
                    st.success("Visible text successfully scraped!")
                    st.subheader("Scraped Text:")
                    st.write(json_data["scraped_text"])
                    
                    # Provide download links for the CSV and JSON files
                    if "csv_file" in json_data:
                        csv_file_url = f"http://localhost:8000/static/{json_data['csv_file']}"
                        st.markdown(create_download_link(csv_file_url, "Download CSV file"), unsafe_allow_html=True)
                    
                    if "json_file" in json_data:
                        json_file_url = f"http://localhost:8000/static/{json_data['json_file']}"
                        st.markdown(create_download_link(json_file_url, "Download JSON file"), unsafe_allow_html=True)
                elif "error" in json_data:
                    st.warning(f"Error: {json_data['error']}")
                else:
                    st.warning("Failed to scrape visible text from the URL.")
            except requests.RequestException as e:
                st.warning(f"Failed to connect to the FastAPI server. Error: {e}")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()

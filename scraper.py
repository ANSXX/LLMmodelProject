# streamlit_app.py
import streamlit as st
import requests

# Streamlit UI
def main():
    st.title("Web Data Scraper")

    # Get the URL from the user
    url_input = st.text_input("https://www.incometax.gov.in/iec/foportal/", "")

    if st.button("Scrape Visible Text"):
        if url_input:
            # Make a GET request to the FastAPI server with the URL
            response = requests.get(f"http://localhost:8000/?url={url_input}")
            if response.status_code == 200:
                data = response.json()
                if "scraped_text" in data:
                    st.success("Visible text successfully scraped!")
                    st.subheader("Scraped Text:")
                    st.write(data["scraped_text"])
                else:
                    st.warning("Failed to scrape visible text from the URL.")
            else:
                st.warning("Failed to connect to the FastAPI server.")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
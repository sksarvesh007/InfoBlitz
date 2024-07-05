import os
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from urllib.parse import urlparse, parse_qs

# Function to fetch page content
def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        return f"Error fetching {url}: {e}"

# Function to transform text
def transform_text(content):
    # Remove excessive newlines and extra spaces
    content = ' '.join(content.splitlines()).strip()
    # Replace multiple spaces with single space
    content = ' '.join(content.split())
    return content

# Function to save content to file
def save_to_file(url, content, index):
    filename = f"output/website_{index}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Link: {url}\n")
        transformed_content = transform_text(content)
        file.write(transformed_content)

# Function to save image
def save_image(url, index):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Extract image filename from URL
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        with open(f"output/image_{index}_{filename}", 'wb') as file:
            file.write(response.content)
        
        print(f"Image saved as image_{index}_{filename}")
    except Exception as e:
        print(f"Error saving image from {url}: {e}")

def main():
    query = input("Enter your search query: ")
    num_results = 10

    search_results = search(query, num_results=num_results)
    
    for i, url in enumerate(search_results, start=1):
        page_content = fetch_page_content(url)
        save_to_file(url, page_content, i)
        print(f"Content saved to website_{i}.txt")

        # Saving the first image from the search results
        if i == 1:  # Save only the first image
            image_url = fetch_first_image_url(url)
            if image_url:
                save_image(image_url, i)

def fetch_first_image_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tags = soup.find_all('img')
        if image_tags:
            return image_tags[0]['src']  # Get the src attribute of the first image tag
        else:
            print("No images found on the page.")
            return None
    except Exception as e:
        print(f"Error fetching image URL from {url}: {e}")
        return None

if __name__ == "__main__":
    main()

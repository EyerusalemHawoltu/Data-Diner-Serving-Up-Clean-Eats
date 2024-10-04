import requests
import time
import hmac
import hashlib
import base64
from urllib.parse import quote, urlencode
from bs4 import BeautifulSoup

# Pixabay API credentials
PIXABAY_API_KEY = '46350458-0bdfc3c47d4c714c7dfce84d5'  # Replace with your API key

# Base URL for Pixabay API
PIXABAY_BASE_URL = "https://pixabay.com/api/"

# Get images from Pixabay API
def get_pixabay_images(food_name):
    url = f"{PIXABAY_BASE_URL}?key={PIXABAY_API_KEY}&q={quote(food_name)}&image_type=photo"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching images: {response.status_code} - {response.text}")
        return None

# Fallback to more general search terms if no exact match is found
def fallback_food_search(food_name):
    print(f"Trying exact search for: {food_name}")
    
    # If no exact match, try with more general search terms
    search_terms = food_name.split()  # Split the name into individual words
    food_info = []  # Initialize food_info to store matched foods

    for i in range(len(search_terms) - 1, 0, -1):
        fallback_name = " ".join(search_terms[:i])
        print(f"Trying search for: {fallback_name}")
        food_info = get_food_information(fallback_name)
        if food_info:
            break  # Exit loop if a match is found
    
    return food_info

# Scrape recipes from a provided URL
url = 'https://www.delish.com/cooking/recipe-ideas/g43443854/fast-food-copycat-recipes/'  # URL to scrape

# Define headers to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

def scrape_food_names(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            html_content = response.text
            return BeautifulSoup(html_content, 'html.parser')
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if response.status_code == 429:
                print("Rate limit exceeded, sleeping before retrying...")
                time.sleep(5)
        except Exception as err:
            print(f"An error occurred: {err}")
        time.sleep(2)
    return None

# Function to extract food names from the parsed HTML
def extract_food_names(soup):
    if not soup:
        return None
    
    # Extracting all h2 tags
    h2_tags = soup.find_all('h2')
    
    # Filter and clean the names
    food_names = []
    for h2 in h2_tags:
        text = h2.get_text().strip()
        if text:
            cleaned_name = text.split('. ', 1)[-1]
            food_names.append(cleaned_name)

    return food_names[:20]

# Main function
def main():
    print("Starting web scraping...\n")
    
    # Scrape the website
    soup = scrape_food_names(url)
    
    if soup:
        # Extract the names of the foods
        food_names = extract_food_names(soup)
        
        if food_names:
            print("The Foods we have:\n")
            for i, name in enumerate(food_names, start=1):
                print(f"{i}. {name.strip()}")
            
            # Ask the user to select a food
            try:
                choice = int(input("\nEnter the number of the food you want to know more about: "))
                if 1 <= choice <= len(food_names):
                    selected_food = food_names[choice - 1]
                    print(f"\nYou selected: {selected_food}\n")
                    # Get images related to the selected food
                    images = get_pixabay_images(selected_food)
                    if images and 'hits' in images:
                        print(f"\nImages related to {selected_food}:\n")
                        for image in images['hits']:
                            print(image['webformatURL'])  # Prints the web format image URL
                    else:
                        print("No images found.")
                else:
                    print("Invalid choice. Please select a number from the list.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("No foods found.")
    
    time.sleep(2)

# Entry point
if __name__ == "__main__":
    main()

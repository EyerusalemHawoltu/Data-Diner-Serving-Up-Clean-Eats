# Food Image Scraper

This script scrapes a list of fast food recipes from a webpage, allowing you to select a food item, and then fetches images related to that food using the Pixabay API.

## Features

- Scrapes food names from a specified URL.
- Prompts the user to choose a food item from the scraped list.
- Fetches and displays related images from Pixabay for the chosen food.

## How to Use

1. **Set up the Pixabay API key**:  
   Replace the placeholder API key `'46350458-0bdfc3c47d4c714c7dfce84d5'` in the script with your own Pixabay API key. You can obtain the key by signing up at [Pixabay API](https://pixabay.com/api/docs/).

2. **Run the script**:  
   The script starts by scraping food names from a predefined URL ([Fast Food Copycat Recipes](https://www.delish.com/cooking/recipe-ideas/g43443854/fast-food-copycat-recipes/)). It displays the food names and asks you to select one.

3. **Fetch images**:  
   Once you select a food, the script fetches related images from Pixabay and prints the URLs of the images.

## Functions Overview

- `get_pixabay_images(food_name)`:  
  Fetches images from Pixabay based on the provided food name.

- `scrape_food_names(url)`:  
  Scrapes the webpage for food names and returns the parsed HTML content.

- `extract_food_names(soup)`:  
  Extracts and cleans food names from the BeautifulSoup object.

- `fallback_food_search(food_name)`:  
  Tries fallback search terms if no exact match is found on Pixabay.

- `main()`:  
  Main function that coordinates scraping and image fetching based on user input.

## Error Handling

- Handles HTTP errors and retries in case of request failure.
- Implements a rate limit handler when the API returns a `429` error code (Too Many Requests).

---

**Author**: Eyerusalem Hawoltu Afework

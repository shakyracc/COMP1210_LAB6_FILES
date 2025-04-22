# I got help from AI with this question

import os
import requests
from bs4 import BeautifulSoup  # bs4 is the BeautifulSoup module

# Start from the XKCD homepage
url = 'https://xkcd.com'

# Create a folder to store the comics (if it doesn’t exist)
os.makedirs('xkcd_comics', exist_ok=True)

while not url.endswith('#'):
    # Download the page
    print(f"Downloading page: {url}")
    res = requests.get(url)
    res.raise_for_status()

    # Parse the HTML
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find the comic image inside <div id="comic">
    comic_elem = soup.select('#comic img')
    if comic_elem:
        comic_url = 'https:' + comic_elem[0].get('src')
        print(f"Downloading image: {comic_url}")
        
        # Download the image
        img_res = requests.get(comic_url)
        img_res.raise_for_status()

        # Save the image to the local folder
        image_filename = os.path.join('xkcd_comics', os.path.basename(comic_url))
        with open(image_filename, 'wb') as img_file:
            for chunk in img_res.iter_content(100000):
                img_file.write(chunk)

    # Find the URL of the previous comic and update the URL
    prev_link = soup.select_one('a[rel="prev"]')
    url = 'https://xkcd.com' + prev_link.get('href')

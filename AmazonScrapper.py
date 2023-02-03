import csv
from bs4 import BeautifulSoup
import requests

# Define the class identifier for the product information on the Amazon India homepage
class_identifier = 'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16'
# Define the URL for the Amazon India homepage with the search query "bags"
url = "https://www.amazon.in/s?k=bags"
# Define the headers for the GET request
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}

# Create a list to store the product information from the Amazon India homepage
products_list = []
# Loop through pages 1 to 20 to retrieve the product information for each page
for page_num in range(1, 21):
    # Update the URL for each page
    url = f"https://www.amazon.in/s?k=bags&page={page_num}&qid=1675361504&ref=sr_pg_{page_num}"
    # Make a GET request to the URL
    page = requests.get(url, headers=headers)
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(page.content, "lxml")

    # Find the product links on the page
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    links_list = [link.get('href') for link in links]
    # Find the product titles on the page
    titles = soup.find_all("span", attrs={'class':'a-size-medium a-color-base a-text-normal'})
    # Find the product prices on the page
    price = soup.find_all("span", attrs={'class':"a-price-whole"})
    # Find the number of reviews for each product on the page
    noofreviews = soup.find_all("span", attrs={'class':"a-size-base s-underline-text"})

    # Loop through each product on the page
    for link, title, p, reviews in zip(links_list, titles, price, noofreviews):
        # Store the product information in a dictionary
        product = {
            'link': link,
            'title': title.text,
            'price': p.text,
            'noofreviews': reviews.text
        }
        # Append the product information to the "products_list"
        products_list.append(product)

# Create a list to store the product details
product_details = []
# Loop through each product link in the "links_list"
for link in links_list:
    # Make a GET request to the product detail page
    new_webpage = requests.get("https://www.amazon.com" + link, headers=headers)
    # Use BeautifulSoup to parse the HTML conten
    new_soup = BeautifulSoup(new_webpage.content, "lxml")

    try:
        asin = new_soup.find("th", class_="a-color-secondary a-size-base prodDetSectionEntry", string="ASIN").find_next("td").text.strip()
        manufacturer = new_soup.find("th", class_="a-color-secondary a-size-base prodDetSectionEntry", string="Manufacturer").find_next("td").text.strip()
    except:
        # add error handling as needed
        continue

    product_details.append({
        'asin': asin,
        'manufacturer': manufacturer
    })

# Write to CSV file
with open("products.csv", "w", newline="", encoding='utf-8') as f:
   writer = csv.DictWriter(f, fieldnames=['title', 'price', 'noofreviews', 'link', 'asin', 'manufacturer'])

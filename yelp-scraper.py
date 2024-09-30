'''
This script scrapes reviews and ratings from a Yelp page and saves the data to a CSV file.
The user is prompted to enter the URL of the Yelp page they want to scrape.
The script extracts the business name, total number of reviews, reviewer names, review text, and ratings.
The extracted data is then saved to a CSV file with the format 'yelp_reviews_{business_name}.csv'.
Author: Mahender Reddy Thota
Scraper last updated on 2024-09-29
'''

import requests
from bs4 import BeautifulSoup
import csv

# Target Yelp page URL
url = input('Enter the URL of the Yelp page you want to scrape: ')

# Send a GET request to fetch the page content
response = requests.get(url)
response.raise_for_status()  # Raise an exception for bad status codes

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the desired data
business_name = soup.find('h1', class_='y-css-olzveb').text.strip()

# Extract the total number of reviews
total_reviews = soup.find('div', class_='y-css-6i2mgn').text.strip().split(' ')[0]

# Find all review containers
review_containers = soup.find_all('li', class_='y-css-mu4kr5')


# Initialize lists to store extracted data
reviewer_names = []
ratings = []
reviews = []

for container in review_containers:
    
    review_text_element = container.find('p', class_ = 'comment__09f24__D0cxf y-css-h9c2fl')
    review_text = review_text_element.text.strip().replace('\n', '') if review_text_element else 'No review text'

    rating_element = container.find('div', class_='y-css-1gng1og')
    rating = rating_element.find('div', class_ = 'y-css-1jwbncq').get('aria-label').strip().split(' ')[0].replace('\n', '') if rating_element else 'No rating'

    reviewer_element = container.find('div', class_ = 'user-passport-info y-css-ya63xp')
    reviewer = reviewer_element.find('a', class_ = 'y-css-12ly5yx').text.strip() if reviewer_element else 'No reviewer'

    
    reviews.append(review_text)
    ratings.append(rating)
    reviewer_names.append(reviewer)

# Write the data to a CSV file
filename = 'yelp_reviews_' + business_name + '.csv'
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Business Name', 'Reviewer Name', 'Rating', 'Review'])  # Write header row

    # Write data rows for each review
    for i in range(len(reviews)):
        writer.writerow([business_name, reviewer_names[i], ratings[i], reviews[i]])


print("Data has been successfully scraped and saved to 'yelp_reviews_"+ business_name + ".csv' file.")
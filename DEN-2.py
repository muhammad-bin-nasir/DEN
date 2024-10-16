import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_website(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []
        for heading in soup.find_all('h2'):
            data.append([heading.text.strip()])
        save_to_csv(data, 'output.csv')
        
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Heading'])  
        writer.writerows(data)
    print(f"Data saved to {filename}")

exampleUrl = 'https://en.wikipedia.org/wiki/Atif_Aslam'

scrape_website(exampleUrl)

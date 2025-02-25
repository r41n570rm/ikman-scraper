from bs4 import BeautifulSoup
import requests
import pandas as pd

# Get search query
query_name = str(input('Enter search query: '))   

# Get output file name      
output_filename = str(input('Enter output file name (without the .csv extension): '))    
output_filename += ".csv"                

master_list = []

def scrapeIkman(page_num):
  for page in range(1,page_num+1):
    source = f'https://ikman.lk/en/ads/sri-lanka?sort=date&order=desc&buy_now=0&urgent=0&query={query_name}&page={page_num}'
    html = requests.get(source).text
    soup = BeautifulSoup(html, 'lxml')

    for ad in soup.find_all('li', class_='normal--2QYVk gtm-normal-ad'):
      data_dict = {}
      item_name = ad.h2.text
      item_price = ad.find('div', class_='price--3SnqI color--t0tGX').text
      item_photo = ad.img['src']
      item_path = ad.a['href']
      item_link = f'https://ikman.lk{item_path}'
      data_dict['Photo'] = item_photo
      data_dict['Name'] = item_name
      data_dict['Price'] = item_price
      data_dict['Link'] = item_link
      master_list.append(data_dict)

# Get number of pages to scrape
num_pages = int(input("Enter the number of pages to scrape: "))

scrapeIkman(num_pages)

df = pd.DataFrame(master_list)
df.to_csv(output_filename, index=False)
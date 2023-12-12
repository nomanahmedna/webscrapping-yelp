#this code runs best on vpn when location is selected USA.


import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Read URLs from a text file
with open('urls.txt', 'r') as file:
    urls = file.read().splitlines()

# Create an empty list to store the extracted data
data_list = []

# Iterate through each URL
for url in urls:
    # Making a GET request for each URL
    r = requests.get(url)
    
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    # to extract website and phone
    web_phone = soup.find_all("p", "css-1p9ibgf")
    useful_web_phone = []

    for items in web_phone:
        items = items.text
        useful_web_phone.append(items)

    # Add the extracted data to the list
    data_list.append(useful_web_phone)

# If there is data in the list
if data_list:
    # Determine the maximum number of columns across all rows
    max_columns = max(len(row) for row in data_list)

    # Fill missing values with None
    data_list = [row + [None] * (max_columns - len(row)) for row in data_list]

    # Generate column names as 'Column1', 'Column2', ..., 'ColumnN'
    columns = [f'Column{i}' for i in range(1, max_columns + 1)]

    # Create a DataFrame from the list with dynamically generated column names
    df = pd.DataFrame(data_list, columns=columns)

    # Export the DataFrame to a CSV file
    df.to_csv('output.csv', index=False)

    # Print a message to indicate that the export is complete
    print("Data has been exported to 'output.csv'")
else:
    print("No data to export.")

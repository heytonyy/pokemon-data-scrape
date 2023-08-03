import requests
from bs4 import BeautifulSoup
import csv

url = "https://pokemondb.net/pokedex/all"

# Get HTML from URL
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Get table from HTML
table = soup.find("table", class_="data-table")

# Get column headers
headers = [header.text.strip() for header in table.find("tr").find_all("th")]

# Get data from each row
rows = []
for row in table.find_all("tr")[1:]:
    row_data = [cell.text.strip() for cell in row.find_all("td")]
    row_dict = dict(zip(headers, row_data))
    rows.append(row_dict)


# Open file for writing each column to a separate text file

# Get column headers
headers = list(rows[0].keys())

# Open file for writing each column
for header in headers:
    with open(f"{header}.txt", "w", newline="") as f:
        writer = csv.writer(f)

        # Write header row
        writer.writerow([header])

        # Write column data from each row
        for row in rows:
            writer.writerow([row[header]])


# Get image URLs
img_urls = []

for row in table.find_all("tr")[1:]:
    # Get img src attribute
    img_url = (
        row.find("td", class_="cell-num cell-fixed")
        .find("span", class_="infocard-cell-img")
        .img["src"]
    )

    # Append to list
    img_urls.append(img_url)

with open("image_urls.txt", "w") as f:
    for url in img_urls:
        f.write(url + "\n")

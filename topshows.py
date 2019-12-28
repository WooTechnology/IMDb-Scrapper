''' TOP 250 TV SHOWS BASED ON IMDb RATING'''

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"

page = urllib.request.urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

right_table=soup.find('tbody', class_="lister-list")

show = []
show_star = []
year = []
rating = []

for row in right_table.findAll("tr"):
     cells = row.findAll('td')
     show.append(cells[1].find('a').get_text(strip=True))
     show_star.append(cells[1].find('a')['title'])
     year.append(cells[1].find('span').get_text(strip=True))
     rating.append(cells[2].find('strong').get_text(strip=True))

df = pd.DataFrame(show,columns=['Show'])
df['Starring'] = show_star
df['Year of Release'] = year
df['User Rating'] = rating

print(df)

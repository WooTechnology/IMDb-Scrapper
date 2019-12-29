from bs4 import BeautifulSoup
import urllib.request

choice = input("Enter the choice of TV show/Movie")

words = choice.split()

updated_choice = ""

for word in words:
    updated_choice = updated_choice + "+" + word

#To remove the inital + sign from the string
updated_choice = updated_choice[1:]

url = "https://www.imdb.com/find?q="+ updated_choice + "&ref_=nv_sr_sm"

page = urllib.request.urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

right_table=soup.find('table', class_="findList")

ans = ""
show_url = "https://www.imdb.com"
for row in right_table.findAll("tr"):
     cells = row.findAll('td', class_="result_text")
     for cell in cells:
         ans = show_url + cell.find('a').get('href')
         page = urllib.request.urlopen(ans)
         soup = BeautifulSoup(page, 'html.parser')
         #Now we are on the particular shows page.
         print(soup.find('title').get_text(strip=True))
         #To deal with shows having no rating yet.
         try:
             print("User Rating ", soup.find('div', class_="ratingValue").get_text(strip=True))
         except AttributeError:
             print("No reviews yet.")
         #If it's a movie then no episodes will exist
         try:
             episode_url = soup.find('a', class_='bp_item np_episode_guide np_right_arrow').get('href')
             print(episode_url)
         except:
             pass
         print()

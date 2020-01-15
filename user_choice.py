from bs4 import BeautifulSoup
import urllib.request
import datetime

def convert_date(d):
    month = {'Jan.':'01', 'Feb.':'02', 'Mar.':'03', 'Apr.':'04', 'May':'05',
             'Jun.':'06', 'Jul.':'07', 'Aug.':'08', 'Sep.':'09', 'Oct.':'10',
             'Nov.':'11', 'Dec.':'12'}
    part = d.split()
    new_date = part[0] + "/" + month[part[1]] + "/" + part[2]
    return new_date

#main program
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
             ans = show_url + episode_url
             page = urllib.request.urlopen(ans)
             soup = BeautifulSoup(page, 'html.parser')
             current_date = datetime.datetime.now().strftime("%d/%m/%Y")
             episode_date = soup.find_all('div', class_='airdate')
             #finding next episode date
             for date in episode_date:
                 date = date.get_text(strip=True)
                 #Making dates a datetime object so that they can be compared.
                 new_date = datetime.datetime.strptime(convert_date(date), "%d/%m/%Y")
                 curr_date = datetime.datetime.strptime(current_date, "%d/%m/%Y")

                 if new_date >= curr_date:
                     print("Next episode: " + date)
                     break
             else:
                 #There could be a possibilty that there is a new season episode for the show
                 try:
                     season_url = soup.find('a', {'id' : 'load_next_episodes'}).get('href')
                     season_url = ans + season_url
                     page = urllib.request.urlopen(season_url)
                     soup = BeautifulSoup(page, 'html.parser')
                     new_season = soup.find('div', class_='airdate').get_text(strip=True)
                     print("Next season: " + new_season)
                 except:
                     print("No new episodes/seasons upcoming yet!")
         except:
             pass
         print()

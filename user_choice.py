from bs4 import BeautifulSoup
import urllib.request

choice = input("Enter the choice of TV show/Movie")

words = choice.split()

updated_choice = ""

for word in words:
    updated_choice = updated_choice + "+" + word

#To remove the inital + sign from the string
updated_choice = updated_choice[1:]
print(updated_choice)

url = "https://www.imdb.com/find?q="+ updated_choice + "&ref_=nv_sr_sm"

page = urllib.request.urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

print(url)

from bs4 import BeautifulSoup
import urllib.request
import datetime
import mysql.connector
from tabulate import tabulate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="####",
  database="tvshows"
)

mycursor = mydb.cursor()
#We have created this database
# mycursor.execute("CREATE DATABASE tvshows")

#creating a table to store the email and users choice of shows
try:
    mycursor.execute("CREATE TABLE User_Choice (Email VARCHAR(255), TV_Shows VARCHAR(255)")
    mydb.commit()
except:
    mydb.rollback()

#Add data to your table
def add_data(email, shows):
    try:
        mycursor.execute("INSERT INTO User_Choice(Email, TV_Shows) VALUES (email, shows);")
        mydb.commit()
    except:
        mydb.rollback()

#Function to convert date in desired format so that it can be compared.
def convert_date(d):
    month = {'Jan.':'01', 'Feb.':'02', 'Mar.':'03', 'Apr.':'04', 'May':'05',
             'Jun.':'06', 'Jul.':'07', 'Aug.':'08', 'Sep.':'09', 'Oct.':'10',
             'Nov.':'11', 'Dec.':'12'}
    part = d.split()
    new_date = part[0] + "/" + month[part[1]] + "/" + part[2]
    return new_date

#Global variable which will store our HTML email message
html = ""

#main program
def main(entered_choice):
    global html

    choice = entered_choice
    final_output = ""
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
    rvs = ""
    img_url = ""
    title = ""
    url = ""
    show_url = "https://www.imdb.com"
    #if the entered show exists or not
    try:
        row = right_table.find("tr")
        cells = row.findAll('td', class_="result_text")
        for cell in cells:
         ans = show_url + cell.find('a').get('href')
         url = ans #For storing the link of the show
         page = urllib.request.urlopen(ans)
         soup = BeautifulSoup(page, 'html.parser')
         #Now we are on the particular shows page.
         img_url = soup.find('div', class_="poster")
         title = soup.find('div', class_="title_wrapper").h1.get_text(strip=True)
         print(title)
         #To deal with shows having no rating yet.
         try:
             rvs = soup.find('div', class_="ratingValue").get_text(strip=True)
         except AttributeError:
             rvs = "No reviews yet."
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
                     final_output = "Next episode: " + date
                     break
             else:
                 #There could be a possibilty that there is a new season episode for the show
                 try:
                     season_url = soup.find('a', {'id' : 'load_next_episodes'}).get('href')
                     season_url = ans + season_url
                     page = urllib.request.urlopen(season_url)
                     soup = BeautifulSoup(page, 'html.parser')
                     new_season = soup.find('div', class_='airdate').get_text(strip=True)
                     final_output = "Next season: " + new_season
                 except:
                     final_output = "No new episodes/seasons upcoming yet!"
         except:
             final_output = "No information available"

         #Checking if image for the show is available
         try:
             img_url = img_url.img.get('src')
         except:
             img_url = "https://bit.ly/2CMBIFr"
        image =  """<tr>
                <td width="80" valign="top" bgcolor="d0d0d0" style="padding:5px;">
                <img src=\"""" + img_url + """\" width="80" height="120"/>
                </td>
                <td width="15"></td>
                <td valign="top">"""

    except:
        final_output = "This show doesn't exist."

    #Making the final email message
    title = """<h3>""" + """<a href=""" + url + """>""" + title + """</a><br>""" + """</h3>"""
    final_output = """<p><em>""" + final_output + """</em></p>"""
    reviews = """<p><em>""" + "Reviews: " + rvs + """</em></p>"""
    series_content = image + """<b>""" + "TV series name : " + """</b>""" + title + final_output + reviews
    html += series_content


#Functioning of the code begins here
user_email = input("Enter your email id: ")
shows_input = input("Enter the list of shows(seperated by comma): ")
shows_list = shows_input.split(',')
add_data(user_email, shows_input)
print("\nFetching data for shows...\n")

for show in shows_list:
    main(show)

#SENDING EMAIL
try:
    message = MIMEMultipart()
    message["Subject"] = "Schedule of your favorite TV Shows"
    message["From"] = sender_email
    message["To"] = user_email

    message.attach(MIMEText(html, "html"))

    s = smtplib.SMTP('smtp.gmail.com')
    s.starttls()
    password = "sender_email_password"
    s.login(sender_email, password)

    s.sendmail(sender_email, user_email , message.as_string())
    s.quit()
    print("Email sent successfully!")
except:
    print("Unable to send the email")

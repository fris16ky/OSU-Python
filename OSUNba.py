#Keeping the NBA code separate so that I can work on them both. Get football working first, then deal with the NBA!

#For now, seems like I can't do the NBA without hardcoding it. There's no rhyme or reason to the stats shown on the page I was looking at, and I can't search them up on Google or ESPN
#Since there's unique IDs. So, might try to figure out a way to work with this current website, or just clean up this code and only do NFL. OR just hardcode it for NBA and keep that separate

#Here's my code from what I briefly worked on in the main file
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

#Create a new instance of the Chrome driver
driver = webdriver.Chrome()
nbaCollegeInfo = []
driver.get("https://basketball.realgm.com/ncaa/conferences/Big-Ten-Conference/2/Ohio-State/103/nba-players")
#Wait 10 seconds for the page to load
driver.implicitly_wait(10)
#Get the page source/all of it's code
html_nba = driver.page_source
soup_nba = BeautifulSoup(html_nba, "html.parser")

#This website is a bit trickier. I think I found an alright idea, but it's not working atm, so we'll need to come back and fix it. 

starting_point = soup_nba.find("tbody")

# Start iterating from the next row after the starting point
current_row = starting_point.find_next_sibling("tr")

# Iterate through the rows until encountering <tr><td>Oklahoma</td></tr>
while current_row:
    # Print the contents of current_row for debugging
    print(current_row)

   #Extracting data for each player: 
    Name = current_row.find("a").text.strip()
    Position = current_row.find_all("td")[1].text.strip()
    Team = current_row.find_all("a")[2].text.strip()
    Name_href = current_row.find("a")["href"]

    #finding the first and 2nd anchor tags, taking the href for the player, position of the third td tag
    nbaCollegeInfo.append({"Name": Name, "Name_Href": Name_href, "Team": Team, "Position": Position})
    
    # Move to the next row
    next_row = current_row.find_next_sibling("tr")
    
    # Check if the next row is outside of the tbody element
    if next_row and next_row.parent.name != 'tbody':
        break
    
    # Update current_row
    current_row = next_row

    # Print a message indicating that we're moving to the next row
    print("Moving to next row...")


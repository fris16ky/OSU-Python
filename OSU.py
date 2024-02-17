from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

#LET'S GO - Restarting then re- "pip install"ing worked! Now we should be good to start my testing

#This personal project is my SECOND attempt at Web Scraping
#The idea is to parse through various websites (mainly ESPN) to gather statistical information on all Ohio State Buckeyes
#that are playing in the 3 major sports (NFL, NBA, MLB - albeit there are 0 active MLB players, seems like 0 in the NHL too)

#Idea NFL: This code SHOULD Retrieve important information from a website, including the Name, Team, and Position of each player
#it will ALSO take a hyperlink attached to their name, which directs to their statistics page on ESPN. 
#The code will then emulate/run that link in order to get the dynamic data of the website, and then pull all important statistical values
#for each player. This data will be formatted appropriately (i.e. Terry McLaurin had 1,002 receiving yards on 79 receptions and 132 targets. His longest
# was a catch for 48 yards, received 47 first downs, 4 Touchdowns, and had 0 Rushing Attempts and 0 total fumbles)
#BUT, this will all be written out in a .txt file that will be saved to the users computer! That way it's a ton cleaner, and I get to learn new stuff. 

#Idea NBA is essentially the same, albeit more and different stats (there are, on average, more important stats in Basketball)
#I MIGHT include win-loss records too, not sure. But this is pulling data from each players LAST SEASON ONLY - not careers, or best years or anything. Maybe eventually

#We're using Selenium since it'll open it's own Google Chrome tab instead of taking the HTML code from when the site is loaded normally
#The tags I need (for show names, durations, etc.) are added dynamically, so they're not on the base HTML
from selenium import webdriver
from selenium.webdriver.common.by import By

#Arrays for the information
baseCollegeInfo = [] #this will be the info gathered from the espn.com/nfl/college/_/letter/o
espnProInfo = [] #info from the hyperlinks in the espn college site
playerLinks = [] #stores the hyperlinks to visit each players espn stats page

#Starting the Web Scrape process

#Create a new instance of the Chrome driver
driver = webdriver.Chrome()
#Navigate to my MyAnimeList page
driver.get("https://www.espn.com/nfl/college/_/letter/o")

#Wait 10 seconds for the page to load
driver.implicitly_wait(10)
#Get the page source/all of it's code
html = driver.page_source

#Code to get the episode count of the One Piece main show
#^obv change
soup = BeautifulSoup(html, "html.parser")
#Find the tag that contains the progress/episodes watched (anything that contains the words "One Piece")
# findProgress = soup.find("td", string=lambda text: "Ohio State" in str(text))
#Not sure if that works ^ Can I do While (same as above) != Oklahoma? 
#or will that instantly stop since it CAN find Oklahoma. I think I'll need soup.next() or something idk. 

#So, the way it is in the college site, first hyperlink (a) after "Ohio State" is a player (Eli Apple). 
#NEXT Hyperlink is the team - so we don't want the href of the team, but we do want the string of the team
#Then, next value is a <td> (They're all Tds, but this one is only a td) - contains the Position
#Will this have to be a 3d array or ... idk what they're called. Heap stack or something? But where I can have an array
#but each value in the array has multiple items? Like store "Player1" Player1.Name = "Eli Apple"; Player1.Team = "Miami Dolphins", Player1.Position = "Cornerback"

#IT'S A DICTIONARY: array = []
#player1 = {"Name": "Eli Apple", "Team": "Miami Dolphins", "Position", "Cornerback"}
#array.append(player1)

#Example code from ChatGPT: 
# def create_player(name, team, position):
#     return {"Name": name, "Team": team, "Position": position}

# # Assuming you have scraped data and stored it in some variables
# # Example data for three players
# player_data = [
#     {"name": "Eli Apple", "team": "Miami Dolphins", "position": "Cornerback"},
#     {"name": "Player2", "team": "Team2", "position": "Position2"},
#     {"name": "Player3", "team": "Team3", "position": "Position3"}
# ]

# Loop through the scraped player data and add it to ArraySports
# for player in player_data:
#     player_dict = create_player(player["name"], player["team"], player["position"])
#     ArraySports.append(player_dict)


#For getting the data between Ohio State and Oklahoma, Gpt has this: 

# Find the starting point <tr><td>Ohio State</td></tr>
starting_point = soup.find("tr", string="Ohio State")

# Start iterating from the next row after the starting point
title_row = starting_point.find_next_sibling("tr")
current_row = title_row.find_next_sibling("tr")

# Iterate through the rows until encountering <tr><td>Oklahoma</td></tr>
while current_row:
    # Print the contents of current_row for debugging
    print(current_row)

    # Check if the current row contains the ending point
    if current_row.find("td").text == "Oklahoma":
        break

   #Extracting data for each player: 
    Name = current_row.find("a").text.strip()
    Team = current_row.find_all("a")[1].text.strip()
    Name_Href = current_row.find("a")["href"]
    Position = current_row.find_all("td")[2].text.strip()
    #finding the first and 2nd anchor tags, taking the href for the player, position of the third td tag
    baseCollegeInfo.append({"Name": Name,"Name_Href": Name_Href, "Team": Team, "Position": Position})

    #move to the next row: 
    current_row = current_row.find_next_sibling("tr")

    # Print a message indicating that we're moving to the next row
    print("Moving to next row...")



# Display the extracted data
for row in baseCollegeInfo:
    print(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"])

#THAT WORKS - now we need to do the hard part; Use the href to get their stats! Going to do this for the NBA too rq
#Doing NFL first!

titles = []
stats = []

#BIIIIG Problem. This isn't working. Idk if it's too much to go through, but it's not working. I should/can find a better way to streamline this as well. 
#So, I want to gather all of the titles for stats of players (i.e. Total Tackles, Kicks Blocked, Receptions, etc.) in order for it to be better or easier?
#So, CB, S, De, Dt, Lb all have the same stat titles. So do WR and TE. HB, QB, Punter have different stat titles. 
#Oline and Long Snapper have no stats whatsoever - look up PFF grade?
#Not really sure what to do ngl. This is pretty hard to both get the stats names and the stat values. I suppose I can cheat it. 
#Maybe during the intake (populating of baseCollegeInfo), if they have a defensive position (Listed on website as "Cornerback, Safety, Defensive End, Linebacker, Defensive Tackle")
#have a format for their stats? Like just worry about taking the values, and have different If conditions for printing.

#I.e. if it's a defensive player, the first stat is Total Tackles. Then Solo Tackles, then Assist Tackles. So, 46, 37, 9 will be turned into: 
#"Eli Apple has had 46 Total Tackles, 37 Solo Tackles, and 9 Assist Tackles"... for all stats. And if it's a WR/TE, have the format up as well (first rec, then targets, etc.)
#I'm tired/unmotivated rn, but work on this this weekend/later/Monday/Tuesday. I'm not even sure where I want that check. Maybe on the intake of Position?
#have a 1-6 PosNum added to the Dict? 1 for Defense, 2 for Receiver, 3 for HB, QB, Punter, Oline, which we can use that later in the foreach loop for printing!?

for link in baseCollegeInfo: 
    driver.get(link["Name_Href"])
    driver.implicitly_wait(10)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    #Pull stats. For every position that's NOT quarterback, I suppose we can just take their normal stats. For QBs, we want rushing stats too, so we'll need to figure out
    #a way to manipulate the link. (Adding /gamelog/ after "/nfl/player" to get their entire game stats)
    if link["Position"] != "Quarterback": 
        #continue with stats
        starting_point = soup.find("tr", class_="Table__TR Table__even")
        current_row = title_row.find_next("th")
        while current_row: 
            print(current_row)
            titles.append(current_row.get("title"))

            # Move to the next row
            next_row = current_row.find_next_sibling("th")

            if next_row and next_row.parent.name != 'thead':
                break

    else: 
        #manipulation time   
        break


    print(link["Name_Href"])
    print(titles)

#Close the browser
driver.quit()

#ChatGPT has it closing the browser right after the "html = driver.page_source" line.
#And before the soup = BeautifulSoup(html, "html.parser")
#Regarding driver.quit(), its placement after the soup code is generally fine. Since you're fetching the entire page source with driver.page_source before quitting the driver, it ensures that you have all the 
#necessary HTML content before parsing it with BeautifulSoup. This sequence should work without issues. It's common practice to close the Selenium webdriver after you're done using it to free up system resources. So, placing driver.quit() at the end is recommended.

#Parsing through each movie link to get its duration
# for link in movie_links: 
#     url = link
#     response = requests.get(url)
#     html_content = response.content
#     soup = BeautifulSoup(html_content, "html.parser")
#     #Find the tag that contains the duration; the span before the duration has a text of "Duration:"
#     duration_tag = soup.find("span", string="Duration:")
#     #Extract the duration (in hours/minutes) from the next sibling tag
#     duration = duration_tag.next_sibling.strip()
#     #Add the duration to the movie_durations array
#     movie_durations.append(duration)

#Printing the show/movie names
# print() #Extra line before to separate from coding glob
# print("You have watched", episode_count, "episodes of One Piece! You have also watched the following films: ")
# #Special code to print the elements of the array (movie names) all in one line
# for i in range (len(movie_names)): 
#     if i == len(movie_names) - 1: 
#         #If we're at the last element, we don't need a comma
#         print("and", movie_names[i])
#     else: 
#         #Put a comma in between each movie/film
#         print(movie_names[i], end=", ")

#Converting the movie durations array into the totalled minutes
# def convert_time(array): 
#     #Given an array of strings in the format: xx min. or xx hr. xx min.
#     total_minutes = 0
#     for time in array: 
#         #Splitting the elements up by spaces
#         parts = time.split(' ')
#         movie_minutes = 0 #number of minutes for each movie
#         for i, part in enumerate(parts): 
#             if part.isdigit(): 
#                 if i < len(parts) - 1 and parts[i+1] == 'min.': 
#                     #If we're not at the end and we're looking at minutes, add them to the current movie_minutes
#                     movie_minutes += int(part)
#                 elif i < len(parts) - 1 and parts[i+1] == 'hr.': 
#                     #If we're not at the end and we're looking at the hours, multiply by 60 then add to the current movie_minutes
#                     movie_minutes += int(part) * 60
#                 else: 
#                     movie_minutes += int(part)
#         total_minutes += movie_minutes
#     #For the One Piece main series (non-movie), we need to multiply it's general duration by how many episodes I've watched
#     #Including intro and outro, the average/general duration is 24 minutes per episode
#     total_minutes += (int(episode_count) - 1) * 24
#     total_hours = total_minutes / 60

#     print() #For a new line
#     print("You have spent", '{:,.0f}'.format(total_minutes), "minutes watching One Piece, which is also equal to", round(total_hours, 3), "hours, or", round(total_hours/24, 3), "days!")
#     #Special formatting to make 10000 go to 10,000, and rounding for clean numbers
# convert_time(movie_durations)
# print() #Line after for a cleaner viewing and reading
# #Currently (8 Movies, 939 Episodes) this will print 23,178 minutes or 386.3 Hours or 16.096 Days
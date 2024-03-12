from urllib.request import urlopen
import requests
import re
from bs4 import BeautifulSoup
import os

#This personal project is my SECOND attempt at Web Scraping
#The idea is to parse through various websites (mainly ESPN) to gather statistical information on all Ohio State Buckeyes
#that are playing in the 3 major sports - this is for the NFL. The NBA statistical recordings are more tricky, and there 
#are 0 active Buckeyes in the MLB and NHL

#We're using Selenium since it'll open it's own Google Chrome tab instead of taking the HTML code from when the site is loaded normally
from selenium import webdriver
from selenium.webdriver.common.by import By

#Arrays for the information
baseCollegeInfo = [] #this will be the info gathered from the espn.com/nfl/college/_/letter/o
espnProInfo = [] #info from the hyperlinks in the espn college site
playerLinks = [] #stores the hyperlinks to visit each players espn stats page

#Starting the Web Scrape process; Create a new instance of the Chrome driver
driver = webdriver.Chrome()
#Navigate to the ESPN page
driver.get("https://www.espn.com/nfl/college/_/letter/o")

#Wait 10 seconds for the page to load
driver.implicitly_wait(10)
#Get the page source/all of it's code
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
#For getting the data between Ohio State and Oklahoma: 
# Find the starting point <tr><td>Ohio State</td></tr>
starting_point = soup.find("tr", string="Ohio State")

# Start iterating from the next row after the starting point
title_row = starting_point.find_next_sibling("tr")
current_row = title_row.find_next_sibling("tr")

# Iterate through the rows until encountering <tr><td>Oklahoma</td></tr> (aka end of Buckeyes)
while current_row:
    # Print the contents of current_row for debugging
    # print(current_row)

    # Check if the current row contains the ending point
    if current_row.find("td").text == "Oklahoma":
        break

   #Extracting data for each player: 
    Name = current_row.find("a").text.strip()
    Team = current_row.find_all("a")[1].text.strip()
    Name_Href = current_row.find("a")["href"]
    Position = current_row.find_all("td")[2].text.strip()
    #finding the first and 2nd anchor tags, taking the href for the player, position of the third td tag
    baseCollegeInfo.append({"Name": Name,"Name_Href": Name_Href, "Team": Team, "Position": Position, "Stats": ""})

    #move to the next row: 
    current_row = current_row.find_next_sibling("tr")

    # Print a (logging) message indicating that we're moving to the next row
    print("Moving to next row...")

#Defaulting titles for each position group that has the same exact ESPN stats, for sorting/deciphering later
defense = ["Cornerback", "Safety", "Defensive End", "Linebacker", "Defensive Tackle"]
receiver = ["Tight End", "Wide Receiver"]
oline = ["Offensive Tackle", "Guard", "Center", "Long Snapper"]

#Function to determine if a value is a number (covers floats, ints, or numbers with a comma)
def is_numeric(s):
    try:
        float(s.replace(",", ""))
        return True
    except ValueError:
        return False

#Getting stats for every link
for link in baseCollegeInfo: 
    driver.get(link["Name_Href"])
    driver.implicitly_wait(10)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    #Getting stats for players that do not need advanced/further stats - All Defense, Receivers, Running Back, Punters
    if link["Position"] in defense or link["Position"] in receiver or link["Position"] == "Running Back" or link["Position"] == "Punter": 
        #print("Get stats like normal!")
        # Find the starting point by searching for the first <td> with a numerical value
        starting_point = soup.find("td", string=lambda string: string and is_numeric(string.strip())) 
        if starting_point:
            starting_point = starting_point.find_parent("tr")
        # Now, starting_point should be the table row containing the stats
        # Initialize an empty string to store the concatenated numbers
        stats_string = ""

        # Iterate over each <td> element in the found row
        if starting_point:
            for td in starting_point.find_all("td"):
                # Check if the content of the <td> element represents a numeric value
                if td.text.strip().replace(",", "").replace(".", "", 1).isdigit():
                    # If the content can be converted to a float without loss of precision,
                    # convert it to a float and then back to string to remove trailing zeros
                    float_value = float(td.text.strip().replace(",", ""))
                    if float_value.is_integer():
                        stats_string += str(int(float_value)) + " "
                    else:
                        stats_string += str(float_value) + " "

        # Add the concatenated stats string to the dictionary under the key "Stats"
        link["Stats"] = stats_string.strip()  # Remove trailing space
    elif link["Position"] in oline: 
        #Oline/Long Snappers do not have stats on ESPN. There are SOME in PFF, but the important ones are pay-walled.
        print("No Stats - oline!") 
    elif link["Position"] == "Quarterback": 
        #In order to get rushing stats for QBs (+ a few more passing stats), we need to view their full stats, which is at a new/different link. 
        #The difference for this link is that it includes /gamelog/ right after /player, so we need to replace/insert it!
        string_to_insert = "gamelog/"
        insert_index = link["Name_Href"].find("/player/") + len("/player/")
        new_link = link["Name_Href"][:insert_index] + string_to_insert + link["Name_Href"][insert_index:]
        print(new_link) #logging
        
        #Repeat process
        driver.get(new_link)
        driver.implicitly_wait(10)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        # Find the starting point by searching for the "Regular Season Stats" text within a <td> element
        starting_point = soup.find("td", string="Regular Season Stats")
        # Find the sibling <td> elements containing the statistics
        if starting_point:
            stats_tds = starting_point.find_next_siblings("td")
            if stats_tds:
                stats_string = ""
                for td in stats_tds:
                    if td.text.strip().replace(",", "").replace(".", "", 1).isdigit():
                        float_value = float(td.text.strip().replace(",", ""))
                        if float_value.is_integer():
                            stats_string += str(int(float_value)) + " "
                        else:
                            stats_string += str(float_value) + " "
                link["Stats"] = stats_string.strip()  # Remove trailing space
    else: 
        #There shouldn't be any other position name possible, but in case, handle that
        print("Cry")
    #Printing out the link + the stat values as numbers for logging
    print(link["Name_Href"])
    print(link["Stats"])

#Close the browser
driver.quit()

#Organize the stats for our current printing process + later formatted in a Text file
def organizeStats(nums, pos): 
    if pos in defense: 
        #Labels for each stat listed in numerical value in the dictionary
        labels = [
            "Total Tackles", "Solo Tackles", "Assist Tackles", "Sacks", 
            "Forced Fumbles", "Fumbles Recovered", "Fumble Recovered Yards", 
            "Interceptions", "Interception Yards", "Average Interception Return Yards", 
            "Touchdowns", "Yards - Longest Interception Return", "Passes Defensed", 
            "Stuffs", "Stuff Yards", "Kicks Blocked!"
        ]
        
        num_values = nums.split() #Split up the numbers string into individual stats
        #print(num_values) #logging
        stat_sentences = [f"{value} {label}" for value, label in zip(num_values, labels)]
        #This iterates over pairs of values in both and lines them up using zip. i.e. first 3 of num_values is 46, 37, 9. First 3 of labels is TOT, SOLO, AST, so it pairs those together

        # Join the sentences together with commas and 'and' for the last one
        formatted_sentence = ", ".join(stat_sentences[:-1]) + ", and " + stat_sentences[-1]
        return(formatted_sentence)
    elif pos in receiver: 
        labels = [
            "Receptions", "Receiving Targets", "Receiving Yards", "Yards Per Reception", 
            "Receiving Touchdowns", "Yards - Longest Reception", "Receiving First Downs", 
            "Rushing Attempts", "Rushing Yards", "Yards per Rush Attempt", 
            "Rushing Touchdowns", "Yards - Longest Rush", "Fumbles", "Fumbles Lost!"
        ]
        
        num_values = nums.split() 
        #print(num_values) #logging
        stat_sentences = [f"{value} {label}" for value, label in zip(num_values, labels)]
        formatted_sentence = ", ".join(stat_sentences[:-1]) + ", and " + stat_sentences[-1]
        return(formatted_sentence)
    elif pos in oline: 
        #Stats:
        #Jake McQuaide and Liam McCullough (starting Long Snappers) have 0 stats for Long Snappers - so can't do anything about them. 
        #Returning empty string. pain
        return(nums)
    elif pos == "Running Back": 
        labels = [
            "Rushing Attempts", "Rushing Yards", "Yards Per Rush Attempt", "Rushing Touchdowns", 
            "Yards - Longest Rush", "Receptions", "Receiving Yards", "Yards Per Reception", 
            "Receiving Touchdowns", "Yards - Longest Reception", "Fumbles", "Fumbles Lost!"
        ]
        
        num_values = nums.split()
        #print(num_values) #logging
        stat_sentences = [f"{value} {label}" for value, label in zip(num_values, labels)]
        formatted_sentence = ", ".join(stat_sentences[:-1]) + ", and " + stat_sentences[-1]
        return(formatted_sentence)
    elif pos == "Punter": 
        labels = [
            "Punts", "Gross Average Punt Yards", "Yards - Longest Punt", "Total Punt Yards", 
            "Touchbacks", "Touchback Percentage", "Punts Inside the 20", "Punts Inside the 20 Percentage",
            "Punt Returns Allowed", "Punt Return Yards", "Average Punt Return Yards", "Net Average Punt Yards"
        ]
        
        num_values = nums.split()
        #print(num_values) #logging
        stat_sentences = [f"{value} {label}" for value, label in zip(num_values, labels)]
        formatted_sentence = ", ".join(stat_sentences[:-1]) + ", and " + stat_sentences[-1]
        return(formatted_sentence)
    elif pos == "Quarterback": 
        labels = [
            "Completions", "Passing Attempts", "Passing Yards", "Completion Percentage", 
            "Yards Per Pass Attempt", "Passing Touchdowns", "Interceptions", "Yards - Longest Pass", 
            "Times Sacked", "Passer Rating", "Adjusted QBR", "Rushing Attempts", "Rushing Yards",
            "Yards Per Rush Attempt", "Rushing Touchdowns", "Yards - Longest Rush!"
        ]
        
        num_values = nums.split() 
        #print(num_values) #logging
        stat_sentences = [f"{value} {label}" for value, label in zip(num_values, labels)]
        formatted_sentence = ", ".join(stat_sentences[:-1]) + ", and " + stat_sentences[-1]
        return(formatted_sentence)
    else: 
        #Same as before; this shouldn't ever execute, but just in case
        return("Cry v2")

#File will be saved under this code folder.
file_path = "OSU.txt"

# Open the file in write mode to refresh/wipe the contents each time it's run
with open(file_path, "w") as file:
    pass  # Do nothing, just open and close the file to wipe its contents so it doesn't keep appending

#Print the extracted data
#This is what will be pasted in the txt file. All of this information here. Everything else (stats, links, moving to next row) is all for logging purposes
for row in baseCollegeInfo:
    if row["Position"] in defense: 
        #Appending our exact print contents, but add extra spaces for readability. 
        with open(file_path, "a") as file: 
            file.write(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + ".\nThis year, he recorded " + organizeStats(row["Stats"], row["Position"]) + "\n" + "\n")
        #Logging purposes
        print(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + ".\nThis year, he recorded " + organizeStats(row["Stats"], row["Position"]))
    elif row["Position"] in receiver: 
        with open(file_path, "a") as file: 
            file.write(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + ".\nThis year, he recorded " + organizeStats(row["Stats"], row["Position"]) + "\n" + "\n")
        print(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + ".\nThis year, he recorded " + organizeStats(row["Stats"], row["Position"]))
    elif row["Position"] in oline: 
        with open(file_path, "a") as file: 
            file.write(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + "! Sadly, ESPN doesn't record stats, and PFF hides theirs behind a subscription!" + "\n" + "\n")
        print(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + "! Sadly, ESPN doesn't record stats, and PFF hides theirs behind a subscription!\nWe know they were GOATED this year tho!")
    elif row["Position"] == "Running Back": 
        with open(file_path, "a") as file: 
            file.write(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + ".\nThis year, he recorded " + organizeStats(row["Stats"], row["Position"]) + "\n" + "\n")
        print(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + ".\nThis year, he recorded " + organizeStats(row["Stats"], row["Position"]))
    elif row["Position"] == "Punter": 
        with open(file_path, "a") as file: 
            file.write(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + ".\nThis year, he recorded " + organizeStats(row["Stats"], row["Position"]) + "\n" + "\n")
        print(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + ".\nThis year, he recorded " + organizeStats(row["Stats"], row["Position"]))
    elif row["Position"] == "Quarterback": 
        with open(file_path, "a") as file: 
            file.write(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + ".\nThis year, he recorded " + organizeStats(row["Stats"], row["Position"]) + "\n" + "\n")
        print(row["Name"] + " is a " + row["Position"] + " for the " + row["Team"] + ".\nThis year, he recorded " + organizeStats(row["Stats"], row["Position"]))
    else: 
        print("Cry but v3")

#This will open the file on your computer automatically after the code is finished running.
os.startfile(file_path)

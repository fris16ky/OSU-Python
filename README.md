# Purpose
Having lived in Ohio for a decade, I grew up (and still am) an Ohio State Buckeye fan. 
I am also a big nerd for statistics and constantly look for social media posts (i.e. by the NFL) about my favorite Buckeyes, or occasionally just look them up myself. 
<br>Thus birthed this project. 

# How does it work?
This project is a basic webscraper that first reaches out to a website that contains current NFL player's alma mater. <br>
From this page I begin iterating through every Buckeye, capturing their Full Name, Team Name, Position and the hyperlink attached to their name (which links to their ESPN page), and put it all in a Python Dictionary. <br>
After that, I wrote a for loop to go through every link and capture their stats (and put in the correct place of the dictionary), to put it in layman's terms. <br>
Finally, I created base string labels for each unique position to be used later, when I printed all of the information in a clean format. This project also imports the OS and writes the data to be easily read in a text editor 
(for me, Notepad), which also automatically opens upon completion. 

# Difficulties
There were quite a few challenges with this program; it definitely didn't help that I took a long break before 'completely' finishing this project (thanks Franklin for the motivation). <br>
There were typical challenges, like changing IDEs, dealing with high statistical numbers (handling commas in values that can reach the thousands), and dealing with apostrophes in names (i.e. Dre'Mont Jones) - that was not fun. <br>
When I initially 'completed' this project, I had ignored a position group; the Offensive Linemen (arguably the most important too!). This was for a few reasons: at the time, PFF hid most of their statistical information behind a paywall, 
and it was going to be a challenge to get to the PFF page for each player regardless. There was no easy fix, every player's link had a unique ID attached to it. I ended up with multiple calculations just to get the link to be used for the webscraping. <br>
It started with their main page -> taking their name from the dictionary to use the search bar -> in the first row, take THAT link, start a new driver and then finally start scraping for the stats. <br>
To keep it short (ish), I also dealt with issues on PFF (They listed 0 snaps for Long Snappers, despite Extra Points and Field Goals that should've counted). <br>
And finally, getting different stats for different players was a fun challenge. Things like Quarterbacks not even having their full stats shown on their ESPN link, to deciding which stats to capture at all, to then getting rid of empty stats as well, it was a lot. <br>
It was always worth it, though. This is one of my favorite projects, and holds a special place in my heart, even though it is extremely simple. 

# Technology Used
Half of this project was developed with VisualStudio Code, the other half with Cursor (which emulates VSCode to my knowledge). The language was Python, and I used BeautifulSoup (bs4), selenium, writing to a file (import os), and 3 helper functions. 

import requests, os, sys
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta, date

endURL = datetime.now() - timedelta(1)
endURL = endURL.strftime('%Y') + "/" + endURL.strftime('%m') + "/" + endURL.strftime('%d')
print(endURL)

print("\nLogging on...")

browser = webdriver.Chrome()
browser.get(f"https://highschoolsports.nj.com/school/oakland-indian-hills/schedule/{endURL}")

print("Sorting through games...")

gameTitles = []
gamesTitles = browser.find_elements(By.TAG_NAME, "tr")[1:]
for game in gamesTitles:
    game = str(game.text).split(" ")[0:2]
    gameTitle = " ".join(game)
    gameTitles.append(gameTitle)

#for game in games:
    #browser.find_element(By.LINK_TEXT, "Game Details").click()
    #browser.back()

#for title in gameTitles
if "Basketball" in title:
    print(f'<p class="main-text"> <span class="team">{title}</span><span class="scores">&nbsp;&nbsp;&nbsp; . . . . . . . . .   Indian Hills: 45 &nbsp;&nbsp;  Westwood: 70</span>
            <li class="scores-stats"><pre><em>&#128293; Michael Caso</em> - 2pointers: 4   3pointers: 2   free throws: 6   <span style="float: right;">&#129351; total points: 20 </span></pre></li>
            <li class="scores-stats"><pre><em>Dylan Biernacki</em> - 2pointers: 5   free throws: 1   <span style="float: right;">&#129352; total points: 11 </span></pre></li>
            <li class="scores-stats"><pre><em>Connor Matthews</em> - 2pointers: 2   free throws: 2   <span style="float: right;">&#129353; total points: 6 </span></pre></li>
            <li class="scores-stats"><pre><em>Michael Manning</em> - 2pointers: 2   <span style="float: right;">total points: 4 </span></pre></li>
            <li class="scores-stats"><pre><em>Anothony Franchina</em> - 2pointers: 2   <span style="float: right;">total points: 4 </span> </pre></li>
        </p>
        <pre>
        </pre>')

while True:
    pass
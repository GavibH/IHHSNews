import requests, os, sys
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta, date

endURL = datetime.now() - timedelta(1)
endURL = endURL.strftime('%Y') + "/" + endURL.strftime('%m') + "/" + endURL.strftime('%d')
#URL = f"https://highschoolsports.nj.com/school/oakland-indian-hills/schedule/{endURL}"
URL = f"https://highschoolsports.nj.com/school/oakland-indian-hills/schedule/2023/04/27"

print("\nLogging on...")

#--------FUNCTIONS---------------------------------------------------------------------------
#.______        ___           _______. __  ___  _______ .___________..______        ___       __       __      
#|   _  \      /   \         /       ||  |/  / |   ____||           ||   _  \      /   \     |  |     |  |     
#|  |_)  |    /  ^  \       |   (----`|  '  /  |  |__   `---|  |----`|  |_)  |    /  ^  \    |  |     |  |     
#|   _  <    /  /_\  \       \   \    |    <   |   __|      |  |     |   _  <    /  /_\  \   |  |     |  |     
#|  |_)  |  /  _____  \  .----)   |   |  .  \  |  |____     |  |     |  |_)  |  /  _____  \  |  `----.|  `----.
#|______/  /__/     \__\ |_______/    |__|\__\ |_______|    |__|     |______/  /__/     \__\ |_______||_______|

def scoreBasketball(browser, gender, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">{gender}s Basketball</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">{gender}s Basketball</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    for scoreboard in browser.find_elements(By.CLASS_NAME, "col-12.mt-3"):
        if "Indian Hills" in scoreboard.text:
            tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
            scores = []

            for rowScore in rows:
                rowScore = rowScore.text
                rowScore = rowScore.split(" ")
                scores.append(int(rowScore[6]))
                
            scores.sort()
            scores.reverse()

            positions = {}
            for pos, score in enumerate(scores):
                for row in rows:
                    row = row.text
                    row = row.split(" ")
                    totalPoints = row[6]
                    playerName = row[0] + " " + row[1]

                    check = True
                    if len(positions) > 0:
                        for key in positions:
                            if positions[key] == playerName:
                                check = False

                    if int(totalPoints) == score and int(totalPoints) != 0 and check:
                        positions[pos + 1 ] = playerName
            
            for i in range(len(positions)):
                i += 1
                for rowAgain in rows:
                    rowAgain = rowAgain.text
                    rowAgain = rowAgain.split(" ")
                    playerName = rowAgain[0] + " " + rowAgain[1]
                    if playerName == positions[i]:
                        threes = rowAgain[3]
                        twos = rowAgain[2]
                        freethrows = rowAgain[4]
                        totalPoints = rowAgain[6]
                        if i == 1:
                            print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - 2pointers: {twos}   3pointers: {threes}   free throws: {freethrows} <span class="right-stat">&#129351; Total points: {totalPoints}</span></p></li>""")
                        elif i == 2:
                            print(f"""<li class="scores-stats"><p><em>{playerName}</em> - 2pointers: {twos}   3pointers: {threes}   free throws: {freethrows} <span class="right-stat">&#129352; Total points: {totalPoints}</span></p></li>""")
                        elif i == 3:
                            print(f"""<li class="scores-stats"><p><em>{playerName}</em> - 2pointers: {twos}   3pointers: {threes}   free throws: {freethrows} <span class="right-stat">&#129353; Total points: {totalPoints}</span></p></li>""")
                        else:
                            print(f"""<li class="scores-stats"><p><em>{playerName}</em> - 2pointers: {twos}   3pointers: {threes}   free throws: {freethrows} <span class="right-stat">Total points: {totalPoints}</span></p></li>""")


    print("</div>\n<pre>\n</pre>")
        
#-----------------------------------------------------------------------------------
#____    __    ____ .______       _______     _______.___________. __       __  .__   __.   _______ 
#\   \  /  \  /   / |   _  \     |   ____|   /       |           ||  |     |  | |  \ |  |  /  _____|
# \   \/    \/   /  |  |_)  |    |  |__     |   (----`---|  |----`|  |     |  | |   \|  | |  |  __  
#  \            /   |      /     |   __|     \   \       |  |     |  |     |  | |  . `  | |  | |_ | 
#   \    /\    /    |  |\  \----.|  |____.----)   |      |  |     |  `----.|  | |  |\   | |  |__| | 
#    \__/  \__/     | _| `._____||_______|_______/       |__|     |_______||__| |__| \__|  \______| 
def scoreWrestling(browser, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">Wrestling</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">Wrestling</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    tbody = browser.find_element(By.CLASS_NAME, "table.table-borderless.table-striped.table-stats.table-sm")
    for row in tbody.find_elements(By.TAG_NAME, "tr"):
        row = row.text
        row = row.split(" ")
        if row[2] == "(IH)":

            playerName = row[0][4:] + " " + row[1]
            finish = row[4]
            if "Major" in finish:
                finish = "Major Decision"

            if "Forfeit" not in finish:
                print(f"""<li class="scores-stats"><p><em>{playerName}</em> - {finish} </p></li>""")

    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------
# _______  _______ .__   __.   ______  __  .__   __.   _______ 
#|   ____||   ____||  \ |  |  /      ||  | |  \ |  |  /  _____|
#|  |__   |  |__   |   \|  | |  ,----'|  | |   \|  | |  |  __  
#|   __|  |   __|  |  . `  | |  |     |  | |  . `  | |  | |_ | 
#|  |     |  |____ |  |\   | |  `----.|  | |  |\   | |  |__| | 
#|__|     |_______||__| \__|  \______||__| |__| \__|  \______| 

def scoreFencing(browser, gender, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">{gender}s Fencing</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">{gender}s Fencing</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    tables = browser.find_elements(By.CLASS_NAME, "col-md-6.mt-3")
    for record in tables:
        if "Indian Hills" in record.text:

            if "Saber" in record.text:
                swordType = "Saber"
            elif "Foil" in record.text:
                swordType = "Foil"
            elif "Epee" in record.text:
                swordType = "Epee"

            scores = []

            tbody = record.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
            for rowScore in rows:
                rowScore = rowScore.text
                rowScore = rowScore.split(" ")
                scores.append(int(rowScore[2]))

            scores.sort()
            scores.reverse()

            positions = {}
            for pos, score in enumerate(scores):
                for rowPos in rows:
                    rowPos = rowPos.text
                    rowPos = rowPos.split(" ")
                    playerName = rowPos[0] + " " + rowPos[1]
                    check = True
                    if len(positions) > 0:
                        for key in positions:
                            if positions[key] == playerName:
                                check = False

                    if int(rowPos[2]) == score and int(rowPos[2]) != 0 and check:
                        positions[pos + 1] = playerName

            for i in range(len(positions)):
                i += 1
                for row in rows:
                    row = row.text
                    row = row.split(" ")
                    playerName = row[0] + " " + row[1]
                    if positions[i] == playerName:
                        wins = row[2]
                        if i == 1:
                            print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Wins: {wins} <span class="right-stat">{swordType}</span></p></li>""")
                        else:
                            print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Wins: {wins} <span class="right-stat">{swordType}</span></p></li>""")


    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------
#.______     ______   ____    __    ____  __       __  .__   __.   _______ 
#|   _  \   /  __  \  \   \  /  \  /   / |  |     |  | |  \ |  |  /  _____|
#|  |_)  | |  |  |  |  \   \/    \/   /  |  |     |  | |   \|  | |  |  __  
#|   _  <  |  |  |  |   \            /   |  |     |  | |  . `  | |  | |_ | 
#|  |_)  | |  `--'  |    \    /\    /    |  `----.|  | |  |\   | |  |__| | 
#|______/   \______/      \__/  \__/     |_______||__| |__| \__|  \______| 
                                                                          
def scoreBowling(browser, gender, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">{gender}s Bowling</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">{gender}s Bowling</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    for scoreboard in browser.find_elements(By.CLASS_NAME, "col-12.mt-3"):
        if "Indian Hills" in scoreboard.text:
            tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
            scores = []

            for rowScore in rows:
                rowScore = rowScore.text
                rowScore = rowScore.split(" ")
                scores.append(int(rowScore[6]))
                
            scores.sort()
            scores.reverse()

            positions = {}
            for pos, score in enumerate(scores):
                for row in rows:
                    row = row.text
                    row = row.split(" ")
                    totalPoints = row[6]
                    playerName = row[0] + " " + row[1]

                    check = True
                    if len(positions) > 0:
                        for key in positions:
                            if positions[key] == playerName:
                                check = False

                    if int(totalPoints) == score and int(totalPoints) != 0 and check:
                        positions[pos + 1 ] = playerName
            
            for i in range(len(positions)):
                i += 1
                for rowAgain in rows:
                    rowAgain = rowAgain.text
                    rowAgain = rowAgain.split(" ")
                    playerName = rowAgain[0] + " " + rowAgain[1]
                    if playerName == positions[i]:
                        game1 = rowAgain[2]
                        game2 = rowAgain[3]
                        game3 = rowAgain[4]
                        totalPins = rowAgain[6]
                        if i == 1:
                            print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Game1: {game1}   Game2: {game2}   Game3: {game3} <span class="right-stat">&#129351; Total pins: {totalPins}</span></p></li>""")
                        elif i == 2:
                            print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Game1: {game1}   Game2: {game2}   Game3: {game3} <span class="right-stat">&#129352; Total pins: {totalPins}</span></p></li>""")
                        elif i == 3:
                            print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Game1: {game1}   Game2: {game2}   Game3: {game3} <span class="right-stat">&#129353; Total pins: {totalPins}</span></p></li>""")
                        else:
                            print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Game1: {game1}   Game2: {game2}   Game3: {game3} <span class="right-stat"> Total pins: {totalPins}</span></p></li>""")


    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------
#.______        ___           _______. _______ .______        ___       __       __      
#|   _  \      /   \         /       ||   ____||   _  \      /   \     |  |     |  |     
#|  |_)  |    /  ^  \       |   (----`|  |__   |  |_)  |    /  ^  \    |  |     |  |     
#|   _  <    /  /_\  \       \   \    |   __|  |   _  <    /  /_\  \   |  |     |  |     
#|  |_)  |  /  _____  \  .----)   |   |  |____ |  |_)  |  /  _____  \  |  `----.|  `----.
#|______/  /__/     \__\ |_______/    |_______||______/  /__/     \__\ |_______||_______|

def scoreBaseball(browser, gender, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">{gender}</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">{gender}</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    for scoreboard in browser.find_elements(By.CLASS_NAME, "col-12.mt-3"):
        if "Indian Hills" in scoreboard.text:
            if "Pitching" in scoreboard.text:

                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                pitchCount = []
                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    if "(" in rowScore[2]:
                        del rowScore[2]
                    pitchCount.append(int(rowScore[2]))
                    
                pitchCount.sort()
                pitchCount.reverse()
                
                positions = {}
                for pos, pitch in enumerate(pitchCount):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        if "(" in row[2]:
                            del row[2]
                        pitches = row[2]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(pitches) == pitch and int(pitches) != 0 and check:
                            positions[pos + 1] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        if "(" in rowAgain[2]:
                            del rowAgain[2]
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            pitches = rowAgain[2]
                            earnedRuns = rowAgain[6]
                            strikeouts = rowAgain[8]
                            if gender == "Baseball":
                                era = rowAgain[10]
                            elif gender == "Softball":
                                era = rowAgain[9]
                            print(f"""<li class="scores-stats"><p><em>(PITCHER) {playerName}</em> - Pitches: {pitches}   Strikeouts: {strikeouts}   Earned Runs: {earnedRuns} <span class="right-stat">ERA: {era}</span></p></li>""")


            else:
                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                hitsList = []

                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    hitsList.append(int(rowScore[4]))
                    
                hitsList.sort()
                hitsList.reverse()

                positions = {}
                for pos, score in enumerate(hitsList):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        hits = row[4]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(hits) == score and int(hits) != 0 and check:
                            positions[pos + 1 ] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            runs = rowAgain[3]
                            hits = rowAgain[4]
                            atBats = rowAgain[2]
                            homeruns = "0"
                            if int(rowAgain[4]) != 0:
                                homeruns = rowAgain[9]
                            
                            if int(homeruns) > 0:
                                if i == 1:
                                    print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - At Bats: {atBats}   Runs: {runs}   Hits: {hits}  &#11088; Homeruns: {homeruns} &#11088;<span class="right-stat">&#129351;</span></p></li>""")
                                elif i == 2:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - At Bats: {atBats}   Runs: {runs}   Hits: {hits}  &#11088; Homeruns: {homeruns} &#11088;<span class="right-stat">&#129352;</span></p></li>""")
                                elif i == 3:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - At Bats: {atBats}   Runs: {runs}   Hits: {hits}  &#11088; Homeruns: {homeruns} &#11088;<span class="right-stat">&#129353;</span></p></li>""")
                                else:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - At Bats: {atBats}   Runs: {runs}   Hits: {hits}  &#11088; Homeruns: {homeruns} &#11088;<span class="right-stat">&#11088;</span></p></li>""")
                            else:
                                if i == 1:
                                    print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - At Bats: {atBats}   Runs: {runs}   Hits: {hits} <span class="right-stat">&#129351;</span></p></li>""")
                                elif i == 2:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - At Bats: {atBats}   Runs: {runs}   Hits: {hits} <span class="right-stat">&#129352;</span></p></li>""")
                                elif i == 3:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - At Bats: {atBats}   Runs: {runs}   Hits: {hits} <span class="right-stat">&#129353;</span></p></li>""")
                                else:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - At Bats: {atBats}   Runs: {runs}   Hits: {hits} <span class="right-stat"></span></p></li>""")

    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------
#.______     ______   ____    ____  _______.    __          ___       ______ .______        ______        _______.     _______. _______ 
#|   _  \   /  __  \  \   \  /   / /       |   |  |        /   \     /      ||   _  \      /  __  \      /       |    /       ||   ____|
#|  |_)  | |  |  |  |  \   \/   / |   (----`   |  |       /  ^  \   |  ,----'|  |_)  |    |  |  |  |    |   (----`   |   (----`|  |__   
#|   _  <  |  |  |  |   \_    _/   \   \       |  |      /  /_\  \  |  |     |      /     |  |  |  |     \   \        \   \    |   __|  
#|  |_)  | |  `--'  |     |  | .----)   |      |  `----./  _____  \ |  `----.|  |\  \----.|  `--'  | .----)   |   .----)   |   |  |____ 
#|______/   \______/      |__| |_______/       |_______/__/     \__\ \______|| _| `._____| \______/  |_______/    |_______/    |_______|
                                                                                         

def scoreBoysLacrosse(browser, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">Boys Lacrosse</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">Boys Lacrosse</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    for scoreboard in browser.find_elements(By.CLASS_NAME, "col-12.mt-3"):
        if "Indian Hills" in scoreboard.text:
            if "Goalie" in scoreboard.text:
                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                saveCount = []
                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    if "(" in rowScore[2]:
                        del rowScore[2]
                    saveCount.append(int(rowScore[2]))
                    
                saveCount.sort()
                saveCount.reverse()
                
                positions = {}
                for pos, save in enumerate(saveCount):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        if "(" in row[2]:
                            del row[2]
                        saves = row[2]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(saves) == save and int(saves) != 0 and check:
                            positions[pos + 1] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        if "(" in rowAgain[2]:
                            del rowAgain[2]
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            saves = rowAgain[2]
                            print(f"""<li class="scores-stats"><p><em>(GOALIE) {playerName}</em> - Saves: {saves}</p></li>""")

            elif "Scoring" in scoreboard.text:
                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                scores = []
                fosCount = []

                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    scores.append(int(rowScore[2]))
                    fosCount.append(int(rowScore[7]))
                    
                scores.sort()
                scores.reverse()
                fosCount.sort()
                fosCount.reverse()

                for rowCheck in rows: 
                    rowCheck = rowCheck.text
                    rowCheck = rowCheck.split(" ")
                    goals = rowCheck[2]
                    fos = rowCheck[7]
                    playerName = rowCheck[0] + " " + rowCheck[1]

                    for posCheck, scoreCheck in enumerate(scores):
                        if int(goals) == scoreCheck and int(goals) != 0 and int(fos) != 0:
                            del scores[posCheck]
                            fos = "0"

                positions = {}
                positionsFos = {}
                for pos, score in enumerate(scores):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        goals = row[2]
                        fos = row[7]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(goals) == score and int(goals) != 0 and check and int(fos) == 0:
                            positions[pos + 1] = playerName

                for pos, fosScore in enumerate(fosCount):
                    for rowFos in rows:
                        rowFos = rowFos.text
                        rowFos = rowFos.split(" ")
                        fos = rowFos[7]
                        playerName = rowFos[0] + " " + rowFos[1]

                        check = True
                        if len(positionsFos) > 0:
                            for key in positionsFos:
                                if positionsFos[key] == playerName:
                                    check = False

                        if int(fos) == fosScore and int(fos) != 0 and check:
                            positionsFos[pos + 1] = playerName

                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            goals = rowAgain[2]
                            assists = rowAgain[3]
                            if i == 1:
                                print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Goals: {goals}   Assists: {assists} <span class="right-stat">&#129351; Total points: {goals}</span></p></li>""")
                            elif i == 2:
                                print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Goals: {goals}   Assists: {assists}  <span class="right-stat">&#129352; Total points: {goals}</span></p></li>""")
                            elif i == 3:
                                print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Goals: {goals}   Assists: {assists}  <span class="right-stat">&#129353; Total points: {goals}</span></p></li>""")
                            else:
                                print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Goals: {goals}   Assists: {assists}  <span class="right-stat">Total points: {goals}</span></p></li>""")
                
                for j in range(len(positionsFos)):
                    j += 1
                    for rowAgainFos in rows:
                        rowAgainFos = rowAgainFos.text
                        rowAgainFos = rowAgainFos.split(" ")
                        playerName = rowAgainFos[0] + " " + rowAgainFos[1]
                        if playerName == positionsFos[j]:
                            fos = rowAgainFos[7]
                            fosTotal = rowAgainFos[6]
                            goals = rowAgainFos[2]
                            if j == 1:
                                finalPrint = f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - """
                                if int(goals) != 0:
                                    finalPrint += f"""Goals: {goals}"""
                                finalPrint += f""" Face Offs Taken: {fosTotal}   Face Offs Won: {fos} <span class="right-stat">FOGO</span></p></li>"""
                                print(finalPrint)
                            else:
                                finalPrint = f"""<li class="scores-stats"><p><em>{playerName}</em> - """
                                if int(goals) != 0:
                                    finalPrint += f"""Goals: {goals}"""
                                finalPrint += f""" Face Offs Taken: {fosTotal}   Face Offs Won: {fos} <span class="right-stat">FOGO</span></p></li>"""
                                print(finalPrint)


    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------
#  _______  __  .______       __          _______.    __          ___       ______ .______        ______        _______.     _______. _______ 
# /  _____||  | |   _  \     |  |        /       |   |  |        /   \     /      ||   _  \      /  __  \      /       |    /       ||   ____|
#|  |  __  |  | |  |_)  |    |  |       |   (----`   |  |       /  ^  \   |  ,----'|  |_)  |    |  |  |  |    |   (----`   |   (----`|  |__   
#|  | |_ | |  | |      /     |  |        \   \       |  |      /  /_\  \  |  |     |      /     |  |  |  |     \   \        \   \    |   __|  
#|  |__| | |  | |  |\  \----.|  `----.----)   |      |  `----./  _____  \ |  `----.|  |\  \----.|  `--'  | .----)   |   .----)   |   |  |____ 
# \______| |__| | _| `._____||_______|_______/       |_______/__/     \__\ \______|| _| `._____| \______/  |_______/    |_______/    |_______|
                                                                                         

def scoreGirlsLacrosse(browser, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">Girls Lacrosse</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">Girls Lacrosse</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    for scoreboard in browser.find_elements(By.CLASS_NAME, "col-12.mt-3"):
        if "Indian Hills" in scoreboard.text:
            if "Goalie" in scoreboard.text:
                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                saveCount = []
                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    if "(" in rowScore[2]:
                        del rowScore[2]
                    saveCount.append(int(rowScore[2]))
                    
                saveCount.sort()
                saveCount.reverse()
                
                positions = {}
                for pos, save in enumerate(saveCount):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        if "(" in row[2]:
                            del row[2]
                        saves = row[2]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(saves) == save and int(saves) != 0 and check:
                            positions[pos + 1] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        if "(" in rowAgain[2]:
                            del rowAgain[2]
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            saves = rowAgain[2]
                            print(f"""<li class="scores-stats"><p><em>(GOALIE) {playerName}</em> - Saves: {saves}</p></li>""")

            elif "Scoring" in scoreboard.text:
                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                scores = []

                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    scores.append(int(rowScore[2]))
                    
                scores.sort()
                scores.reverse()

                positions = {}
                for pos, score in enumerate(scores):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        goals = row[2]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(goals) == score and int(goals) != 0 and check:
                            positions[pos + 1 ] = playerName
            

                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            goals = rowAgain[2]
                            assists = rowAgain[3]
                            drawControls = rowAgain[6]
                            if i == 1:
                                finalPrint = f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Goals: {goals}   Assists: {assists}"""
                                if int(drawControls) != 0:
                                    finalPrint += f""" Draw Controls: {drawControls}"""
                                finalPrint += f""" <span class="right-stat">&#129351; Total points: {goals}</span></p></li>"""
                                print(finalPrint)
                            elif i == 2:
                                finalPrint = f"""<li class="scores-stats"><p><em>{playerName}</em> - Goals: {goals}   Assists: {assists}"""
                                if int(drawControls) != 0:
                                    finalPrint += f""" Draw Controls: {drawControls}"""
                                finalPrint += f""" <span class="right-stat">&#129352; Total points: {goals}</span></p></li>"""
                                print(finalPrint)
                            elif i == 3:
                                finalPrint = f"""<li class="scores-stats"><p><em>{playerName}</em> - Goals: {goals}   Assists: {assists}"""
                                if int(drawControls) != 0:
                                    finalPrint += f""" Draw Controls: {drawControls}"""
                                finalPrint += f""" <span class="right-stat">&#129353; Total points: {goals}</span></p></li>"""
                                print(finalPrint)
                            else:
                                finalPrint = f"""<li class="scores-stats"><p><em>{playerName}</em> - Goals: {goals}   Assists: {assists}"""
                                if int(drawControls) != 0:
                                    finalPrint += f""" Draw Controls: {drawControls}"""
                                finalPrint += f""" <span class="right-stat">Total points: {goals}</span></p></li>"""
                                print(finalPrint)

    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------
#____    ____  ______    __       __       ___________    ____ .______        ___       __       __      
#\   \  /   / /  __  \  |  |     |  |     |   ____\   \  /   / |   _  \      /   \     |  |     |  |     
# \   \/   / |  |  |  | |  |     |  |     |  |__   \   \/   /  |  |_)  |    /  ^  \    |  |     |  |     
#  \      /  |  |  |  | |  |     |  |     |   __|   \_    _/   |   _  <    /  /_\  \   |  |     |  |     
#   \    /   |  `--'  | |  `----.|  `----.|  |____    |  |     |  |_)  |  /  _____  \  |  `----.|  `----.
#    \__/     \______/  |_______||_______||_______|   |__|     |______/  /__/     \__\ |_______||_______|

def scoreVolleyball(browser, gender, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">{gender}s Volleyball</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">{gender}s Volleyball</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    for scoreboard in browser.find_elements(By.CLASS_NAME, "col-12.mt-3"):
        if "Indian Hills" in scoreboard.text:
            tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
            killCount = []

            for rowScore in rows:
                rowScore = rowScore.text
                rowScore = rowScore.split(" ")
                killCount.append(int(rowScore[2]))
                
            killCount.sort()
            killCount.reverse()

            positions = {}
            for pos, kill in enumerate(killCount):
                for row in rows:
                    row = row.text
                    row = row.split(" ")
                    kills = row[2]
                    playerName = row[0] + " " + row[1]

                    check = True
                    if len(positions) > 0:
                        for key in positions:
                            if positions[key] == playerName:
                                check = False

                    if int(kills) == kill and check:
                        positions[pos + 1 ] = playerName
            
            for i in range(len(positions)):
                i += 1
                for rowAgain in rows:
                    rowAgain = rowAgain.text
                    rowAgain = rowAgain.split(" ")
                    playerName = rowAgain[0] + " " + rowAgain[1]
                    if playerName == positions[i]:
                        blocks = rowAgain[3]
                        digs = rowAgain[4]
                        kills = rowAgain[2]
                        servicePoints = rowAgain[6]
                        if int(kills) != 0:
                            if int(servicePoints) == 0:
                                if i == 1:
                                    print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Kills: {kills}   Blocks: {blocks}   Digs: {digs} <span class="right-stat">&#129351;</span></p></li>""")
                                elif i == 2:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Kills: {kills}   Blocks: {blocks}   Digs: {digs} <span class="right-stat">&#129352;</span></p></li>""")
                                elif i == 3:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Kills: {kills}   Blocks: {blocks}   Digs: {digs} <span class="right-stat">&#129353;</span></p></li>""")
                                else:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Kills: {kills}   Blocks: {blocks}   Digs: {digs} </p></li>""")
                            else:
                                if i == 1:
                                    print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Kills: {kills}   Blocks: {blocks}   Digs: {digs}  Service Points: {servicePoints} <span class="right-stat">&#129351;</span></p></li>""")
                                elif i == 2:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Kills: {kills}   Blocks: {blocks}   Digs: {digs} Service Points: {servicePoints}<span class="right-stat">&#129352;</span></p></li>""")
                                elif i == 3:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Kills: {kills}   Blocks: {blocks}   Digs: {digs} Service Points: {servicePoints}<span class="right-stat">&#129353;</span></p></li>""")
                                else:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Kills: {kills}   Blocks: {blocks}   Digs: {digs} Service Points: {servicePoints}</p></li>""")
                        else:
                            if int(servicePoints) != 0:
                                if i == 1:
                                    print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Service Points: {servicePoints} <span class="right-stat">&#129351;</span></p></li>""")
                                elif i == 2:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Service Points: {servicePoints} <span class="right-stat">&#129352;</span></p></li>""")
                                elif i == 3:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Service Points: {servicePoints} <span class="right-stat">&#129353;</span></p></li>""")
                                else:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Service Points: {servicePoints} </p></li>""")


    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------
#  _______   ______    __       _______ 
# /  _____| /  __  \  |  |     |   ____|
#|  |  __  |  |  |  | |  |     |  |__   
#|  | |_ | |  |  |  | |  |     |   __|  
#|  |__| | |  `--'  | |  `----.|  |     
# \______|  \______/  |_______||__|    

def scoreGolf(browser, gender, hillsScore, oppScore, opponent):
    if float(hillsScore) < float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">{gender}s Golf</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">{gender}s Golf</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    for scoreboard in browser.find_elements(By.CLASS_NAME, "card"):
        if "Results" in scoreboard.text:
            tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")

            for oppPos, oppCheck in enumerate(rows):
                oppCheck = oppCheck.text
                if "Indian Hills" not in oppCheck:
                    del rows[oppPos]
            
            pos = 1
            positions = {}
            for player in rows:
                player = player.text
                player = player.split(" ")
                positions[pos] = player[1] + " " + player[2]
                pos += 1
            
            for row in rows:
                row = row.text
                row = row.split(" ")
                del row[3]
                del row[3]
                playerName = row[1] + " " + row[2]
                spot = int(row[0])
                points = row[3]
                if positions[1] == playerName:
                    print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Score: {points} <span class="right-stat">&#129351;</span></p></li>""")
                elif positions[2] == playerName:
                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Score: {points} <span class="right-stat">&#129352;</span></p></li>""")
                elif positions[3] == playerName:
                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Score: {points} <span class="right-stat">&#129353;</span></p></li>""")
                else:
                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Score: {points} </p></li>""")

        elif "Overview" in scoreboard.text:
            tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
            row = tbody.find_element(By.TAG_NAME, "tr")

            row = row.text
            row = row.split(" ")

            coursePar = row[0]
            holesPlayed = row[2]
            print(f"""<li class="scores-stats"><p style="text-decoration:underline"><em>Course Par</em> - {coursePar}    <em>Holes Played</em> - {holesPlayed}</p></li>""")

    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------
# _______   ______     ______   .___________..______        ___       __       __      
#|   ____| /  __  \   /  __  \  |           ||   _  \      /   \     |  |     |  |     
#|  |__   |  |  |  | |  |  |  | `---|  |----`|  |_)  |    /  ^  \    |  |     |  |     
#|   __|  |  |  |  | |  |  |  |     |  |     |   _  <    /  /_\  \   |  |     |  |     
#|  |     |  `--'  | |  `--'  |     |  |     |  |_)  |  /  _____  \  |  `----.|  `----.
#|__|      \______/   \______/      |__|     |______/  /__/     \__\ |_______||_______|

def scoreFootball(browser, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">Football</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">Football</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    for scoreboard in browser.find_elements(By.CLASS_NAME, "col-12.mt-3"):
        if "Indian Hills" in scoreboard.text:
            if "Passing" in scoreboard.text:

                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                compCount = []
                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    if "(" in rowScore[2]:
                        del rowScore[2]
                    compCount.append(int(rowScore[2]))
                    
                compCount.sort()
                compCount.reverse()
                
                positions = {}
                for pos, comp in enumerate(compCount):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        if "(" in row[2]:
                            del row[2]
                        comps = row[2]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(comps) == comp and int(comps) != 0 and check:
                            positions[pos + 1] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        if "(" in rowAgain[2]:
                            del rowAgain[2]
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            comps = rowAgain[2]
                            passYards = rowAgain[4]
                            passTD = rowAgain[5]

                            print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Completions: {comps}   Passing Yards: {passYards}   Passing Touchdowns: {passTD} <span class="right-stat"Quarterback</span></p></li>""")

                print("<pre>\n</pre>")

            elif "Rushing" in scoreboard.text:
                print("""<li class="scores-stats"><p style="text-decoration:underline"><em>OFFENSE</em></p></li>""")
                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                yardsCount = []

                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    yardsCount.append(int(rowScore[3]))
                    
                yardsCount.sort()
                yardsCount.reverse()

                positions = {}
                for pos, yard in enumerate(yardsCount):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        yards = row[3]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(yards) == yard and int(yards) != 0 and check:
                            positions[pos + 1 ] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            yards = rowAgain[3]
                            carries = rowAgain[2]
                            touchdowns = rowAgain[4]
                            
                            if int(touchdowns) > 0:
                                if i == 1:
                                    print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Rushing Yards: {yards}   Carries: {carries}  &#11088; Touchdowns: {touchdowns} &#11088;<span class="right-stat">&#129351;</span></p></li>""")
                                elif i == 2:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Rushing Yards: {yards}   Carries: {carries}  &#11088; Touchdowns: {touchdowns} &#11088;<span class="right-stat">&#129352;</span></p></li>""")
                                elif i == 3:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Rushing Yards: {yards}   Carries: {carries}  &#11088; Touchdowns: {touchdowns} &#11088;<span class="right-stat">&#129353;</span></p></li>""")
                                else:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Rushing Yards: {yards}   Carries: {carries}  &#11088; Touchdowns: {touchdowns} &#11088;</p></li>""")
                            else:
                                if i == 1:
                                    print(f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Rushing Yards: {yards}   Carries: {carries}  <span class="right-stat">&#129351;</span></p></li>""")
                                elif i == 2:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Rushing Yards: {yards}   Carries: {carries}  <span class="right-stat">&#129352;</span></p></li>""")
                                elif i == 3:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Rushing Yards: {yards}   Carries: {carries}  <span class="right-stat">&#129353;</span></p></li>""")
                                else:
                                    print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Rushing Yards: {yards}   Carries: {carries}  </p></li>""")
                print("<pre>\n</pre>")

            elif "Receiving" in scoreboard.text:

                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                recCount = []
                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    if "(" in rowScore[2]:
                        del rowScore[2]
                    recCount.append(int(rowScore[2]))
                    
                recCount.sort()
                recCount.reverse()
                
                positions = {}
                for pos, rec in enumerate(recCount):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        if "(" in row[2]:
                            del row[2]
                        recs = row[2]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(recs) == rec and int(recs) != 0 and check:
                            positions[pos + 1] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        if "(" in rowAgain[2]:
                            del rowAgain[2]
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            recs = rowAgain[2]
                            recYards = rowAgain[3]
                            recTD = rowAgain[4]

                            if int(recTD) != 0:
                                print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Receptions: {recs}   Receiving Yards: {recYards}   Receiving Touchdowns: {recTD} </p></li>""")
                            else:
                                print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Receptions: {recs}   Receiving Yards: {recYards}   </p></li>""")
                print("<pre>\n</pre>")

            elif "Defense" in scoreboard.text:
                print("""<li class="scores-stats"><p style="text-decoration:underline"><em>DEFENSE</em></p></li>""")
                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                tackleCount = []

                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    tackleCount.append(int(rowScore[6]))
                    
                tackleCount.sort()
                tackleCount.reverse()

                positions = {}
                for pos, tackle in enumerate(tackleCount):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        tackles = row[6]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(tackles) == tackle and int(tackles) != 0 and check:
                            positions[pos + 1 ] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            tackles = rowAgain[6]
                            sacks = rowAgain[2]
                            intercept = rowAgain[10]
                            kickBlock = rowAgain[13]

                            if i == 1:
                                finalPrint = f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Tackles: {tackles} """
                            else:
                                finalPrint = f"""<li class="scores-stats"><p><em>{playerName} - Tackles: {tackles} """

                            if int(sacks) > 0:
                                finalPrint += f"""Sacks: {sacks} """
                            
                            if int(intercept) > 0:
                                finalPrint += f"""Interceptions: {intercept} """

                            if int(kickBlock) > 0:
                                finalPrint += f"""Kicks Blocked: {kickBlock} """
                            
                            if i == 1:
                                finalPrint += f"""<span class="right-stat">&#129351;</span></p></li>"""
                            elif i == 2:
                                finalPrint += f"""<span class="right-stat">&#129352;</span></p></li>"""
                            elif i == 3:
                                finalPrint += f"""<span class="right-stat">&#129353;</span></p></li>"""
                            else:
                                finalPrint += f"""</p></li>"""
                            
                            print(finalPrint)

                print("<pre>\n</pre>")
            elif "Special" in scoreboard.text:
                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                fgCount = []
                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    if "(" in rowScore[2]:
                        del rowScore[2]
                    fgCount.append(int(rowScore[2]))
                    
                fgCount.sort()
                fgCount.reverse()
                
                positions = {}
                for pos, fg in enumerate(fgCount):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        if "(" in row[2]:
                            del row[2]
                        fgs = row[2]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(fgs) == fg and int(fgs) != 0 and check:
                            positions[pos + 1] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        if "(" in rowAgain[2]:
                            del rowAgain[2]
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            fgs = rowAgain[2]
                            fgYards = rowAgain[4]

                            print(f"""<li class="scores-stats"><p><em>{playerName}</em> - Field Goals: {fgs}   Field Goal Length (Longest): {fgYards} <span class="right-stat">Kicker</span></p></li>""")


    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------
#     _______.  ______     ______   ______  _______ .______      
#    /       | /  __  \   /      | /      ||   ____||   _  \     
#   |   (----`|  |  |  | |  ,----'|  ,----'|  |__   |  |_)  |    
#    \   \    |  |  |  | |  |     |  |     |   __|  |      /     
#.----)   |   |  `--'  | |  `----.|  `----.|  |____ |  |\  \----.
#|_______/     \______/   \______| \______||_______|| _| `._____|

def scoreSoccer(browser, gender, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">{gender}s Soccer</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">{gender}s Soccer</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    for scoreboard in browser.find_elements(By.CLASS_NAME, "col-md-6.mt-3"):
        if "Indian Hills" in scoreboard.text:
            if "Scoring" in scoreboard.text:

                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                scores = []
                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    if "(" in rowScore[2]:
                        del rowScore[2]
                    scores.append(int(rowScore[2]))
                    
                scores.sort()
                scores.reverse()
                
                positions = {}
                for pos, score in enumerate(scores):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        if "(" in row[2]:
                            del row[2]
                        goals = row[2]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(goals) == score and int(goals) != 0 and check:
                            positions[pos + 1] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        if "(" in rowAgain[2]:
                            del rowAgain[2]
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            goals = rowAgain[2]
                            assists = rowAgain[3]

                            if i == 1:
                                finalPrint = f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Goals: {goals} """
                            else:
                                finalPrint = f"""<li class="scores-stats"><p><em>{playerName}</em> - Goals: {goals} """

                            if int(assists) > 0:
                                finalPrint += f"""Assists: {assists} """

                            if i == 1:
                                finalPrint += f"""<span class="right-stat">&#129351;</span></p></li>"""
                            elif i == 2:
                                finalPrint += f"""<span class="right-stat">&#129352;</span></p></li>"""
                            elif i == 3:
                                finalPrint += f"""<span class="right-stat">&#129353;</span></p></li>"""
                            else:
                                finalPrint += f"""</p></li>"""

                            print(finalPrint)


            elif "Goalie" in scoreboard.text:
                tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")[:-1]
                saveList = []

                for rowScore in rows:
                    rowScore = rowScore.text
                    rowScore = rowScore.split(" ")
                    if "(" in rowScore[2]:
                        del rowScore[2]
                    saveList.append(int(rowScore[2]))
                    
                saveList.sort()
                saveList.reverse()

                positions = {}
                for pos, save in enumerate(saveList):
                    for row in rows:
                        row = row.text
                        row = row.split(" ")
                        if "(" in row[2]:
                            del row[2]
                        saves = row[2]
                        playerName = row[0] + " " + row[1]

                        check = True
                        if len(positions) > 0:
                            for key in positions:
                                if positions[key] == playerName:
                                    check = False

                        if int(saves) == save and int(saves) != 0 and check:
                            positions[pos + 1 ] = playerName
                
                for i in range(len(positions)):
                    i += 1
                    for rowAgain in rows:
                        rowAgain = rowAgain.text
                        rowAgain = rowAgain.split(" ")
                        if "(" in rowAgain[2]:
                            del rowAgain[2]
                        playerName = rowAgain[0] + " " + rowAgain[1]
                        if playerName == positions[i]:
                            saves = rowAgain[2]
                            
                            print(f"""<li class="scores-stats"><p><em>(GOALIE) {playerName}</em> - Saves: {saves}  </p></li>""")

    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------
#.___________. _______ .__   __. .__   __.  __       _______.
#|           ||   ____||  \ |  | |  \ |  | |  |     /       |
#`---|  |----`|  |__   |   \|  | |   \|  | |  |    |   (----`
#    |  |     |   __|  |  . `  | |  . `  | |  |     \   \    
#    |  |     |  |____ |  |\   | |  |\   | |  | .----)   |   
#    |__|     |_______||__| \__| |__| \__| |__| |_______/    
                                                            

def scoreTennis(browser, gender, hillsScore, oppScore, opponent):
    if float(hillsScore) > float(oppScore):
        print(f"""<div><p class="main-text"><img class="green-w" src="./images/GreenW.png">&nbsp;<span class="team">{gender}s Tennis</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    else:
        print(f"""<div><p class="main-text"> <span class="team">{gender}s Tennis</span><span class="scores">&nbsp;&nbsp;&nbsp;Indian Hills: {hillsScore} &nbsp;&nbsp;  {opponent}: {oppScore}</span></p>""")
    card = browser.find_element(By.CLASS_NAME, "card")
    for scoreboard in card.find_elements(By.CLASS_NAME, "card-body.p-0"):
        print(scoreboard.text)
        tbody = scoreboard.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        scores = []

        for rowScore in rows:
            rowScore = rowScore.text
            rowScore = rowScore.split(" ")
            if "(" in rowScore[2]:
                del rowScore[2]
            scores.append(int(rowScore[2]))
            
        scores.sort()
        scores.reverse()
        
        positions = {}
        for pos, score in enumerate(scores):
            for row in rows:
                row = row.text
                row = row.split(" ")
                if "(" in row[2]:
                    del row[2]
                goals = row[2]
                playerName = row[0] + " " + row[1]

                check = True
                if len(positions) > 0:
                    for key in positions:
                        if positions[key] == playerName:
                            check = False

                if int(goals) == score and int(goals) != 0 and check:
                    positions[pos + 1] = playerName
        
        for i in range(len(positions)):
            i += 1
            for rowAgain in rows:
                rowAgain = rowAgain.text
                rowAgain = rowAgain.split(" ")
                if "(" in rowAgain[2]:
                    del rowAgain[2]
                playerName = rowAgain[0] + " " + rowAgain[1]
                if playerName == positions[i]:
                    goals = rowAgain[2]
                    assists = rowAgain[3]

                    if i == 1:
                        finalPrint = f"""<li class="scores-stats"><p><em>&#128293; {playerName}</em> - Goals: {goals} """
                    else:
                        finalPrint = f"""<li class="scores-stats"><p><em>{playerName}</em> - Goals: {goals} """

                    if int(assists) > 0:
                        finalPrint += f"""Assists: {assists} """

                    if i == 1:
                        finalPrint += f"""<span class="right-stat">&#129351;</span></p></li>"""
                    elif i == 2:
                        finalPrint += f"""<span class="right-stat">&#129352;</span></p></li>"""
                    elif i == 3:
                        finalPrint += f"""<span class="right-stat">&#129353;</span></p></li>"""
                    else:
                        finalPrint += f"""</p></li>"""

                    print(finalPrint)

        

    print("</div>\n<pre>\n</pre>")

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

def trySelenium():
    browser = webdriver.Chrome()
    browser.get(URL)

    print("\nSorting through games...\n")

    tbody = browser.find_element(By.TAG_NAME, "tbody")
    games = tbody.find_elements(By.TAG_NAME, "tr")
    gameList = []

    for row in games:
        gameList.append(row.text)


        
    count = 0
    for game in gameList:
        tbody = browser.find_element(By.TAG_NAME, "tbody")
        gameUgly = tbody.find_elements(By.TAG_NAME, "tr")[count]
        game = gameUgly.text

        if "@" in game:
            game = game.replace(" @ ", ",")
        else:
            game = game.replace(" vs. ", ",")
        
        if " W " in game:
            game = game.replace(" W ", ",W")
        elif " L " in game:
            game = game.replace(" L ", ",L")

        game = game[:-13]

        if "\n" in game:
            L =[]
            for k, char in enumerate(game):
                if char == "\n":
                    L.append(k)

            kill = game[L[0]:L[1] + 1]
            game = game.replace(kill, ",")
        
        game = game.split(",")

        title = game[0]
        opponent = game[1]
        score = game[2]

        if "L" in score:
            score = score.replace("L", "")
            hillsScore = score.split("-")[1]
            oppScore = score.split("-")[0]
        elif "W" in score:
            score = score.replace("W", "")
            hillsScore = score.split("-")[0]
            oppScore = score.split("-")[1]

        browser.execute_script("window.scrollTo(0, 470)")

        link = gameUgly.find_element(By.LINK_TEXT, "Game Details")
        link.click()

        if "Basketball" in title:
            if "Girl" in title:
                scoreBasketball(browser, "Girl", hillsScore, oppScore, opponent)
            elif "Boy" in title:
                scoreBasketball(browser, "Boy", hillsScore, oppScore, opponent)

        elif "Wrestling" in title:
            scoreWrestling(browser, hillsScore, oppScore, opponent)

        elif "Fencing" in title:
            if "Girl" in title:
                scoreFencing(browser, "Girl", hillsScore, oppScore, opponent)
            elif "Boy" in title:
                scoreFencing(browser, "Boy", hillsScore, oppScore, opponent)

        elif "Swim" in title:
            scoreSwimming(browser) #UNIFINISHED (i no no wanna)

        elif "Bowling" in title:
            if "Girl" in title:
                scoreBowling(browser, "Girl", hillsScore, oppScore, opponent)
            elif "Boy" in title:
                scoreBowling(browser, "Boy", hillsScore, oppScore, opponent)

        elif "Baseball" in title:
            scoreBaseball(browser, "Baseball", hillsScore, oppScore, opponent)
        elif "Softball" in title:
            scoreBaseball(browser, "Softball", hillsScore, oppScore, opponent)
        
        elif "Lacrosse" in title:
            if "Girl" in title:
                scoreGirlsLacrosse(browser, hillsScore, oppScore, opponent)
            elif "Boy" in title:
                scoreBoysLacrosse(browser, hillsScore, oppScore, opponent)
        
        elif "Volleyball" in title:
            if "Girl" in title:
                scoreVolleyball(browser, "Girl", hillsScore, oppScore, opponent)
            elif "Boy" in title:
                scoreVolleyball(browser, "Boy", hillsScore, oppScore, opponent)

        elif "Golf" in title:
            if "Girl" in title:
                scoreGolf(browser, "Girl", hillsScore, oppScore, opponent)
            elif "Boy" in title:
                scoreGolf(browser, "Boy", hillsScore, oppScore, opponent)

        elif "Football" in title:
            scoreFootball(browser, hillsScore, oppScore, opponent)

        elif "Soccer" in title:
            if "Girl" in title:
                scoreSoccer(browser, "Girl", hillsScore, oppScore, opponent)
            elif "Boy" in title:
                scoreSoccer(browser, "Boy", hillsScore, oppScore, opponent)

        elif "Tennis" in title:
            if "Girl" in title:
                scoreTennis(browser, "Girl", hillsScore, oppScore, opponent)
            elif "Boy" in title:
                scoreTennis(browser, "Boy", hillsScore, oppScore, opponent)

        browser.back()
        count += 1


trySelenium()
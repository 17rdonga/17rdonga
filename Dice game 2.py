#Libraries:
import time
import random
import json
import os

def Add_Credentials(valid, new_login, usernames, individual): #Function to add credentials if the user wants to
    while valid  == True:
        new_player = input("Would you like to add new credentials:") # Takes input to check if user wants to add credentials
        if new_player.upper() == "YES":
            valid = False # validates input, if input is valid, valid = False,otherwise valid = True
            # and the process is repeated through the loop
            new_login = True
        elif new_player.upper()== "NO":
            valid = False
            new_login = False
        else:
            print("Enter yes or no")
            valid = True
    while new_login == True: # If the user answered with yes, they have to enter their credentials and this loop is activated
        individual = True # variable to make sure someone doesn't have the same username (used below)
        new_username = input("Enter your username:")
        new_password1 = input("Enter your password:")
        new_password2 = input("Enter your password again to verify:") #Asks for password twice to confirm
        if new_password1 == new_password2: #checks whether the password entries are the same
            for name in usernames: # compares with each username in the external file
                if new_username == name: # if username has already been used, the username is
                    # not added and they are asked again because of the while loop
                    print("Someone else has the same username, unable to add ")
                    individual = False
            if individual == True: # if the username is unique and the password entries are the same:
                file = open("usernames.txt", 'a') #open file to append to it
                file.write("\n" + new_username + ":" + new_password1) # adds the details as a string formatted in the right way
                new_login = False # to avoid looping
                print("your details have been added") #confirmation to the user
        else: # if password entries are not the same:
            print("ERROR, enter the same password twice")
            new_login = True # the user must enter again, which is made possible by the while loop
         
def lists(): # function to extract the usernames and passwords (from the external file) into separate lists
    pword = [] #initialising lists
    usrname = []
    passwords = open("usernames.txt", "r") #opening file to read
    for password in passwords:
        players_details = password.split(':') # uses split function to store details as 2D array
        pword.append(players_details[1].strip()) # the passwords and usernames are appended into different lists
        usrname.append(players_details[0])
    return usrname, pword
       
def Authorisation_Player1(usernames, passwords): # function to check whether players are authorised 
    print("Authorisation:")
    username = input("\nEnter username:")# Takes user input of usernames and passwords
    password = input("Enter password:")
    if username in usernames: #checks whether they have entered a username that is stored in the file
        index = usernames.index(username) #finds index of the entered username in the list of usernames to compare with the password
        if password == passwords[index]: # checks if the username and password correspond
            x = True # sets x to true if user is authorised to be used later in the code
        else:
            x = False
    else:
        x = False
    return [x, username]


def Roll_P1(): #function that rolls dice for the user
    roll1 = random.randint(1,6) # generates a random number between 1 and 6
    roll2 = random.randint(1,6)
    if roll1 == roll2: #checks if they roll a double
        prompt = input("You have rolled a double, so press enter to roll again:")
        roll3 = random.randint(1,6) # if the user rolls a double the dice is rolled again
    else:
        roll3 = 0 # variable which stores the number rolled after the double
    return roll1, roll2, roll3

def extra_roll(): # function that rolls one more time for the users just in case they both get the same score at the end
    roll = random.randint(1,6)
    return roll

def Score(rollscore): # function that adds up the points for the user (when they roll an odd or even number)
    if rollscore % 2 == 0: #if score is even
        rollscore += 10 # adds 10
    elif rollscore % 2 == 1: # if the score is odd
        rollscore -= 5 #takeaway 5
    if rollscore < 0: #makes sure score can never become negative
        rollscore = 0
    return rollscore
def Leaderboard(player_name, player_score, player_name2, player_score2):
    file = open("leaderboard.txt", 'r')
    if os.stat("leaderboard.txt").st_size != 0:
        for dict in file:
            remove = dict.strip()
            remove = remove.replace("'", "\"")
            converted_dict = json.loads(remove)
            scores.append(converted_dict)
    scores.append({"Name": player_name, "Score": player_score})
    scores.append({"Name": player_name2, "Score": player_score2})
    sorted_scores = sorted(scores, key=lambda k: k['Score'], reverse=True)
    file.close()
    print("\nLeaderboard:")
    if len(sorted_scores) >= 5:
        for x in range(0,5):
            print(str(x+1) + "." + sorted_scores[x]['Name'] + ":", sorted_scores[x]['Score'])        
    else:
        for x in range(0, len(sorted_scores)):
            print(str(x+1) + "." + sorted_scores[x]['Name'] + ":", sorted_scores[x]['Score'])
    return sorted_scores
def Leaderboard_update(sorted_scores):
    file1 = open("leaderboard.txt", 'w')
    for score in sorted_scores:
        file1.write(str(score) + "\n")
    file1.close()
#Variables:    
details = []
scores = []
P1_total = 0
P2_total = 0
game = True
x = False
new_login = True
valid = True
valid2 = False
individual = True

for i in range(0,2): # asks both players whether they want to add credentials
    y = lists()
    print("Player" + str(i + 1) + ":")
    Add_Credentials(valid, new_login, y[0], individual)

y = lists() #runs lists() function again to extract up to date details
#check P1 credentials:
for x in range(3):
    player1secure = Authorisation_Player1(y[0], y[1])
    if player1secure[0] == False: # if the player doesn't enter correctly
        print("\nCrendentials are wrong")
    if player1secure[0] == True:
        print(player1secure[1], "is authorised")
        break
    if x == 2 and player1secure[0] == False:
        print("\nYou have run out of tries")
else:
    print("Hi", player1secure[1], "you are authorised")

for x in range(3):
    player2secure = Authorisation_Player1(y[0], y[1])
    if player2secure[1] == player1secure[1]:
        print("You can't use the same credentials")
        player2secure[0] = False
    if player2secure[0] == False: # if the player doesn't enter correctly
        print("\nCrendentials are wrong")
    if player2secure[0] == True:
        print(player2secure[1], "is authorised")
        break
    if x == 2 and player2secure[0] == False:
        print("\nYou have run out of tries")
else:
    print("Hi", player2secure[1], "you are authorised")

if player2secure[0] == True and player1secure[0] == True: # checks that both players are authorised
    condition = True # sets condition to True, which allows them to play the game
    print("\nWelcome", player1secure[1], "and", player2secure[1], "you can now play the DICE GAME")
# Instruction:
    print("\nInstructions:") # Instructions:
    print("\n- You roll 2 6-sided die each round.\n- There are 5 rounds in total.\n- If you roll an even number,you get 10 extra points, if you roll an odd number you lose 5 points.\n- If you roll a double you get to roll again.\n- Each of your points will be added up to a total score and the player with the highest score wins.") 
else:
    condition = False
    game = False # stops the system from jumping to end game displays
    print("You cannot play, as 1 or more players are unauthorised")
    
#main:
if condition == True:
    for i in range(1,6): # Each player rolls 5 times
        p1_prompt = input(player1secure[1] + " press Enter to roll") # prompts the player, so that user is involved with rolling
        player1_score_list = Roll_P1() # rolls the dice
        if player1_score_list[2] != 0: # checks if roll3 has a value (whether they have rolled a double)
            print("you rolled a", player1_score_list[0], ", a", player1_score_list[1], "and a", player1_score_list[2]) # tells player what they rolled
        else:
            print("you rolled a", player1_score_list[0], "and a", player1_score_list[1])
        player1_score = player1_score_list[0] + player1_score_list[1] # adds two dice together
        changed_score1 = Score(player1_score) # finds actual score after calc by calling Score() function
        P1_total += changed_score1 + player1_score_list[2] # adds score to total
        print("\n" + player1secure[1]+"'s total is:", P1_total)
        
        p2_prompt = input(player2secure[1] + " press Enter to roll")
        player2_score_list = Roll_P1()
        if player2_score_list[2] != 0:
            print("you rolled a", player2_score_list[0], ", a", player2_score_list[1], "and a", player2_score_list[2])
        else:
            print("you rolled a", player2_score_list[0], "and a", player2_score_list[1])
        player2_score = player2_score_list[0] + player2_score_list[1]
        changed_score2 = Score(player2_score)
        P2_total += changed_score2 + player2_score_list[2]  
        print("\n" + player2secure[1]+"'s total is:", P2_total)

# End of game:
while game == True:
    print(player1secure[1], "'s score:", P1_total) # displays both their scores
    print(player2secure[1], "'s score:", P2_total)
    if P1_total  > P2_total: # checks if player 1 has won
        print("\n\n", player1secure[1], "has WON!!!") #displays this
        game = False # exits the game
        new_leaderboard = Leaderboard(player1secure[1], P1_total, player2secure[1], P2_total) # calls both leaderboard function to change and update the leaderboard
        Leaderboard_update(new_leaderboard)
    elif P1_total < P2_total: # checks if player 2 has won
        print("\n\n", player2secure[1], "has WON!!!")
        game = False #exits game
        new_leaderboard = Leaderboard(player2secure[1], P2_total, player1secure[1], P1_total) # updates the leaderboard by calling functions
        Leaderboard_update(new_leaderboard)
    elif P1_total == P2_total: # checks if the scores are equal
        print("\n\n" + "You both have the same score, so")
        P1_prompt2 = input(player1secure[1] + " Press enter to roll one more time:")
        extra_roll1 = extra_roll() #rolls again for player 1
        print(player1secure[1], "rolled a", extra_roll1) # prints result
        P2_prompt2 = input(player2secure[1] + " Press enter to roll one more time:")
        extra_roll2 = extra_roll() # rolls again for player 2
        print(player2secure[1], "rolled a", extra_roll2) # prints result
        P1_total += extra_roll1 # adds the extra rolls to the totals
        P2_total += extra_roll2
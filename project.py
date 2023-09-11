# Libraries
from cmu_graphics import * # cmu_graphics by Carnegie Mellon University, used for graphics. Source: https://academy.cs.cmu.edu/desktop
import random # Built-in Python module that generates pseudo-random values. Source: https://docs.python.org/3/library/random.html
import time # Built-in Python module that handles time functions. Source: https://docs.python.org/3/library/time.html
app.stepsPerSecond = 60 # FPS limiter

# Menu text
Label("ClickTest", 200, 200, size=80)
Label("Click rapidly", 200, 350, size=40)
counter = Label(0, 200, 275, size=40)

# Create labels for displaying the first and second scores
scoreLabel1 = Label("", 100, 50, size=20)
scoreLabel2 = Label("", 300, 50, size=20)
scoreDifference = Label("", 200, 100, size=20)
hiScoreText = Label("", 120, 25, size=20)
hiDiffText = Label("", 320, 25, size=20)

clicInc = 0 # Click incrementer. Goes up every mouse click

startCheck = 0 # If first start is done
indicator = Label(clicInc, 380, 380) # The amount of clicks a user has registered total within an interval

roundStart = Rect(0, 20, 40, 40, fill='white') # Explained in countClicks()

scoreBoardScore = [0, 0, 0, 0] # The index that holds score values. From left to right: Round 1 score, Round 2 score, Highest Difference, Highest Score

roundEnd = False # Stops mouse clicks after the end of the second iteration, requiring a keypress to restart.

def countClicks():
    global startCheck, clicInc, startTime, roundEnd # Globals from above
    while True:

        # The yield variable below is called to essentially 'pause' the code until a given input is registered and provides a value.
        # Without this, the counter will go infinitely without any input.
        # Information source: https://docs.python.org/3.10/tutorial/classes.html#generators

        mouseX, mouseY = yield
        if roundEnd: # If the round is completed
            continue # Skips while statement and 'deactivates' countClicks() until it receives newRound()
        startCheck += 1
        indicator.value = clicInc
        clicInc += 1
        if startCheck == 1: # If the game has started
            startTime = time.time() # Start the timer on the first click
        elapsedTime = time.time() - startTime # Calculate the time elapsed to be displayed in the line below
        counter.value = int(elapsedTime) # Update the counter label with the elapsed time in seconds

        # This code segment draws a square that shows the beginning of the new round. It turns white after 6 clicks.
        
        if clicInc <= 5: # check if clicInc (how many times one clicks) is 5 or less
            roundStart.fill = 'green'
        else:
            roundStart.fill = 'white'

        if elapsedTime >= 3: # If the round exceeds the alloted time
            if scoreBoardScore[0] == 0: # If the first index equals 0 after the interval ends
                scoreBoardScore[0] = clicInc # Save the first half's click score
                scoreLabel1.value = "Score 1: " + str(scoreBoardScore[0]) # Print score
                print("Scoreboard score:", scoreBoardScore[0]) # Debug
                clicInc = 0 # Reset
                counter.value = 0 # Reset
                indicator.value = 0 # Reset
                startCheck = 0 # Reset
            else: # Otherwise save the second half's data and finalize scores
                scoreBoardScore[1] = clicInc # Save the second half's click score
                scoreLabel2.value = "Score 2: " + str(scoreBoardScore[1]) # Print second half's click score
                print("Scoreboard score:", scoreBoardScore[0], scoreBoardScore[1]) # Debug
                scoreDifference.value = "Difference: " + str(scoreBoardScore[1] - scoreBoardScore[0]) # Calculate the difference between the two halves' click amount
                difference = scoreBoardScore[1] - scoreBoardScore[0] # Because it is difficult to use scoreDifference value since it has text, redo the math and save it in the dedicated var
                if difference > scoreBoardScore[2]: # Check if the new difference is higher than the current highest
                    scoreBoardScore[2] = difference # Update the highest difference if the score is beaten
                    hiDiffText.value = "Largest Diff: " + str(scoreBoardScore[2]) # Print the highest score saved in the list
                if scoreBoardScore[1] > scoreBoardScore[3]: # Check if the new score is higher than the current highest
                    scoreBoardScore[3] = scoreBoardScore[1] # Update the highest score if the score is beaten
                    hiScoreText.value = "High Score: " + str(scoreBoardScore[3]) # Print the difference saved in the list
                roundEnd = True 

# Code to restart the round
def resetGameState(): # This entirely resets the game statistics, apart from the high scores.
    global startCheck, clicInc, counter, indicator, roundStart, scoreBoardScore, scoreLabel1, scoreLabel2, scoreDifference, roundEnd # Globals
    clicInc = 0
    startCheck = 0
    counter.value = 0
    indicator.value = 0
    roundStart.fill = 'white'
    scoreBoardScore[0] = 0 # Resets round 1 score
    scoreBoardScore[1] = 0 # Resets round 2 score
    scoreLabel1.value = "" 
    scoreLabel2.value = ""
    scoreDifference.value = ""
    roundEnd = False

# Finishing generator variable
stateUpdate = countClicks() # Initializer. stateUpdate holds the generator variable
next(stateUpdate)

# On mouse press do this. This will make mouse inputs be the input for the stateUpdate generator
def onMousePress(mouseX, mouseY):
    stateUpdate.send((mouseX, mouseY))

def newRound(): # This will rerun countClicks
    global stateUpdate
    stateUpdate = countClicks()
    next(stateUpdate) # Starts generator

def onKeyPress(key): # When X is pressed, reset stats and game
    if key == 'x':
        resetGameState()
        newRound()

cmu_graphics.run() # Run CMU Graphics library

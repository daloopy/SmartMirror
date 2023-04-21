import os
import webbrowser

def main():
    # check flag - a user has been created 
    userCreated = os.path.exists("home/team17/flag")

    # if it has:
    if(userCreated):
        open_spotify() # open spotify on chromium
        os.system("python3 home/team17/Documents/SmartMirror/GUI/screenmanager.py")

    # if it hasnt:
    else:
        os.system("mkdir home/team17/flag") # set flag
        os.system("python3 home/team17/Documents/SmartMirror/GUI/startup.py")
        open_spotify() # start spotify on chrome
        os.system("python3 home/team17/Documents/SmartMirror/GUI/screenmanager.py")
        

def open_spotify():
    path = "home/team17/Local/Chromium/Application/chrome.exe" # TO-DO: fix path **********
    chrome = webbrowser.get('{} %s'.format(path))
    chrome.open_new("https://www.spotify.com")

main()

# What will need fixing:
# any paths used here are from memory or a guess







# What this does: 
# Function that will run every time the Pi is powered on.

# If it is powered on for the first time, it creates the user profile. 
# this is startup.py
# If the user profile is already set up, skip this step ^

# Next, start the Spotify browser
# open it in chrome

# Last, start the GUI.
# this is done w/ screenmanager.py

#os.system spawns a new process and waits; exit code is returned





# What i used for testing:
# userCreated = os.path.exists("flag")
# os.system("python3 screenmanager.py")
# os.system("mkdir flag") # set flag
# os.system("python3 startup.py")
# os.system("python3 screenmanager.py")
# path = "Applications/Google Chrome.app/chrome.exe"
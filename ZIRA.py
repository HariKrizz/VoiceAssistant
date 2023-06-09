from gtts import gTTS

import datetime
import os
import pyttsx3
import random
import smtplib
import speech_recognition as sr
import warnings
import webbrowser
import wikipedia

warnings.filterwarnings('ignore')

# Zira Voice

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Audio Outputs
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


print('Initiating ZIRA...')
speak('Initiating ZIRA...')

print("Loading Modules and Functions...")
speak("Loading Modules and Functions...")


# Speech to Text --> Voice commands
def getCommand():
    rec = sr.Recognizer()
    rec.energy_threshold = 8000

    with sr.Microphone() as source:
        print('Listening...')
        rec.pause_threshold = 0.5
        audio = rec.listen(source)
    try:
        print('Recognizing commmand...')
        data = rec.recognize_google(audio).lower()
        print('You said: ', data)

    except Exception as e:
        print('Fetching error from service.', e)

        return 'None'
    return data


# Greet the user on start
def greetUser():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning Hari")

    elif hour >= 12 and hour <= 15:
        speak("Good Afternoon Hari")

    elif hour >= 15 and hour <= 23:
        speak("Good Evening Hari")

    else:
        speak("It's almost midnight,you should get some sleep.")
    speak("Hello,I'm ZIRA. How can I help you?")


# Functions for Zira

def bluetooth():
    print('btWaiting...')


def browseNet():
    print('netWaiting...')


def codeVS():
    print('vsWaiting...')


def current_Date():
    print('dateWaiting...')


def current_Time():
    print('timeWaiting...')


def exitZira():
    print('ziraWaiting...')


def playMusic():
    print('playmusicWaiting...')


def playNext():
    print('playnextWaiting...')


def sendMail():
    print('mailWaiting...')

 
def searchWiki():
    print('wikiWaiting...')


def youtube():
    print('youtubeWaiting...')


# Zira Command Dictionary
cmd_dict = {'bluetooth': bluetooth(), 'search': browseNet(), 'code': codeVS, 'date': current_Date,
            'exit': exitZira, 'song': playMusic, 'next': playNext, 'mail': sendMail, 'time': current_Time,
            'wiki': searchWiki, 'open youtube': youtube
        }

# Main starting of execution
if __name__ == "__main__":

    # greetUser()
    userCommand = getCommand().lower()

    while True:

        for userCommand in cmd_dict.keys():
            val = cmd_dict.get(userCommand)()
            val.clear
            print(str(val))
                
        else:
            print('Try again')
            getCommand()
'''
Use the Interactive Window to develop Python Scripts
- You can create cells on a Python file by typing "#%%" 
- Use "Shift + Enter " to run a cell, the output will be shown in the interactive window
'''
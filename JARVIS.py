import json
from gtts import gTTS

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import bluetooth
import datetime
from py_dotenv import read_dotenv
import os
import pyaudio
import pyttsx3
import random
import screen_brightness_control as sbc
import smtplib
import speech_recognition as sr
import spotipy
import warnings
import webbrowser
import wikipedia

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)
# Ignoring warning Message
warnings.filterwarnings('ignore') 

# Functions for JARVIS
cmd = ('wiki', 'firefox', 'open code', 'open email', 'time', 'date', 'sleep', 'youtube', 'bluetooth')
# music = ('play music', 'next song', 'stop music')
music = ('play music')
sys_ctrl = ('volume up', 'volume down', 'bright up', 'bright down')
power = ('shutdown', 'restart', 'lock')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function for audio Outputs
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

print('Initiating...')
speak('Initiating...')

speak("Starting Processes...")


# Date and Time
def today_date():
    current_date = datetime.datetime.today().strftime('%A, %d %B %Y')
    print('Today is', current_date)
    speak("Today is" + current_date)

#  Current Time
def present_time():
    # time.strftime('%I:%M %p',time.localtime())
    current_Time = datetime.datetime.now().strftime('%I %M %S')
    print('The Time is', current_Time)
    speak("The time is" + current_Time)

 
# Function for Wishing by Time
def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning Hari")
        today_date()
        present_time()

    elif hour >= 12 and hour <= 15:
        speak("Good Afternoon Hari")
        today_date()
        present_time()

    elif hour >= 15 and hour <= 23:
        speak("Good Evening Hari")
        today_date()
        present_time()

    else:
        present_time()
        speak("It's almost midnight sir, you should get some sleep.")
    speak("I'm your assistant JARVIS. How can I help you?")


# Take Microphone commands and reply in string output
def takeCommand():
    rec = sr.Recognizer()
    rec.energy_threshold = 8000

    with sr.Microphone(device_index=None) as source:

        print('Listening...')
        rec.pause_threshold = 0.5
        audio = rec.listen(source)
    try:
        print('Recognizing commmand...')
        data = rec.recognize_google(audio, language='en-US')
        print('You said: ', data)

    except Exception as e:
        print('Fetching error from service.', e)
        return 'None'
    return data

# Send Email
def sendMail(to_address, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('email@example.com', 'password')
    server.sendmail('email@example.com', to_address, content)
    server.close()

# Browse Internet
def searchNet(site_addr, search):
    try:
        url = site_addr + search
        print(url)
        webbrowser.open(url)
    except:
        speak("Unexpected Error Occured")

# Search for near-by Bluetooth Devices
def searchBluetooth():
    print("Looking for nearby devices...")
    speak("Looking for nearby devices...")

    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print('Found %d Devices' % len(nearby_devices))
    speak('Found %d Devices' % len(nearby_devices))

    for addr, names in nearby_devices:
        print('%s - %s' % (names, addr))

        for services in bluetooth.find_service(address=addr):
            print('Device Name: %s' % (services[names]))
            print('Description: %s' % (services["description"]))
            print('Protocol: %s' % (services["protocol"]))
            print('Provider: %s' % (services["provider"]))
            print('Port: %s' % (services["port"]))
            print('Service id: %s' % (services["service-id"]))

# Get the Default Audio Devices and Volume using Pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
currentVolume = volume.GetMasterVolumeLevel()

# # Play Music
# def playMusic():
#     music_dir = 'F:\\♫Songs♫'
#     songs = os.listdir(music_dir)
#     chosen = random.randint(0, songs.__len__())
#     os.startfile(os.path.join(music_dir, songs[chosen]))
# # Close Music Player
# def closeMusic():
#     os.system('TASKKILL /F /IM  Groove Music')

def openSpotifyMusic():
    # username = os.environ('USERNAME')
    clientID = os.environ['SPOTIPY_CLIENT_ID']
    clientSecret = os.environ['SPOTIPY_CLIENT_SECRET']
    redirect_uri = os.environ['REDIRECT_URI']
    print(clientID, clientSecret, redirect_uri)
    
    oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri)
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)
    user_name = spotifyObject.current_user()

    # To print the response in readable format.
    print(json.dumps(user_name, sort_keys=True, indent=4))

    while True:
        print("Hello" + user_name['display_name'])
        search_song = input("Enter the Song name: ")
        results = spotifyObject.search(search_song, 1, 0, "track")
        songs_dict = results['tracks']
        song_items = songs_dict['items']
        song = song_items[0]['external_urls']['spotify']
        webbrowser.open(song)
        print('Song has opened in your browser.')
       
# Close JARVIS
def terminate():
    print('Hibernating JARVIS.. See you next time.')
    speak("Hibernating JARVIS.. See you next time.")
    exit()

if __name__ == "__main__":
    wishMe()
    while True:
        command = takeCommand().lower()

        # Executing commands as per voice command
        if cmd[0] in command:
            try:
                
                speak("Searching in Wikipedia.")
                command = command.replace(wikipedia.summary(command), '')
                result = wikipedia.summary(command, sentences=2)
                speak("According to Wikipedia,")
            except Exception as e:
                print(e)
                takeCommand()
            print(result)
            speak(result)

        elif cmd[1] in command:
            speak("Opening EDGE")
            site_addr = 'https://www.duckduckgo.com/'
            speak("What should I search for?")
            search = takeCommand()
            searchNet(site_addr, search)

        elif cmd[2] in command:
            speak("Opening Visual Studio Code.")
            codePath = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif cmd[3] in command: 
            try:
                speak("Opening your Gmail..")
                speak("Tell me the message content now.")

                to_address = 'harilr1001@gmail.com'

                content = takeCommand()
                sendMail(to_address, content)

                speak("The e-mail has been sent.")
            except Exception as e:
                speak("Sorry, The E-mail could not be sent at the moment.")
                print(e)
                takeCommand()

        elif cmd[4] in command:
            present_time()

        elif cmd[5] in command:
            today_date()
        
        elif cmd[6] in command:
            terminate()

        elif cmd[7] in command:
            webbrowser.open('youtube.com')

        elif cmd[8] in command:
            searchBluetooth()

        elif power[0] in command:
            speak("Preparing for System shutdown...")
            os.system("shutdown /s")

        elif power[1] in command:
            speak("Preparing for System Restart...")
            os.system("shutdown /r")

        elif power[2] in command:
            speak("Preparing for Log-off...")
            os.system("shutdown /l")

        elif music[0] in command:
            speak("Opening Spotify. Please wait.")
            openSpotifyMusic()

        elif music[1] in command:
            speak("Changing Track")
            openSpotifyMusic()

        elif music[2] in command:
            print("Closing Groove Music..")
            closeMusic()

        elif sys_ctrl[0] in command:
            print("Increasing System Volume")
            volume.SetMasterVolumeLevel(currentVolume + 3.0, None)
            print('New Volume:' + str(currentVolume))

        elif sys_ctrl[1] in command:
            print("Reducing System Volume")
            volume.SetMasterVolumeLevel(currentVolume - 3.0, None)
            print('New Volume:' + str(currentVolume))

        elif sys_ctrl[2] in command:
            bright = sbc.get_brightness()

            new_bright = bright + 10
            print("Current Brightness Level:" + str(bright))
            sbc.set_brightness(new_bright)
            monitors = sbc.list_monitors()
            print(monitors)
        elif sys_ctrl[3] in command:
            bright = sbc.get_brightness()
            new_bright = bright - 10
            print("Current Brightness Level:" + str(bright))
            sbc.set_brightness(new_bright)
            
        else:
            print("Nothing Found!")

# The commented line will open url in a new tab
# webbrowser.get('firefox').open_new_tab('http://www.csestack.org')    2021F10081808vcx

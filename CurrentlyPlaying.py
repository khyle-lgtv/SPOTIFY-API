import os # A python module that imports OS functions to the program.
import spotipy # A python library that utilize the Spotify Web API.
import requests # A python module that enables the program to do HTTP requests.
import tkinter as tk # A python library that allow GUI functions to the program.
from dotenv import load_dotenv # A python library that enables the program to load environment variables.
from spotipy.oauth2 import SpotifyOAuth # This module handles the authentication of the Spotify using OAuth 2.0.
from PIL import Image, ImageTk # A python library that makes the program supports image.
from io import BytesIO # A module that allows file related input-output. BytesIO talks about the memory of the file.

load_dotenv() # A code that loads the environmental variable save on the device.
CLIENT_ID = os.getenv("MY_CLIENT_ID") # It is the unique id of the application in Spotify Web API.
CLIENT_SECRET = os.getenv("MY_CLIENT_SECRET") # It is a confidential id that are used to authenticate the requests when making requests to the Spotify API.
REDIRECT_URI = os.getenv("MY_REDIRECT_URI") # After the login authentication this is the destination.
SCOPE = "user-read-currently-playing" # This is the current scope of the program.

SP = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)) # The programs Authentication Code flow.

def CurrentlyPlayingInformation(): # A function where it process all the programs functions.
    CurrentTrack = SP.currently_playing() # Gets the currently playing track and calls the function "SP" to get the details.
    if CurrentTrack and CurrentTrack['item']: # A conditional where it runs if there is a track playing on spotify account, the [item] is where all the details contain and it is in dictionary form.
        TrackName = CurrentTrack['item']['name'] # Gets the song name.
        TrackArtist = CurrentTrack['item']['artists'][0]['name'] # Gets the artist name, the index [0] indicates that the first name on the list is get.
        TrackCover = CurrentTrack['item']['album']['images'][0]['url'] # Gets the album cover of the track.

        TrackStatus = "PLAYING" if CurrentTrack['is_playing'] else "PAUSED" # A ternary operator that tells if the current track is playing or paused.
        
        response = requests.get(TrackCover) # Sends an HTTP GET request to download the album cover image.
        img_data = BytesIO(response.content) # Stores the image in memory as a byte stream, BytesIO enables this.
        img = Image.open(img_data) # Open image using PIL.
        img = img.resize((400, 400)) # A size of the image
        img_tk = ImageTk.PhotoImage(img) # Converts the PIL image to tkinter supported format.
        TrackCoverLabel.config(image=img_tk) # A tkinter method that configures a placeholder with the image it gets, it change depends on the track.
        TrackCoverLabel.image = img_tk # It makes the Tkinter to keep a reference, it makes the image to show.

        TrackProgress = CurrentTrack['progress_ms'] // 1000 # Get the track's current progress and converts it to seconds since it is in milliseconds form.

        mins, secs = divmod(TrackProgress, 60) # Split the total seconds using "divmod".
        TrackDuration = f"Duration: {mins:02}:{secs:02}" # Formats the duration to make it readable.

        CurrentlyPlaying = f"{TrackName}\nby {TrackArtist}\n{TrackDuration}\nStatus: {TrackStatus}" # Using f string, CurrentlyPlaying is a variable that gets the previous variables to make it display the track information.
        CurrentTrackLabel.config(text=CurrentlyPlaying) # A tkinter method that configures a content depending on the current track.

        CGUI.after(1000, CurrentlyPlayingInformation) # Calls the function every 1 seconds to refresh the display.
    else: # A statement the contains functions if nothing is playing.
        CurrentTrackLabel.config(text="No track...") # A tkinter method that configures a content depending on the current track.
        CGUI.after(1000, CurrentlyPlayingInformation) # Calls the function every 1 seconds to refresh the display.

CGUI = tk.Tk() # This is the root window of the programs GUI.
CGUI.title("CURRENTLY PLAYING") # A title that are located on the top-left corner of the window.
CGUI.geometry('1200x700') # The window's size
CGUI.config(background="black") # A configuration that change the background to black.

CGUILabel = tk.Label(CGUI, text="Currently Playing", font=("fixedsys", 32), background="black", foreground="green2") # A label placed inside of the window that comes with the configuration like the font color, size, and font.
CGUILabel.pack() # A code that makes the label be displayed and placed. Default is the center.

TrackCoverLabel = tk.Label(CGUI) # A label that displays the album cover of the track.
TrackCoverLabel.pack(pady=20) # A code that makes the label be displayed and placed. Default is the center, "pady" means a size of insterval space on top and bottom.

CurrentTrackLabel = tk.Label(CGUI, text="No track...", font=("fixedsys", 32), background="black", foreground="green2") # A label that displays "No track..." if there is no current track playing.
CurrentTrackLabel.pack() # A code that makes the label be displayed and placed. Default is the center.

CurrentlyPlayingInformation() # Calling out a function so it displays when run.
CGUI.mainloop() # To enable the GUI window to display.
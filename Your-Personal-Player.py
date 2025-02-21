import os # A python module that imports OS functions to the program.
import spotipy # A python library that utilize the Spotify Web API.
import requests # A python module that enables the program to do HTTP requests.
import tkinter as tk # A python library that allow GUI functions to the program.
import threading # A library that allows some functions to run independently and not intercept other function running.
import queue # A module that allows queue of object in the program.
from dotenv import load_dotenv # A python library that enables the program to load environment variables.
from spotipy.oauth2 import SpotifyOAuth # This module handles the authentication of the Spotify using OAuth 2.0.
from PIL import Image, ImageTk # A python library that makes the program supports image.
from io import BytesIO # A module that allows file related input-output. BytesIO talks about the memory of the file.

load_dotenv() # A code that loads the environmental variable save on the device.
CLIENT_ID = os.getenv("MY_CLIENT_ID") # It is the unique id of the application in Spotify Web API.
CLIENT_SECRET = os.getenv("MY_CLIENT_SECRET") # It is a confidential id that are used to authenticate the requests when making request to the Spotify API.
REDIRECT_URI = os.getenv("MY_REDIRECT_URI") # After the login authentication this is the destination.
SCOPE = "user-read-currently-playing user-modify-playback-state user-read-playback-state" # This is the scope of the program.

SP = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)) # The programs Authentication Code flow.
YPP_QUEUE = queue.Queue() # Initializes the FIFO queue in this program.

def PreviousTrack(): # A function that makes the program to go back from the previous track.
    threading.Thread(target=SP.previous_track, daemon=True).start() # A method that makes the program to previous track.

def threadingPlayback(): # A function for making the Playback track to work independently.
     threading.Thread(target=PlaybackTrack, daemon=True).start()

def PlaybackTrack(): # A function that contain play and pause.
    CurrentTrack = SP.currently_playing() #  Gets the currently playing track and calls the object "SP" to get the details.
    if CurrentTrack and CurrentTrack['is_playing']: # A statement that checks if the track is playing on the spotify account.
            SP.pause_playback() # A method that makes the program to pause the track.
    else: # A statement that if the track is paused.
            SP.start_playback() # Play the track.

def NextTrack(): # A function that makes the program to proceed to next track.
    threading.Thread(target=SP.next_track, daemon=True).start() # A method that go to the next track.

def TrackInfo(): # A function that displays the tracks information.
    while True:
        CurrentTrack = SP.currently_playing() # Gets the currently playing track and calls the object "SP" to get the details.
        if CurrentTrack and CurrentTrack['item']: # A conditional where it runs if there is a track playing on spotify account, the [item] is where all the details contain and it is in dictionary form.
            TrackName = CurrentTrack['item']['name'] # Gets the song name.
            TrackArtist = CurrentTrack['item']['artists'][0]['name'] # Gets the artist name, the index [0] indicates that the first artist on the list is get.
            TrackCover = CurrentTrack['item']['album']['images'][0]['url'] # Gets the album cover of the track.
            TrackStatus = "PLAYING" if CurrentTrack['is_playing'] else "PAUSED" # A ternary operator that tells if the current track is playing or paused.
            
            response = requests.get(TrackCover) # Sends an HTTP GET request to download the album cover image.
            img_data = BytesIO(response.content) # Stores the image in memory as a byte stream, BytesIO enables this.
            img = Image.open(img_data).resize((400, 400)) # Open image using PIL, and resize it.
            img_tk = ImageTk.PhotoImage(img) # Converts the PIL image to tkinter supported format.
            TrackCoverLabel.config(image=img_tk) # A tkinter method that configures a placeholder with the image it gets, it change depends on the track.
            TrackCoverLabel.image = img_tk # It makes the Tkinter to keep a reference, it makes the image to show.
            
            DurationMS = CurrentTrack['progress_ms'] // 1000 # Get the track's current progress and converts it to seconds since it is in milliseconds form.
            DurationMins, DurationSecs = divmod(DurationMS, 60) # For the real-time counting of tracks progress.
            TrackDuration = f"Duration - {DurationMins:02}:{DurationSecs:02}" # Formats the duration to make it readable.
            
            CurrentlyPlaying = f"{TrackName}\nby {TrackArtist}\n{TrackDuration}\nStatus: {TrackStatus}" # Using f string, CurrentlyPlaying is a variable that gets the previous variables to make it display the track information.
            YPP_QUEUE.put((img_tk, CurrentlyPlaying)) # A tkinter method that configures a content depending on the current track.
        else: # A statement the contains functions if nothing is playing.
            YPP_QUEUE.put((None, "No track...")) # If nothing is playing then this displays.
            
        threading.Event().wait(1) # Calls the function every 1 seconds to refresh the display.

def GUIUpdate(): # A function for updating the tkinter image and text.
    try:
        img_tk, text = YPP_QUEUE.get_nowait() # Retrieves an item without waiting whats comes next on the queue.
        if img_tk: # Run if an item is on queue.
            TrackCoverLabel.config(image=img_tk)
            TrackCoverLabel.image = img_tk
        CurrentTrackLabel.config(text=text)
    except queue.Empty: # An exception that if there is no item on the queue, it will just pass.
        pass

    YPP.after(1000, GUIUpdate) # Updates every 1 s.

YPP = tk.Tk() # This is the root window of the programs GUI.
YPP.title("Your Personal Player") # A title that are located on the top-left corner of the window.
YPP.geometry('900x800') # The window's size.
YPP.config(background="black") # A configuration that change the background to black.

Label = tk.Label(YPP, text="Your Personal Player", font=("fixedsys", 18), background="black", foreground="green2") # A label placed inside of the window that comes with the configuration like the font color, size, and font.
Label.pack() # A code that makes the label be displayed and placed. Default is the center.

TrackCoverLabel = tk.Label(YPP) # A label that displays the album cover of the track.
TrackCoverLabel.pack(pady=10) # A code that makes the label be displayed and placed. Default is the center, "pady" means a size of insterval space on top and bottom.

CurrentTrackLabel = tk.Label(YPP, text="No track...", font=("fixedsys", 18), background="black", foreground="green2") # A label that displays "No track..." if there is no current track playing.
CurrentTrackLabel.pack(pady=10) # A code that makes the label be displayed and placed. Default is the center.

PreviousBtn = tk.Button(YPP, text="<", font=("fixedsys", 18), background="black", foreground="green2", activebackground="green2", activeforeground="black", command=PreviousTrack) # A button for the previous track.
PreviousBtn.place(relx=0.4, rely=0.9, anchor="w") # To specify the placement of the button.

PlaybackBtn = tk.Button(YPP, text="PLAY", font=("fixedsys", 18), background="black", foreground="green2", activebackground="green2", activeforeground="black", command=threadingPlayback) # A button for the pause and play.
PlaybackBtn.place(relx=0.5, rely=0.9, anchor="c") # To specify the placement of the button.

NextBtn = tk.Button(YPP, text=">", font=("fixedsys", 18), background="black", foreground="green2", activebackground="green2", activeforeground="black", command=NextTrack) # A button for the next track.
NextBtn.place(relx=0.6, rely=0.9, anchor="e") # To specify the placement of the button.

threading.Thread(target=TrackInfo, daemon=True).start() # A threading for the track info function.

GUIUpdate() # Calls out the function.
YPP.mainloop() # To enable the GUI window to display.
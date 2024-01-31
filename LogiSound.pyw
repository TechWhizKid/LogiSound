from tkinter import messagebox
from win32 import win32gui
import tkinter as tk
import os
import tarfile
import configparser
import ast
import pygame
import win32con


root = tk.Tk()  # Create a root window
root.withdraw() # Hide the root window


def files_to_remove(files_list):              # Function to remove files from provided list
    for file in files_list:
        if os.path.exists(file):              # Check if file exists before trying to remove
            os.remove(file)


if not os.path.exists("LogiSound.dat"):       # Check if file "LogiSound.dat" exists
    messagebox.showerror("Error", "File \"LogiSound.dat\" not found\nThis file is needed for the app to work.")
    os._exit(0)


if tarfile.is_tarfile("LogiSound.dat"):       # Check if the file "LogiSound.dat" is valid or not
    data = tarfile.open("LogiSound.dat", "r") # Open the tar file in read mode
    if "config.ini" in data.getnames():       # Check if LogiSound.dat contains config.ini
        FILES_IN_DAT = data.getnames()        # Get a list of all files in the tar file
        data.extractall()                     # Extract all the files
        data.close()                          # Close the tar file
    else:
        messagebox.showerror("Error", "Config data not found in file \"LogiSound.dat\".")
        os._exit(0)
else:
    messagebox.showerror("Error", "File \"LogiSound.dat\" is not a valid data file to be used with this app.")
    os._exit(0)


# Check if extraction failed
if not os.path.exists("config.ini"):
    messagebox.showerror("Error", "Error: Not permitted to read from or write to this folder.")
    os._exit(0)
else:
    config = configparser.ConfigParser()   # Initialize configparser
    config.read("config.ini")              # Read the config file


if config.has_section("LogiSound_Config"): # check if the LogiSound_Config section exists
    required_options = ["REQUIRED", "IMAGE_FILE", "SOUND_FILE", "REPEAT_SOUND", "SOUND_VOLUME", "WINDOW_WIDTH", "WINDOW_HEIGHT", "IMG_ROUNDNESS", "WIN_ROUNDNESS"]
    for option in required_options:        # check if all the required options exist
        if not config.has_option("LogiSound_Config", option):
            files_to_remove(FILES_IN_DAT)  # Remove extracted files
            messagebox.showerror("Error", "Incomplete or invalid data in file \"LogiSound.dat\".")
            os._exit(0)
    try:# Check if the config file has valid data
        # access the values from the LogiSound_Config section
        REQUIRED      = ast.literal_eval(config["LogiSound_Config"]["REQUIRED"])
        IMAGE_FILE    = str(config["LogiSound_Config"]["IMAGE_FILE"])
        SOUND_FILE    = str(config["LogiSound_Config"]["SOUND_FILE"])
        REPEAT_SOUND  = int(config["LogiSound_Config"]["REPEAT_SOUND"])
        SOUND_VOLUME  = bool(config["LogiSound_Config"]["SOUND_VOLUME"])
        WINDOW_WIDTH  = int(config["LogiSound_Config"]["WINDOW_WIDTH"])
        WINDOW_HEIGHT = int(config["LogiSound_Config"]["WINDOW_HEIGHT"])
        IMG_ROUNDNESS = int(config["LogiSound_Config"]["IMG_ROUNDNESS"])
        WIN_ROUNDNESS = int(config["LogiSound_Config"]["WIN_ROUNDNESS"])
    except:
        files_to_remove(FILES_IN_DAT)      # Remove extracted files
        messagebox.showerror("Error", "Invalid config data in file \"LogiSound.dat\".")
        os._exit(0)
else:
    files_to_remove(FILES_IN_DAT)          # Remove extracted files
    messagebox.showerror("Error", "Missing section \"LogiSound_Config\" in \"LogiSound.dat\" file which is required.")
    os._exit(0)


# Check if config.ini is misconfigured
if (IMAGE_FILE or SOUND_FILE) not in REQUIRED:
    files_to_remove(FILES_IN_DAT)          # Remove extracted files
    messagebox.showerror("Error", "Misconfigured config data found in file \"LogiSound.dat\".")
    os._exit(0)

# Check if all necessary files are present
for file in REQUIRED:
    if not os.path.exists(file):
        files_to_remove(FILES_IN_DAT)      # Remove extracted files
        messagebox.showerror("Error", "Incomplete or invalid data in file \"LogiSound.dat\".")
        os._exit(0)


pygame.init()                          # Initialize pygame
pygame.mixer.init()                    # Initialize pygame sound mixer


if pygame.image.get_extended():        # Check if pygame can load images of the given format
    try:                               # Invalid / corrupted file if it can't be loaded by pygame
        pygame.image.load(IMAGE_FILE)
    except pygame.error as e:          # If an error is raised, the file is incorrect
        files_to_remove(FILES_IN_DAT)  # Remove extracted files
        messagebox.showerror("Error", "Could not load image from file: \"LogiSound.dat\".\nData in the file might be corrupted.")
        os._exit(0)
else:                                  # Exit if pygame module doesn't supports the file type
    files_to_remove(FILES_IN_DAT)      # Remove extracted files
    messagebox.showerror("Error", f"Unsupported image format in the data file: \"LogiSound.dat\".")
    os._exit(0)


# Check if the sound file is valid and is supported
if pygame.mixer.get_init():            # Check if the mixer is initialized
    try:                               # Try to load the sound file
        test_sound = pygame.mixer.music.load(SOUND_FILE)
        pygame.mixer.music.unload()    # Unload the test sound file
    except:                            # If an error is raised, the file is invalid or unsupported
        files_to_remove(FILES_IN_DAT)  # Remove extracted files
        messagebox.showerror("Error", "Could not load sound from file: \"LogiSound.dat\".\nData in the file might be unsupported or corrupted.")
        os._exit(0)
else:                                  # If the mixer is not initialized, the file cannot be checked
    files_to_remove(FILES_IN_DAT)      # Remove extracted files
    messagebox.showerror("Error", "The mixer is not initialized.\nThis is an internal application error, please report this error.")
    os._exit(0)


SCREEN_INFO = pygame.display.Info()    # Get the display information
SCREEN_WIDTH = SCREEN_INFO.current_w   # Set screen width
SCREEN_HEIGHT = SCREEN_INFO.current_h  # Set screen height

# Calculate the center position of the window
CENTER_X = SCREEN_WIDTH // 2 - WINDOW_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2 - WINDOW_HEIGHT // 2


WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME) # Create a frameless window
WINDOW_ICON = pygame.image.load(IMAGE_FILE)                                     # Load icon for the window
pygame.display.set_icon(WINDOW_ICON)                                            # Set the loaded icon as appicon


# Load and scale the background image
BG_IMAGE = pygame.transform.scale(pygame.image.load(IMAGE_FILE), (WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.mixer.music.load(SOUND_FILE)         # Load the background music
pygame.mixer.music.set_volume(SOUND_VOLUME) # Set volume for the bg music
pygame.mixer.music.play(REPEAT_SOUND)       # Set the value for repeating sound


# Create a surface with alpha channel and draw a rounded rectangle on it
rect_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
pygame.draw.rect(rect_image, (255, 255, 255), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), border_radius=IMG_ROUNDNESS)

# Get the window handle and create a region with rounded corners
window_handle = pygame.display.get_wm_info()['window']
region = win32gui.CreateRoundRectRgn(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, WIN_ROUNDNESS, WIN_ROUNDNESS)

# Set the window region and position
win32gui.SetWindowRgn(window_handle, region, True)
win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 100, 100, WINDOW_WIDTH, WINDOW_HEIGHT, win32con.SWP_SHOWWINDOW)
win32gui.MoveWindow(window_handle, CENTER_X, CENTER_Y, WINDOW_WIDTH, WINDOW_HEIGHT, True)


# Start the mainloop
running = True
while running and pygame.mixer.music.get_busy():
    WINDOW.fill((0, 0, 0))              # Fill the window with black color
    # Blend the background image with the rounded rectangle surface
    BG_IMAGE.blit(rect_image, (0, 0), None, pygame.BLEND_RGBA_MIN)
    WINDOW.blit(BG_IMAGE, (0, 0))       # Blit the blended image onto the window
    for event in pygame.event.get():    # Handle the events
        if event.type == pygame.QUIT:
            running = False             # If the user closes the window, stop the loop
    pygame.display.update()             # Update the display


pygame.mixer.music.unload()             # Unload the sound file
for file in FILES_IN_DAT:               # Loop through the file names
    if os.path.exists(file):            # Check if the file exists
        os.remove(file)                 # Remove the file

pygame.quit() # Quit pygame window


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow for working with images
import requests
import os
import zipfile
import tempfile
import ctypes

if not ctypes.windll.shell32.IsUserAnAdmin():
    print('Not enough priviledge, restarting...')
    import sys
    ctypes.windll.shell32.ShellExecuteW(
        None, 'runas', sys.executable, ' '.join(sys.argv), None, None)
    sys.exit()

else:
    print('Elevated privilege acquired')


owner = "Andre-cmd-rgb"
repo = "FlightWarGame"
asset_name = "game.zip"
target_dir = r"C:\Program Files\Game Launcher\Game"
#installed_version = "0.2.0"


version_file_path = os.path.join(target_dir, "version.txt")
if os.path.isfile(version_file_path):
    with open(version_file_path, "r") as version_file:
        installed_version = version_file.read().strip() 

# Your existing functions (download_and_extract_github_release, is_newest_version_installed, launch_game) go here
def download_and_extract_github_release(owner, repo, asset_name, target_dir):
    # Define the GitHub API URL for the releases of the repository
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    
    try:
        # Send a GET request to the GitHub API
        response = requests.get(api_url)
        response.raise_for_status()

        # Parse the JSON response to get the release information
        release_info = response.json()

        # Find the asset with the specified name 
        asset = next((a for a in release_info['assets'] if a['name'] == asset_name), None)

        if asset:
            # Get the download URL of the asset
            download_url = asset['browser_download_url']

            # Create a temporary directory to store the downloaded file
            with tempfile.TemporaryDirectory() as temp_dir:
                # Download the asset
                response = requests.get(download_url)
                response.raise_for_status()

                # Define the path to save the downloaded file
                download_path = os.path.join(temp_dir, asset_name)

                # Save the downloaded file
                with open(download_path, 'wb') as file:
                    file.write(response.content)

                # Extract the downloaded file (assuming it's a ZIP file)
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)

            print(f"Downloaded and extracted {asset_name} successfully to {target_dir}")
        else:
            print(f"Asset '{asset_name}' not found in the latest release")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def is_newest_version_installed(owner, repo, asset_name, installed_version):
    # Define the GitHub API URL for the releases of the repository
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

    try:
        # Send a GET request to the GitHub API
        response = requests.get(api_url)
        response.raise_for_status()

        # Parse the JSON response to get the release information
        release_info = response.json()

        # Get the tag name (version) of the latest release
        latest_version = release_info['tag_name']

        # Compare the installed version with the latest version
        if latest_version == installed_version:
            print(f"The newest version ({latest_version}) is already installed.")
            return True
        else:
            print(f"A newer version ({latest_version}) is available.")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False





def launchgame():
    import os
    if not is_newest_version_installed(owner, repo, asset_name, installed_version):
        download_and_extract_github_release(owner, repo, asset_name, target_dir)
    os.system(r'"C:\Program Files\Game Launcher\Game\fly1-test.exe"')
    
        
def update_launch_button():
    if is_newest_version_installed(owner, repo, asset_name, installed_version):
        launch_button.config(text="Launch", state=tk.NORMAL)
    else:
        launch_button.config(text="Update", state=tk.NORMAL)

# Function to create a round button
def create_round_button(parent, radius, text, command):
    button = tk.Button(parent, text=text, width=6*radius, height=radius, relief="flat", bg="white", fg="black", command=command)
    button.place(relx=0.5, rely=0.5, anchor="center")
    return button
# Create the main window
root = tk.Tk()
root.title("Game Launcher")
window_width = 800
window_height = 600
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)
# Load the background image
bg_image = Image.open(r"C:\Program Files\Game Launcher\assets\background.png")
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Create a frame to center the button
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Create a round button for launching or updating
launch_button = create_round_button(frame, 1, "Checking for updates...", launchgame)
launch_button.pack()  # Pack the button within the frame

# Update the button label during app startup
update_launch_button()

root.mainloop()
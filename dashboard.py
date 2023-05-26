import tkinter as tk
from tkinter import ttk, filedialog
import os
import json


def show_commit_preview():
    # Get user input for environment variables
    git_repo_path = entry_repo_path.get()
    git_name = entry_name.get()
    git_email = entry_email.get()

    # Set environment variables
    os.environ["GIT_REPO_PATH"] = git_repo_path
    os.environ["GIT_AUTHOR_NAME"] = git_name
    os.environ["GIT_COMMITTER_NAME"] = git_name
    os.environ["GIT_AUTHOR_EMAIL"] = git_email
    os.environ["GIT_COMMITTER_EMAIL"] = git_email

    # Run Git command to get commit log
    command = (
        f'git --git-dir={os.environ["GIT_REPO_PATH"]}\.git --work-tree={os.environ["GIT_REPO_PATH"]} '
        f'log --author="{os.environ["GIT_AUTHOR_NAME"]}" --since=midnight --pretty=format:"%s"'
    )
    log_output = os.popen(command).read()

    # Show commit preview in the preview box
    txt_preview.delete(1.0, tk.END)
    txt_preview.insert(tk.END, log_output)


# Function to handle button click and run commit log
def run_commit_log():
    # Get user input for environment variables
    git_repo_path = entry_repo_path.get()
    git_name = entry_name.get()
    git_email = entry_email.get()

    # Create a dictionary with the Git settings
    git_settings = {
        "git_repo_path": git_repo_path,
        "git_name": git_name,
        "git_email": git_email,
    }

    # Save Git settings to a JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(git_settings, json_file)

    # Set environment variables
    os.environ["GIT_REPO_PATH"] = git_repo_path
    os.environ["GIT_AUTHOR_NAME"] = git_name
    os.environ["GIT_COMMITTER_NAME"] = git_name
    os.environ["GIT_AUTHOR_EMAIL"] = git_email
    os.environ["GIT_COMMITTER_EMAIL"] = git_email

    # Set the log file path on the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    log_file = os.path.join(desktop_path, "daily_commit_log.txt")

    # Run Git command to get commit log
    command = (
        f'git --git-dir={os.environ["GIT_REPO_PATH"]}\.git --work-tree={os.environ["GIT_REPO_PATH"]} '
        f'log --author="{os.environ["GIT_AUTHOR_NAME"]}" --since=midnight --pretty=format:"%s"'
    )
    log_output = os.popen(command).read()

    # Split the log messages and add them to a list
    log_messages = []
    for message in log_output.split("\n"):
        # Check if the message contains a plus sign
        if (
            " " #skip message 
            not in message
        ):
            if "+" in message:
                # Split the message by the plus sign and add each part as a separate log message
                parts = message.split("+")
                for part in parts:
                    log_messages.append(f"- {part.strip()}.")
            else:
                # Add the message as a log message
                log_messages.append(f"- {message.strip()}.")

    # Write the log messages to the log file
    with open(log_file, "w") as file:
        file.write("\n".join(log_messages))

    # Print confirmation message
    lbl_result.config(text=f'Commit log saved to {log_file}')


# root window
root = tk.Tk()
root.geometry("340x340")
root.title("Git Log")
root.resizable(0, 0)

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)


# Path
lbl_repo_path = ttk.Label(root, text="Path:")
lbl_repo_path.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

entry_repo_path = ttk.Entry(root, width=40)
entry_repo_path.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

# Name
lbl_name = ttk.Label(root, text="Author Name:")
lbl_name.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

entry_name = ttk.Entry(root, width=40)
entry_name.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

# Email
lbl_email = ttk.Label(root, text="Email:")
lbl_email.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

entry_email = ttk.Entry(root, width=40)
entry_email.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

# Preview button
btn_preview = ttk.Button(root, text="Preview", command=show_commit_preview)
btn_preview.grid(column=0, row=3, sticky=tk.E, padx=5, pady=5)

# login button
login_button = ttk.Button(root, text="save", command=run_commit_log)
login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

# Create result label
lbl_result = ttk.Label(root, text="")
lbl_result.grid(columnspan=2, row=4, sticky=tk.EW, padx=5, pady=5)

# Preview 
txt_preview = tk.Text(root, height=10 ,width=40)
txt_preview.grid(columnspan=2, row=5, sticky=tk.E, padx=10, pady=5)


json_file_path = os.path.join(os.path.expanduser("~"), "git_settings.json")

# Check if the JSON file exists
if os.path.exists(json_file_path):
    # Load Git settings from the JSON file
    with open(json_file_path, "r") as json_file:
        git_settings = json.load(json_file)

    # Set initial values in entry fields
    entry_repo_path.insert(0, git_settings["git_repo_path"])
    entry_name.insert(0, git_settings["git_name"])
    entry_email.insert(0, git_settings["git_email"])
root.mainloop()

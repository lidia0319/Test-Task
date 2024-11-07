import os
import shutil
import time
import logging

# Configures the log file
logging.basicConfig(filename='sync_operations.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Defines the paths of the two folders
FOLDER1 = 'Source'
FOLDER2 = 'Replica'

# Function to synchronize folder1 with folder2
def synchronize_folders():
    # Synchronizes files from folder1 to folder2
    for root, _, files in os.walk(FOLDER1):
        for file in files:
            folder1_path = os.path.join(root, file)
            folder2_path = os.path.join(FOLDER2, os.path.relpath(folder1_path, FOLDER1))

            # Creates directories in folder2 if necessary
            os.makedirs(os.path.dirname(folder2_path), exist_ok=True)

            # If the file does not exist or is outdated in folder2, copies it
            if not os.path.exists(folder2_path) or os.path.getmtime(folder1_path) > os.path.getmtime(folder2_path):
                shutil.copy2(folder1_path, folder2_path)
                logging.info(f'File copied: {folder2_path}')
                print(f'File copied: {folder2_path}')

    # Removes files from folder2 that are not in folder1
    for root, _, files in os.walk(FOLDER2):
        for file in files:
            folder2_path = os.path.join(root, file)
            folder1_path = os.path.join(FOLDER1, os.path.relpath(folder2_path, FOLDER2))

            # If the file does not exist in folder1, deletes it from folder2
            if not os.path.exists(folder1_path):
                os.remove(folder2_path)
                logging.info(f'File removed: {folder2_path}')
                print(f'File removed: {folder2_path}')

# Continuously runs synchronization with a 2-second delay between runs
try:
    while True:
        synchronize_folders()
        time.sleep(2)  # 2-second delay
except KeyboardInterrupt:
    logging.info("Synchronization interrupted by user.")  # Log when the user interrupts the script
    print("Synchronization interrupted by user.")

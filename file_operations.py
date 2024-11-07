import os
import random
import datetime
import logging
import time

# Configures the log file
logging.basicConfig(filename='file_operations.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Defines the paths of the two folders
FOLDER1 = "Source"
FOLDER2 = "Replica"

# Ensures the folders exist (creates them if they do not exist)
os.makedirs(FOLDER1, exist_ok=True)
os.makedirs(FOLDER2, exist_ok=True)

# Functions for random operations
def create_file(folder):
    # Creates a new file with a random name in the specified folder
    file_name = f'file_{random.randint(1, 10000)}.txt'
    file_path = os.path.join(folder, file_name)
    with open(file_path, 'w') as file:
        content = f'Content created on {datetime.datetime.now()}'
        file.write(content)
    # current_time = datetime.datetime.now().strftime('%H:%M:%S')
    logging.info(f'File created: {file_path}')
    print(f'File created: {file_path}')

def modify_file(folder):
    # Modifies an existing file (appends new content)
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if files:
        chosen_file = random.choice(files)
        file_path = os.path.join(folder, chosen_file)
        with open(file_path, 'a') as file:
            content = f'\nModification made on {datetime.datetime.now()}'
            file.write(content)
        # current_time = datetime.datetime.now().strftime('%H:%M:%S')
        logging.info(f'File modified: {file_path}')
        print(f'File modified: {file_path}')
    else:
        logging.info(f'No file to modify in {folder}')
        print(f'No file to modify in {folder}')

def delete_file(folder):
    # Deletes a random file from the folder
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if files:
        chosen_file = random.choice(files)
        file_path = os.path.join(folder, chosen_file)
        os.remove(file_path)
        # current_time = datetime.datetime.now().strftime('%H:%M:%S')
        logging.info(f'File deleted: {file_path}')
        print(f'File deleted: {file_path}')
    else:
        logging.info(f'No file to delete in {folder}')
        print(f'No file to delete in {folder}')

# Main function to perform random operations
def random_operation():
    # Performs a random operation in one of the folders
    folder = random.choice([FOLDER1, FOLDER2])
    operation = random.choice([create_file, modify_file, delete_file])
    operation(folder)

# Continuously performs random operations with a 5-second delay between them
for _ in range(50):  # Defines the number of desired random operations
    random_operation()
    time.sleep(5)  # 5-second delay

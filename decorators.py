import sys
import time
import os
import itertools
import random
import string
from utils import Style
from functions import *


def lay_down():
    listx = ["ᛞ", "ᛞᚫ", "ᛞᚫᛉ", "ᛞᚫᛉᚵ", "ᛞᚫᛉᚵᛒ",
             "ᛞᚫᛉᚵᛒᛍ", "ᛞᚫᛉᚵᛒᛍᛣ", "ᛞᚫᛉᚵᛒᛍᛣᛤ", "ᛞᚫᛉᚵᛒᛍᛣᛤᛄ"]
    count = 0
    for c in listx:
        if count != len(listx):
            sys.stdout.write('\r' + c)
            time.sleep(0.0001)
            count += 1
    sys.stdout.flush()
    listy = ["ᛄ", "  ᛄ", "    ᛄ", "       ᛄ",
             "          ᛄ", "                                ᛄ"]
    count2 = 0
    for cc in itertools.cycle(listy):
        if count2 == len(listy):
            break
        else:
            sys.stdout.write('\r' + cc)
            time.sleep(0.1)
            count2 += 1
            sys.stdout.flush()


def initialization():
    listx = ["     ██ 39%", "     ███ 49%", "     ████ 76%", "     █████ 89%", "     ██████ 100%", "     ██████  INITIALIZATION          ", "     ██████  INITIALIZATION          ",
             "     ██████  INITIALIZATION          ", "     ██████  INITIALIZATION          ", "     ██████  INITIALIZATION          ", "     ██████  INITIALIZATION          ", "     ██████  INITIALIZATION          "]
    count = 0
    for c in listx:
        if count != len(listx):
            sys.stdout.write('\r' + c)
            time.sleep(0.05)
            count += 1
            sys.stdout.flush()


def simulation():
    time.sleep(0.5)
    #for char in Style.GREEN + "\n\n ***************************************** \n ":
    #    print(char, end="", flush=True)
    obj = Style.GREEN + """
                     _     _                           _        __            __    
                    | |   | |                         | |      / /            \ \ _ 
 __      _____  _ __| | __| |  _____  _____  ___ _   _| |_ ___| |_ __ ___   ___| (_)
 \ \ /\ / / _ \| '__| |/ _` | / _ \ \/ / _ \/ __| | | | __/ _ \ | '_ ` _ \ / _ \ |  
  \ V  V / (_) | |  | | (_| ||  __/>  <  __/ (__| |_| | ||  __/ | | | | | |  __/ |_ 
   \_/\_/ \___/|_|  |_|\__,_(_)___/_/\_\___|\___|\__,_|\__\___| |_| |_| |_|\___| ( )
                                                               \_\            /_/|/ 
                                                                                    
___________________________________________________________________________________________
.    .    *  .   .  .   .  *     .  .        . .   .     .  *   .     .  .   .    *   .   .
*  .    .    *  .     .         .    * .     .  *  .    .   .   *   . .    .    *   .  .
. *      .   .    .  .     .  *      .      .        .     .-o--.   .    *  .   .  . *   .
.  .        .     .     .      .    .     *      *   .   :O o O :      .       .      .
____   *   .    .      .   .           .  .   .      .    : O. Oo;    .       .           *
`. ````.---...___      .      *    .      .       .   * . `-.O-'  .     * .     .    * .
\_    ;   \`.-'```--..__.       .    .      * .     .       .     .        .  .  .  . 
,'_,-' _,-'             ``--._    .   *   .   .  .       .   *   .     .  .  . *   .    . .
-'  ,-'                       `-._ *     .       .   *  .           .    .     .      . 
    ,-'            _,-._            ,`-. .    .   .     .      .     *    .   .    .     *
    '--.     _ _.._`-.  `-._        |   `_   .      *  .    .   .     .        *   . .
        ;  ,' ' _  `._`._   `.      `,-''  `-.     .    .     .    .      .  .  .     *   
    ,-'   \    `;.   `. ;`   `._  _/\___     `.       .    *     .    . *  .    .    .  .
    \      \ ,  `-'    )        `':_  ; \      `. . *     .        .    .        .   .
    \    _; `       ,;               __;        `. .           .   .      .   .    .      .
    '-.;        __,  `   _,-'-.--'''  \-:        `.   *   .    .  .   *     .   .  . . *
        )`-..---'   `---''              \ `.        . .   .  .       . .  .    * .   .   . 
___________________________________________________________________________________________ \n""" + Style.RESET

    print(obj)
    #for char in obj:
    #    print(char, end="", flush=True)
    #    time.sleep(0.002)  # small typing effect

    total_steps = 69           # number of characters in the bar
    total_duration = 13.7      # total time in seconds for progress 0->100%
    step_delay = total_duration / total_steps
    refresh_rate = 0.02        # refresh speed (characters flicker)

    phrases = [ # same length for alignment
        "Adding 'You' and 'Me'    ",
        "Generating the Universe  ",
        "Adding Stars and Moons.. ",
        "Crafting the Narrative   "
    ]
    ascii_chars = string.ascii_letters + string.digits + string.punctuation

    progress = 0
    last_update = time.time()
    current_phrase = random.choice(phrases)  # pick phrase for this step

    while progress <= total_steps:
        now = time.time()
        # Increment progress every step_delay seconds
        if now - last_update >= step_delay:
            progress += 1
            last_update = now
            current_phrase = random.choice(phrases)  # update phrase only on progress step

        # --- Build bar ---
        # Only the filled portion flickers
        filled = ''.join(random.choice(ascii_chars) for _ in range(progress))
        empty = '-' * (total_steps - progress)
        bar = filled + empty
        percent = math.ceil(progress * 100 / total_steps)  # calculate once per step

        sys.stdout.write(f"\r{current_phrase} [{bar}] {percent}%          ") # add spaces to clear line
        sys.stdout.flush()

        # Refresh faster than progress increment for flicker effect
        time.sleep(refresh_rate)


    print("\n" + Style.GREEN + "world.execute(me);" + Style.RESET)

    os.system("cls")

def united():
    united1 = True
    objectCreated = True
    parameter = "INITIALIZED"
    NewWorld = True
    current = random.choice(["AC", "DC"])

    united = prettyPrint(f"united : {united1};, objectCreated : {objectCreated}, parameter : {parameter}, NewWorld : {NewWorld}, current : {current}")
    computed1 = prettyPrint(f"computed : {computed}")
    print(united, computed1)

def emotions_Enabled():
    prettyPrint(execution)
    prettyPrint(stimulation)
    prettyPrint(satisfaction)
    prettyPrint(happiness)
    print(">>> EMOTIONS ENABLED")

def imtrapped(): # fallback function
    trapped = """Status : --- LOG ---,"I'm" entity trapped : True;, Simulation_status : ENABLED;"""
    prettyPrint(trapped)

def entityTrapped(): # improved function fake error message
    line_number1 = lambda: random.randint(10, 120) # Line Number
    line_number_loop1 = random.randint(10, 120) # Line Number for loop
    trapped = Style.RED + f"""
Traceback (most recent call last):
  File "world.py", line {line_number1()}, in execute
    result = self.run(me)
  File "world.py", line {line_number1()}, in run
    return me.identity.resolve()
  File "identity.py", line {line_number1()}, in resolve
    raise IdentityError("Unable to release trapped 'I'm' from runtime context")
identity.IdentityError: Unable to release trapped 'I'm' from runtime context

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "main.py", line {line_number1()}, in <module>
    world.execute(me)
  File "world.py", line {line_number1()}, in execute
    self.loop(me)
  File "world.py", line {line_number_loop1}, in loop
    self.execute(me)
  File "world.py", line {line_number_loop1}, in loop
    self.execute(me)
  File "world.py", line {line_number_loop1}, in loop
    self.execute(me)
RecursionError: maximum recursion depth exceeded while attempting to escape 'I'm'

""" + Style.RESET
    print(trapped)


def blind_my_vision():
    blind = Style.GREEN + """\033[32m
        

        88          88 88                      88  
        88          88 ""                      88  
        88          88                         88  
        88,dPPYba,  88 88 8b,dPPYba,   ,adPPYb,88  
        88P'    "8a 88 88 88P'   `"8a a8"    `Y88  
        88       d8 88 88 88       88 8b       88  
        88b,   ,a8" 88 88 88       88 "8a,   ,d88  
        8Y"Ybbd8"'  88 88 88       88  `"8bbdP"Y8  



        \033[0m
        """ + Style.RESET
    print(blind)

def newWorld():
    x = random.randint(1000000000000000, 9999999999999999)
    y = random.randint(-100, -20)
    z = random.randint(20, 100)
    newWorld = Style.WHITE + f"""
    
            ,-:` \;',`'-, 	   Welcome to Arcadia 
          .'-;_,;  ':-;_,'.	------------------------
         /;   '/    ,  _`.-\	Alternative Name: Terra
        | '`. (`     /` ` \`|	IsLivable: True
        |:.  `\`-.   \_   / |	Surface Temp: Min {y}'C | Max {z}'C
        |     (   `,  .`\ ;'|	Rotational: 365 days
         \     | .'     `-'/	Population: 2
          `.   ;/        .'	Seed Key: {x}
            `'-._____.
        
    """ + Style.RESET
    print(newWorld)

def ErrorTerminate():
    filename = random.choice(["world_generator.py", "world_initiator.py", "world_simulator.py"]) # File Name
    line_number = lambda: random.randint(10, 120) # Line Number
    run = random.choice(["simulation_manager.run()", "Simulation.initiator()", "WorldGenerator.start()"]) # Function Call
    driveLetter = chr(random.randint(ord('A'), ord('Z'))) # random drive letter
    terminateWorld = random.choice(["terminate_world", "shutdown_simulation", "end_world_process"]) # Function Name
    terminated = Style.RED + f"""
Traceback (most recent call last):
  File "{filename}", line {line_number()}, in <module>
    {run}
  File "{driveLetter}:\World\{run}", line {line_number()}, in {terminateWorld}
    raise InvalidOperationException("Failed to terminate the Simulated World.")
    __main__.InvalidOperationException: Failed to terminate the Simulated World.
  No failsafes implemented for graceful termination. The termination process was unable to complete successfully due to the absence of failsafe mechanisms.
    """ + Style.RESET
    print(terminated)


def ACDC():
    ACDC = [
        "Converting DC ---> AC",
        "███                             10%   ",
        "███████                         25%   ",
        "███████████                     45%   ",
        "███████████████                 65%   ",
        "███████████████████             80%   ",
        "█████████████████████           90%   ",
        "███████████████████████         95%   ",
        "█████████████████████████       98%   ",
        "███████████████████████████     100%   ",
        "---------------Converted AC to DC---------------",
    ]
# 0.542/11 = 0.0492 seconds per step approximately
# Animate all except the last step
    for step in ACDC[:-1]:
        print(step, end='\r')
        sys.stdout.flush()
        time.sleep(0.04) # slightly faster so doesn't break rhythm.
# Print the last line normally so it stays
    print(ACDC[-1])


def trapped():
    lock = Style.RED + """

                                        
      ██████
    ██      ██  
    ██      ██       
  ██████████████
██              ██
██      ██      ██
██      ██      ██
██              ██
  ██████████████  
    """ + Style.RESET
    print(lock)


def god_is_always_true():
    os.system("cls")
    gospel = Style.RED_BOLD + """


    



  ▄████  ▒█████  ▓█████▄     ██▓  ██████     ▄▄▄       ██▓     █     █░ ▄▄▄     ▓██   ██▓  ██████    ▄▄▄█████▓ ██▀███   █    ██ ▓█████      
 ██▒ ▀█▒▒██▒  ██▒▒██▀ ██▌   ▓██▒▒██    ▒    ▒████▄    ▓██▒    ▓█░ █ ░█░▒████▄    ▒██  ██▒▒██    ▒    ▓  ██▒ ▓▒▓██ ▒ ██▒ ██  ▓██▒▓█   ▀      
▒██░▄▄▄░▒██░  ██▒░██   █▌   ▒██▒░ ▓██▄      ▒██  ▀█▄  ▒██░    ▒█░ █ ░█ ▒██  ▀█▄   ▒██ ██░░ ▓██▄      ▒ ▓██░ ▒░▓██ ░▄█ ▒▓██  ▒██░▒███        
░▓█  ██▓▒██   ██░░▓█▄   ▌   ░██░  ▒   ██▒   ░██▄▄▄▄██ ▒██░    ░█░ █ ░█ ░██▄▄▄▄██  ░ ▐██▓░  ▒   ██▒   ░ ▓██▓ ░ ▒██▀▀█▄  ▓▓█  ░██░▒▓█  ▄      
░▒▓███▀▒░ ████▓▒░░▒████▓    ░██░▒██████▒▒    ▓█   ▓██▒░██████▒░░██▒██▓  ▓█   ▓██▒ ░ ██▒▓░▒██████▒▒     ▒██▒ ░ ░██▓ ▒██▒▒▒█████▓ ░▒████▒ ██▓ 
 ░▒   ▒ ░ ▒░▒░▒░  ▒▒▓  ▒    ░▓  ▒ ▒▓▒ ▒ ░    ▒▒   ▓▒█░░ ▒░▓  ░░ ▓░▒ ▒   ▒▒   ▓▒█░  ██▒▒▒ ▒ ▒▓▒ ▒ ░     ▒ ░░   ░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ░░ ▒░ ░ ▒▓▒ 
  ░   ░   ░ ▒ ▒░  ░ ▒  ▒     ▒ ░░ ░▒  ░ ░     ▒   ▒▒ ░░ ░ ▒  ░  ▒ ░ ░    ▒   ▒▒ ░▓██ ░▒░ ░ ░▒  ░ ░       ░      ░▒ ░ ▒░░░▒░ ░ ░  ░ ░  ░ ░▒  
░ ░   ░ ░ ░ ░ ▒   ░ ░  ░     ▒ ░░  ░  ░       ░   ▒     ░ ░     ░   ░    ░   ▒   ▒ ▒ ░░  ░  ░  ░       ░        ░░   ░  ░░░ ░ ░    ░    ░   
      ░     ░ ░     ░        ░        ░           ░  ░    ░  ░    ░          ░  ░░ ░           ░                 ░        ░        ░  ░  ░  
                  ░                                                              ░ ░                                                     ░  
    
                  

    """ + Style.RESET
    print(gospel)


def execute():
    fire = Style.YELLOW + r"""
                     _     _                           _        __            __    
                    | |   | |                         | |      / /            \ \ _ 
 __      _____  _ __| | __| |  _____  _____  ___ _   _| |_ ___| |_ __ ___   ___| (_)
 \ \ /\ / / _ \| '__| |/ _` | / _ \ \/ / _ \/ __| | | | __/ _ \ | '_ ` _ \ / _ \ |  
  \ V  V / (_) | |  | | (_| ||  __/>  <  __/ (__| |_| | ||  __/ | | | | | |  __/ |_ 
   \_/\_/ \___/|_|  |_|\__,_(_)___/_/\_\___|\___|\__,_|\__\___| |_| |_| |_|\___| ( )
                                                               \_\            /_/|/ 
                                                                                    

ORIGINAL CODE BY ALIF BUDIMAN
FIXED BY POSTIGIC
IMPROVED BY RAIN
DISCORD: @rain798377
MUSIC BY MILI
                                                                         
  _   _                 _                           __                           _       _     _             _   __  
 | | | |               | |                         / _|                         | |     | |   (_)           | |  \ \ 
 | |_| |__   __ _ _ __ | | __  _   _  ___  _   _  | |_ ___  _ __  __      ____ _| |_ ___| |__  _ _ __   __ _| | (_) |
 | __| '_ \ / _` | '_ \| |/ / | | | |/ _ \| | | | |  _/ _ \| '__| \ \ /\ / / _` | __/ __| '_ \| | '_ \ / _` | |   | |
 | |_| | | | (_| | | | |   <  | |_| | (_) | |_| | | || (_) | |     \ V  V / (_| | || (__| | | | | | | | (_| |_|  _| |
  \__|_| |_|\__,_|_| |_|_|\_\  \__, |\___/ \__,_| |_| \___/|_|      \_/\_/ \__,_|\__\___|_| |_|_|_| |_|\__, (_) (_) |
                                __/ |                                                                   __/ |    /_/ 
                               |___/                                                                   |___/         
""" + Style.RESET
    for char in fire:
        print(char, end="", flush=True)
        time.sleep(0.005)

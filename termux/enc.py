# -*- coding: UTF-8 -*-

# Author: Kenneth Panio
# Github: https://github.com/reiko_dev
# Contact: https://t.me/hackersdecipher
# Language: Python(3)
# Date: 29-10-2024

import os
import base64
import sys
import time
import requests
import random
import string
import uuid
from pprint import pformat

# ASCII art
logo = """
\033[0;31m
░       ░░░        ░░        ░░  ░░░░  ░░░      ░░░░░░░░░       ░░░        ░░  ░░░░  ░░░░░░░
▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒  ▒▒▒  ▒▒▒  ▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒▒▒▒▒▒
▓       ▓▓▓      ▓▓▓▓▓▓▓  ▓▓▓▓▓     ▓▓▓▓▓  ▓▓▓▓  ▓▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓      ▓▓▓▓▓  ▓▓  ▓▓▓▓▓▓▓▓
█  ███  ███  ███████████  █████  ███  ███  ████  ████████  ████  ██  ██████████    █████████
█  ████  ██        ██        ██  ████  ███      █████████       ███        █████  ██████████
                                                                                            

"""

# Basic colors
black = "\033[0;30m"
red = "\033[0;31m"
green = "\033[0;32m"
yellow = "\033[0;33m"
blue = "\033[0;34m"
purple = "\033[0;35m"
cyan = "\033[0;36m"
white = "\033[0;37m"

# Snippets
ask = red + '\n[' + red + '?' + red + '] ' + red
success = red + '\n[' + red + '√' + red + '] '
error = red + '\n[' + red + '!' + red + '] '
info = red + '\n[' + red + '+' + red + '] ' + red

# Current Directory
pwd = os.getcwd()

# Emoji unicode list
alphabet = [
    "\U0001f600", "\U0001f603", "\U0001f604", "\U0001f601", "\U0001f605",
    "\U0001f923", "\U0001f602", "\U0001f609", "\U0001f60A", "\U0001f61b"
]

# Maximum string length and offset for encoding
MAX_STR_LEN = 70
OFFSET = 10

# Normal printer with delay
def sprint(sentence, second=0.05):
    for word in sentence + '\n':
        sys.stdout.write(word)
        sys.stdout.flush()
        time.sleep(second)

# About section
def about():
    os.system("clear")
    sprint(logo, 0.001)
    print(f"{red}[ToolName]  {red} :[𝗘𝗡𝗖𝗥𝗬𝗧𝗜𝗢𝗡 𝗧𝗢𝗢𝗟]")
    print(f"{red}[Version]   {red} :[1.0]")
    print(f"{red}[Author]    {red} :[Kenneth Panio]")
    print(f"{red}[Github]    {red} :[https://github.com/reiko_dev]")
    print(f"{red}[Messenger] {red} :[https://t.me/hackersdecipher]")
    print(f"{red}[Email]     {red} :[lkpanio25@gmail.com]\n")
    ret = input(ask + "1 for main menu, 0 for exit  > " + red)
    if ret == "1":
        main()
    else:
        exit()

# Custom path chooser
def mover(out_file):
    move = input(ask + "Move to a custom path?(y/n) > " + red)
    if move == "y":
        mpath = input(ask + "Enter the path > " + red)
        if os.path.exists(mpath):
            os.system(f'''mv -f "{out_file}" "{mpath}" ''')
            sprint(f"{success}{out_file} moved to {mpath}\n")
        else:
            sprint(error + "Path does not exist!\n")
    else:
        print("\n")
    time.sleep(2)  # Wait for 2 seconds
    main()

# Base64 encoder function
def obfuscate(VARIABLE_NAME, file_content):
    b64_content = base64.b64encode(file_content.encode()).decode()
    index = 0
    code = f'{VARIABLE_NAME} = ""\n'
    for _ in range(int(len(b64_content) / OFFSET) + 1):
        _str = ''
        for char in b64_content[index:index + OFFSET]:
            byte = str(hex(ord(char)))[2:]
            if len(byte) < 2:
                byte = '0' + byte
            _str += '\\x' + str(byte)
        code += f'{VARIABLE_NAME} += "{_str}"\n'
        index += OFFSET
    code += f'exec(__import__("\\x62\\x61\\x73\\x65\\x36\\x34").b64decode({VARIABLE_NAME}.encode("\\x75\\x74\\x66\\x2d\\x38")).decode("\\x75\\x74\\x66\\x2d\\x38"))'
    return code

# Chunk string into smaller parts
def chunk_string(in_s, n):
    return "\n".join(
        "{}\\".format(in_s[i: i + n]) for i in range(0, len(in_s), n)
    ).rstrip("\\")

# Encode string using given alphabet
def encode_string(in_s, alphabet):
    d1 = dict(enumerate(alphabet))
    d2 = {v: k for k, v in d1.items()}
    return (
        'exec("".join(map(chr,[int("".join(str({}[i]) for i in x.split())) for x in\n'
        '"{}"\n.split("  ")])))\n'.format(
            pformat(d2),
            chunk_string(
                "  ".join(" ".join(d1[int(i)] for i in str(ord(c))) for c in in_s),
                MAX_STR_LEN,
            ),
        )
    )

# Encrypt Bash code using npm package "bash-obfuscate"
def encryptsh():
    in_file = input(ask + "Input Filename  > " + red)
    if not os.path.exists(in_file):
        print(error + 'File not found')
        os.system("sleep 2")
        encryptsh()
    rounds = int(input(ask + "Enter number of encryption rounds > "))
    os.system("bash-obfuscate " + in_file + " -o .temp")
    for _ in range(rounds - 1):
        os.system("bash-obfuscate .temp -o .temp")
    out_file = input(ask + "Output Filename  > " + red)
    with open(".temp", 'r') as temp_f, open(out_file, 'w') as out_f:
        filedata = temp_f.read()
        out_f.write("# Encrypted by Kenneth Panio\n# Github: https://github.com/reiko_dev\n\n" + filedata)
    os.remove(".temp")
    print(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

# Decrypt bash code using "eval"
def decryptsh():
    in_file = input(ask + "Input File  > " + red)
    if not os.path.exists(in_file):
        print(error + ' File not found')
        os.system("sleep 2")
        decryptsh()
    with open(in_file, 'r') as in_f, open(".temp1", 'w') as temp_f:
        filedata = in_f.read()
        if "eval" not in filedata:
            print(error + " Cannot be decrypted!")
            return
        newdata = filedata.replace("eval", "echo")
        temp_f.write(newdata)
    out_file = input(ask + "Output File  > " + red)
    os.system("bash .temp1 > .temp2")
    os.remove(".temp1")
    with open(".temp2", 'r') as temp_f2, open(out_file, 'w') as out_f:
        filedata = temp_f2.read()
        out_f.write("# Decrypted by Kenneth Panio\n# Github: https://github.com/reiko_dev\n\n" + filedata)
    os.remove(".temp2")
    print(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

# Encrypt python file into base64 variable
def encryptvar():
    var = input(ask + "Variable to be used(Must Required)  > " + red)
    if var == "":
        sprint(error + " No variable")
        os.system("sleep 3")
        encryptvar()
    if var.find(" ") != -1:
        sprint(error + " Only one word!")
        os.system("sleep 3")
        encryptvar()
    iteration = input(ask + "Iteration count for variable  > " + red)
    try:
        iteration = int(iteration)
    except Exception:
        iteration = 50
    VARIABLE_NAME = var * iteration
    in_file = input(ask + "Input file  > " + red)
    if not os.path.isfile(in_file):
        print(error + ' File not found')
        os.system("sleep 2")
        encryptvar()
    out_file = input(ask + "Output file  > " + red)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as in_f, open(out_file, 'w') as out_f:
        file_content = in_f.read()
        obfuscated_content = obfuscate(VARIABLE_NAME, file_content)
        out_f.write("# Encrypted by Kenneth Panio\n# Github- https://github.com/reiko_dev\n\n" + obfuscated_content)
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

# Encrypt python file into emoji
def encryptem():
    in_file = input(ask + "Input File  > " + red)
    if not os.path.isfile(in_file):
        print(error + ' File not found')
        os.system("sleep 2")
        encryptem()
    out_file = input(ask + "Output File  > " + red)
    with open(in_file) as in_f, open(out_file, "w", encoding="utf-8") as out_f:
        out_f.write("# Encrypted by Kenneth Panio\n# Github- https://github.com/reiko_dev\n\n")
        out_f.write(encode_string(in_f.read(), alphabet))
        sprint(f"{success}{out_file} saved in {pwd}")
        mover(out_file)

# New function: obtain access token from Facebook
def obtain():
    e = input(ask + "Enter your Facebook email/uid: ")
    p = input(ask + "Enter your Facebook password: ")

    h = {
        'authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',       
        'x-fb-friendly-name': 'Authenticate',
        'x-fb-connection-type': 'Unknown',
        'accept-encoding': 'gzip, deflate',
        'content-type': 'application/x-www-form-urlencoded',
        'x-fb-http-engine': 'Liger'
    }
    d = {
        'adid': ''.join(random.choices(string.hexdigits, k=16)),
        'format': 'json',
        'device_id': str(uuid.uuid4()),
        'email': e,
        'password': p,
        'generate_analytics_claims': '0',
        'credentials_type': 'password',
        'source': 'login',
        'error_detail_type': 'button_with_disabled',
        'enroll_misauth': 'false',
        'generate_session_cookies': '0',
        'generate_machine_id': '0',
        'fb_api_req_friendly_name': 'authenticate',
    }
    ses = requests.Session()
    ses.headers.update(h)
    submit = ses.post('https://b-graph.facebook.com/auth/login', data=d).json()  

    if 'session_key' in submit:
        print(f'\n\033[92m SUCCESS: {submit["access_token"]} \033[0m')

    elif 'www.facebook.com' in submit.get('error', {}).get('message', ''):
        print('\n\033[91m FAILED: ACCOUNT IN CHECKPOINT \033[0m')

    elif 'SMS' in submit.get('error', {}).get('message', ''):
        print('\n\033[91m FAILED: 2 FACTOR AUTHENTICATION IS ENABLED. PLEASE DISABLE IT BEFORE GETTING TOKEN \033[0m')

    elif submit.get('error', {}).get('error_user_title') == 'Wrong Credentials':
        print('\n\033[91m FAILED: WRONG CREDENTIALS \033[0m')

    elif submit.get('error', {}).get('error_user_title') == 'Incorrect Username':
        print('\n\033[91m FAILED: ACCOUNT DOES NOT EXIST \033[0M')

    elif 'limit' in submit.get('error', {}).get('message', ''):
        print('\n\033[91m FAILED: REQUEST LIMIT. USE VPN OR WAIT \033[0m')

    elif 'required' in submit.get('error', {}).get('message', ''):     
        print('\n\033[91m FAILED: PLEASE FILL IN ALL REQUIRED FIELDS \033[0m')

    else:
        print(f'\n\033[91m ERROR: {submit}\033[0m')

# Main function
def main():
    os.system("clear")
    sprint(logo, 0.001)
    print(f"{red}[1]{red} Bash{red} Encryption")
    print(f"{red}[2]{red} Bash{red} Decryption")
    print(f"{red}[3]{red} Encrypt{red} Python into Variable")
    print(f"{red}[4]{red} Encrypt{red} Python into Emoji")
    print(f"{red}[5]{red} Get Facebook Token")
    print(f"{red}[6]{red} About")
    print(f"{red}[7]{red} More Tools")
    print(f"{red}[0]{red} Exit")
    choose = input(f"{ask}{red}Choose an option : {red}")
    while True:
        if choose in ["1", "01"]:
            encryptsh()
        elif choose in ["2", "02"]:
            decryptsh()
        elif choose in ["3", "03"]:
            encryptvar()
        elif choose in ["4", "04"]:
            encryptem()
        elif choose in ["5", "05"]:
            obtain()
        elif choose in ["6", "06"]:
            about()
        elif choose in ["7", "07"]:
            if os.path.exists("/data/data/com.termux/files/home"):
                os.system("xdg-open --view 'https://github.com/reiko_dev")
            else:
                os.system("xdg-open 'https://github.com/reiko_dev'")
            main()
        
        elif choose == "0":
            exit()
        else:
            sprint(error + 'Wrong input!')
            os.system("sleep 2")
            main()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sprint(info + "Salamat sa pag gamit!")
        exit()
    except Exception as e:
        sprint(error + str(e))

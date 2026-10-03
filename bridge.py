"""Moomoo OpenD -> JSON bridge for the options dashboard (read-only market data, no trading).
Install once:   pip install flask flask-cors pandas moomoo-api
Run:            py bridge.py          (keep OpenD running and logged in)
Dashboard URL:  http://127.0.0.1:8888
"""
import time, threading
from datetime import date, timedelta
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from moomoo import OpenQuoteContext, RET_OK, SubType, KLType, AuType, OptionType, OptionCondType

OPEND_HOST, OPEND_PORT, BRIDGE_PORT = '127.0.0.1', 11111, 8888
app = Flask(__name__)
CORS(app, origins='*', allow_headers=['X-API-Key', 'X-API-Secret', 'Content-Type'])

@app.after_request
def pna(resp):  # Chrome/Edge require this for a public website to call localhost
    resp.headers['Access-Control-Allow-Private-Network'] = 'true'
    return resp

ctx = OpenQuoteContext(host=OPEND_HOST, port=OPEND_PORT)
lock = threading.Lock()
subs, chain_cache, last_chain_call = set(), {}, [0.0]

def num(x):
    try:
        return None if pd.isna(x) else float(x)
    except Exception:
        return None

@app.get('/health')
def health():
    return jsonify(ok=True)

@app.get('/bars')
def bars():
    sym = request.args.get('symbol', '').upper()
    c = 'US.' + sym
    with lock:
        if c not in subs:
            ret, e = ctx.subscribe([c], [SubType.K_5M], subscribe_push=False)
            if ret != RET_OK:
                return jsonify(error=str(e)), 502
            subs.add(c)
        ret, df = ctx.get_cur_kline(c, 300, KLType.K_5M, AuType.QFQ)
    if ret != RET_OK:
        return jsonify(error=str(df)), 502
    ts = pd.to_datetime(df['time_key']).dt.tz_localize('America/New_York', ambiguous='NaT', nonexistent='NaT')
    out = []
    for t, (_, r) in zip(ts, df.iterrows()):
        if pd.isna(t):
            continue
        out.append(dict(t=int(t.value // 10**6), o=num(r['open']), h=num(r['high']), l=num(r['low']), c=num(r['close']), v=num(r['volume'])))
    return jsonify(out)

@app.get('/chain')
def chain():
    sym = request.args.get('symbol', '').upper()
    c = 'US.' + sym
    with lock:
        ret, sn = ctx.get_market_snapshot([c])
        if ret != RET_OK:
            return jsonify(error=str(sn)), 502
        spot = float(sn['last_price'][0])
        ent = chain_cache.get(sym)
        if not ent or time.time() - ent[0] > 1800:   # cache contract list 30 min (OpenD limit: 10 chain calls / 30 s)
            time.sleep(max(0, 3.2 - (time.time() - last_chain_call[0])))
            last_chain_call[0] = time.time()
            ret, df = ctx.get_option_chain(c, start=str(date.today()), end=str(date.today() + timedelta(days=30)),
                                           option_type=OptionType.ALL, option_cond_type=OptionCondType.ALL)
            if ret != RET_OK:
                return jsonify(error=str(df)), 502
            chain_cache[sym] = ent = (time.time(), df)
        df = ent[1]
        df = df[(df['strike_price'] >= spot * .92) & (df['strike_price'] <= spot * 1.08)].copy()
        df['d'] = (df['strike_price'] - spot).abs()
        df = df.sort_values('d').head(400)
        meta = {r['code']: r for _, r in df.iterrows()}
        ret, s = ctx.get_market_snapshot(list(meta))
    if ret != RET_OK:
        return jsonify(error=str(s)), 502
    out = []
    for _, r in s.iterrows():
        m = meta[r['code']]
        iv = num(r.get('option_implied_volatility'))
        if iv is not None and iv > 5:
            iv /= 100          # OpenD reports percent; dashboard wants decimal
        out.append(dict(exp=str(m['strike_time'])[:10], type='C' if str(m['option_type']).upper().startswith('C') else 'P',
                        strike=num(m['strike_price']), bid=num(r.get('bid_price')), ask=num(r.get('ask_price')), last=num(r.get('last_price')),
                        vol=num(r.get('volume')), oi=num(r.get('option_open_interest')), iv=iv,
                        delta=num(r.get('option_delta')), gamma=num(r.get('option_gamma')),
                        theta=num(r.get('option_theta')), vega=num(r.get('option_vega'))))
    return jsonify(out)

if __name__ == '__main__':
    print('[*] Bridge on http://127.0.0.1:%d  (OpenD %s:%d)' % (BRIDGE_PORT, OPEND_HOST, OPEND_PORT))
    app.run(host='127.0.0.1', port=BRIDGE_PORT, threaded=False)

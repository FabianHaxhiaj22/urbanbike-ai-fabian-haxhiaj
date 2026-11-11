import argparse
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import pandas as pd
import joblib
from config.common import ROOT, REPORTS, FIGURES, FEATURES, read_splits

model_path = ROOT / "models" / "regression.joblib"
if not model_path.exists():
    raise SystemExit("Fillimisht ekzekuto: python run_all.py")
bundle = joblib.load(model_path)
summary = json.loads((REPORTS / "results_summary.json").read_text())
train, valid, test = read_splits()
dates = test.date.dt.strftime("%Y-%m-%d").tolist()

def predict(date):
    if date not in dates:
        raise ValueError("Zgjidh nje date nga lista e testit.")
    row = test.loc[test.date == pd.Timestamp(date)]
    model = bundle["models"][bundle["selected"]]
    value = float(max(0, model.predict(row[FEATURES])[0]))
    actual = int(row.iloc[0].rentals)
    return {"date": date, "model": bundle["selected"],
            "prediction": value, "actual": actual,
            "absolute_error": abs(value - actual)}

def page(result):
    options = []
    for date in dates:
        chosen = " selected" if date == result["date"] else ""
        options.append(f"<option{chosen}>{date}</option>")
    scores = pd.DataFrame(summary["metrics"])
    scores = scores.loc[scores.split == "test", ["model", "MAE", "RMSE",
                                               "R2"]]
    table = scores.to_html(index=False, float_format=lambda x: f"{x:.3f}")
    return f'''<!doctype html>
<html lang="sq"><meta charset="utf-8"><title>UrbanBike AI</title>
<style>
body{{font:16px system-ui;max-width:900px;margin:30px auto;padding:20px;
color:#12243a;background:#f3f6f8}}table{{border-collapse:collapse}}
td,th{{padding:8px 14px}}img{{max-width:100%}}button,select{{padding:10px}}
</style><h1>UrbanBike AI</h1>
<p>Washington D.C., 2011–2012. Demonstrim historik një ditë përpara.</p>
<form><label>Data <select name="date">{''.join(options)}</select></label>
<button>Parashiko</button></form>
<h2>{result['date']} · {result['model']}</h2>
<p>Parashikimi: <b>{result['prediction']:.2f}</b> qira</p>
<p>Reale: {result['actual']} · Gabimi: {result['absolute_error']:.2f}</p>
<h2>Metrikat e testit</h2>{table}
<img src="/figures/04_predictions.png" alt="Parashikime dhe vlera reale">
<h2>Eksplorimi vetëm me train</h2>
<img src="/figures/01_demand.png" alt="Qiratë historike në train">
<p>Moti përdor lag7. Numërimet e djeshme supozohen të njohura.
Ky demonstrim nuk verifikon parashikim të drejtpërdrejtë për sot.</p>
</html>'''

class Handler(BaseHTTPRequestHandler):
    def send(self, body, kind, status=200):
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def do_GET(self):
        url = urlparse(self.path)
        if url.path.startswith("/figures/"):
            path = FIGURES / Path(url.path).name
            if path.suffix == ".png" and path.is_file():
                return self.send(path.read_bytes(), "image/png")
        if url.path not in ["/", "/api/predict"]:
            return self.send("Nuk u gjet.", "text/plain", 404)
        date = parse_qs(url.query).get("date", [dates[0]])[0]
        try:
            result = predict(date)
        except ValueError as error:
            return self.send(str(error), "text/plain; charset=utf-8", 400)
        if url.path == "/api/predict":
            return self.send(json.dumps(result), "application/json")
        self.send(page(result), "text/html; charset=utf-8")

    def log_message(self, *args):
        pass

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()
server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
print(f"Hap http://127.0.0.1:{args.port} . Ndalimi: Ctrl+C", flush=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Aplikacioni u ndal.")
finally:
    server.server_close()

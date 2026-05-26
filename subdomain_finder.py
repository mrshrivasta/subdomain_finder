"""
╔══════════════════════════════════════════════════════════════╗
║       SUBDOMAIN FINDER — EDUCATIONAL TOOL                   ║
║       Made by Karanam Shrivasta                             ║
║       LinkedIn : linkedin.com/in/karanam-shrivasta          ║
║       GitHub   : github.com/mrshrivasta                     ║
╠══════════════════════════════════════════════════════════════╣
║  ⚠  LEGAL DISCLAIMER                                        ║
║  Educational / research use ONLY on domains you OWN or      ║
║  have EXPLICIT WRITTEN PERMISSION to test.                  ║
║  May violate CFAA (US) · CMA 1990 (UK) · IT Act 2000 (IN)  ║
║  Author assumes ZERO LIABILITY for misuse.                  ║
╚══════════════════════════════════════════════════════════════╝

Usage:
  python subdomain_finder.py                     # CLI
  python subdomain_finder.py --web               # Web UI → http://localhost:5000
  python subdomain_finder.py --domain example.com
  python subdomain_finder.py --domain example.com --wordlist my_list.txt
  python subdomain_finder.py --domain example.com --csv out.csv --json out.json

Install:
  pip install flask dnspython requests
"""

import sys, os, re, csv, json, socket, time, threading, argparse, concurrent.futures
from datetime import datetime

# Optional imports
try:
    import dns.resolver, dns.exception
    DNSPYTHON = True
except ImportError:
    DNSPYTHON = False

try:
    import requests
    REQUESTS = True
except ImportError:
    REQUESTS = False

# ── Built-in wordlist (500 common subdomains) ─────────────────────────────────
BUILTIN_WORDLIST = """www api mail smtp pop imap ftp ssh vpn dev staging prod test
admin portal dashboard app apps mobile web static assets cdn media img images
upload uploads download downloads files docs documentation blog forum shop store
payment checkout cart account accounts login auth oauth sso register signup
support help helpdesk ticket tickets crm erp hr finance billing invoice
monitoring metrics logs grafana kibana elastic jenkins ci cd git gitlab github
bitbucket jira confluence wiki status statuspage health ping beta alpha preview
sandbox demo lab research internal intranet extranet corp corporate office
mail2 webmail email newsletter news events calendar booking reservation
backup backups db database mysql postgres redis mongo elasticsearch
api1 api2 apiv1 apiv2 v1 v2 v3 proxy gateway lb loadbalancer
ns1 ns2 mx mx1 mx2 smtp1 smtp2 pop3 imap4 webdisk cpanel whm
secure ssl vpn1 vpn2 remote desktop rdp citrix juniper
dev1 dev2 dev3 staging1 staging2 uat qa test1 test2 sandbox1
old legacy archive backup1 mirror relay gateway1 edge
android ios app1 app2 microservice service services
stream video audio podcast media1 media2 live streaming
map maps location geo geoip
chat messaging socket ws wss push notifications realtime
cron scheduler worker queue jobs
management control panel manage operations ops devops sre
security scan ids ips waf firewall
docs api-docs swagger openapi graphql rest grpc
tenant customer partner affiliate vendor supplier
careers jobs recruitment talent hr people
investor ir press media pr brand
social facebook twitter linkedin instagram youtube
analytics data warehouse bi reporting tableau powerbi
cloud aws azure gcp heroku docker k8s kubernetes
phpmyadmin adminer mongo-express redis-commander
jenkins sonar nexus artifactory registry
""".split()

# deduplicate
BUILTIN_WORDLIST = list(dict.fromkeys(BUILTIN_WORDLIST))


# ── DNS resolver ──────────────────────────────────────────────────────────────
def resolve_host(hostname: str, timeout: float = 2.0) -> dict | None:
    """
    Try multiple DNS record types. Returns result dict or None.
    Uses dnspython if available, else socket fallback.
    """
    result = {
        "hostname": hostname,
        "ips": [],
        "cname": None,
        "mx": None,
        "status": "found",
        "http_status": None,
        "server": None,
        "title": None,
        "resolved_at": datetime.now().isoformat(timespec="seconds"),
    }

    # ── Method 1: dnspython ───────────────────────────────────────────────────
    if DNSPYTHON:
        resolver = dns.resolver.Resolver()
        resolver.timeout = timeout
        resolver.lifetime = timeout

        # A record
        try:
            answers = resolver.resolve(hostname, "A")
            result["ips"] = [str(r) for r in answers]
        except (dns.exception.DNSException, Exception):
            pass

        # CNAME
        try:
            answers = resolver.resolve(hostname, "CNAME")
            result["cname"] = str(answers[0].target).rstrip(".")
        except Exception:
            pass

        if not result["ips"] and not result["cname"]:
            return None

    else:
        # ── Method 2: socket fallback ─────────────────────────────────────────
        try:
            infos = socket.getaddrinfo(hostname, None, socket.AF_INET)
            result["ips"] = list(dict.fromkeys(i[4][0] for i in infos))
        except socket.gaierror:
            return None

    if not result["ips"] and not result["cname"]:
        return None

    # ── HTTP probe (optional) ─────────────────────────────────────────────────
    if REQUESTS and result["ips"]:
        for scheme in ("https", "http"):
            try:
                resp = requests.get(
                    f"{scheme}://{hostname}",
                    timeout=3, allow_redirects=True,
                    headers={"User-Agent": "Mozilla/5.0 (Educational Scanner)"},
                    verify=False,
                )
                result["http_status"] = resp.status_code
                result["server"] = resp.headers.get("Server", "")
                # Extract <title>
                m = re.search(r"<title[^>]*>(.*?)</title>", resp.text, re.IGNORECASE | re.DOTALL)
                result["title"] = m.group(1).strip()[:80] if m else ""
                break
            except Exception:
                pass

    return result


# ── Core scan function ────────────────────────────────────────────────────────
def find_subdomains(
    domain: str,
    wordlist: list[str] = None,
    workers: int = 50,
    timeout: float = 2.0,
    on_result=None,
    stop_event: threading.Event = None,
) -> list[dict]:
    """Enumerate subdomains concurrently."""
    if wordlist is None:
        wordlist = BUILTIN_WORDLIST

    domain = domain.strip().lower().removeprefix("http://").removeprefix("https://").split("/")[0]
    targets = [f"{sub}.{domain}" for sub in wordlist]
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(resolve_host, h, timeout): h for h in targets}
        for fut in concurrent.futures.as_completed(futs):
            if stop_event and stop_event.is_set():
                ex.shutdown(wait=False, cancel_futures=True)
                break
            try:
                res = fut.result()
                if res:
                    results.append(res)
                    if on_result:
                        on_result(res)
            except Exception:
                pass

    results.sort(key=lambda r: r["hostname"])
    return results


# ── CLI ───────────────────────────────────────────────────────────────────────
def cli_mode():
    parser = argparse.ArgumentParser(
        description="Subdomain Finder — Karanam Shrivasta | github.com/mrshrivasta"
    )
    parser.add_argument("--web",      action="store_true")
    parser.add_argument("--domain",   default="example.com")
    parser.add_argument("--wordlist", default=None, help="Path to wordlist file (one per line)")
    parser.add_argument("--workers",  type=int, default=50)
    parser.add_argument("--timeout",  type=float, default=2.0)
    parser.add_argument("--csv",      default=None)
    parser.add_argument("--json",     default=None)
    args = parser.parse_args()

    if args.web:
        web_mode(); return

    wordlist = BUILTIN_WORDLIST
    if args.wordlist:
        with open(args.wordlist) as f:
            wordlist = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    print(f"\n{'═'*62}")
    print(f"  Subdomain Finder — Educational Tool")
    print(f"  Domain   : {args.domain}")
    print(f"  Wordlist : {len(wordlist)} entries")
    print(f"  Workers  : {args.workers}  |  Timeout: {args.timeout}s")
    print(f"  dnspython: {'yes' if DNSPYTHON else 'no (pip install dnspython)'}")
    print(f"  requests : {'yes' if REQUESTS else 'no (pip install requests)'}")
    print(f"  Made by Karanam Shrivasta  ⚠ Authorised domains only")
    print(f"{'═'*62}\n")

    found = []

    def on_result(r):
        ips = ", ".join(r["ips"][:2]) if r["ips"] else r.get("cname", "")
        http = f"[HTTP {r['http_status']}]" if r["http_status"] else ""
        print(f"  ✓ {r['hostname']:<45} {ips:<18} {http}")
        found.append(r)

    find_subdomains(args.domain, wordlist, args.workers, args.timeout, on_result)

    print(f"\n{'═'*62}")
    print(f"  Found {len(found)} subdomains for {args.domain}")
    print(f"{'═'*62}\n")

    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["hostname","ips","cname","http_status","server","title","resolved_at"])
            for r in found:
                w.writerow([r["hostname"],";".join(r["ips"]),r.get("cname",""),
                            r.get("http_status",""),r.get("server",""),r.get("title",""),r["resolved_at"]])
        print(f"  CSV → {args.csv}")

    if args.json:
        with open(args.json, "w") as f:
            json.dump(found, f, indent=2)
        print(f"  JSON → {args.json}\n")


# ── Flask Web App ─────────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Subdomain Finder | Karanam Shrivasta</title>
<meta name="description" content="Free educational subdomain enumeration tool. Discover subdomains via DNS brute-force. Built by Karanam Shrivasta.">
<meta name="keywords" content="subdomain finder, subdomain enumeration, DNS brute force, subdomain scanner, bug bounty tools, ethical hacking, network security education, Karanam Shrivasta">
<meta name="author" content="Karanam Shrivasta">
<meta name="robots" content="index,follow">
<meta name="geo.region" content="IN">
<meta property="og:title" content="Subdomain Finder — Educational Tool">
<meta property="og:description" content="Discover subdomains via DNS enumeration. Educational tool by Karanam Shrivasta.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<meta name="twitter:creator" content="@mrshrivasta">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Subdomain Finder",
"description":"Educational subdomain enumeration and DNS brute-force tool.",
"applicationCategory":"SecurityApplication","operatingSystem":"Linux,macOS,Windows",
"author":{"@type":"Person","name":"Karanam Shrivasta",
"url":"https://www.linkedin.com/in/karanam-shrivasta/","sameAs":["https://github.com/mrshrivasta"]},
"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}
</script>
<style>
:root{--blue:#1A6FD4;--green:#1D9E75;--purple:#534AB7;--red:#E24B4A;
      --bg:#f0f2f5;--card:#fff;--bdr:#e2e8f0;--text:#1a202c;--muted:#64748b;--mono:'Courier New',monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:2rem 1rem}
.container{max-width:960px;margin:0 auto}
h1{font-size:24px;font-weight:700;margin-bottom:4px}
.subtitle{font-size:14px;color:var(--muted);margin-bottom:1.25rem}
.disc{background:#FCEBEB;border:1px solid #F09595;border-radius:12px;padding:1rem 1.25rem;margin-bottom:1.25rem}
.disc h2{font-size:13px;font-weight:700;color:#791F1F;margin-bottom:6px}
.disc p{font-size:12px;color:#A32D2D;line-height:1.7}
.card{background:var(--card);border-radius:14px;border:1px solid var(--bdr);padding:1.25rem;margin-bottom:1rem}
.card-title{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:.875rem}
.form-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:.875rem}
.form-row label{font-size:13px;color:var(--muted)}
input,select,textarea{border:1px solid var(--bdr);border-radius:8px;padding:8px 12px;
  font-size:13px;font-family:var(--mono);background:white;color:var(--text)}
input:focus,select:focus,textarea:focus{outline:2px solid var(--blue);border-color:transparent}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:.875rem}
.tab{padding:6px 14px;border-radius:50px;border:1px solid var(--bdr);font-size:12px;
     cursor:pointer;background:white;color:var(--muted);transition:all .15s;user-select:none}
.tab:hover{background:#f8fafc}
.tab.active{background:var(--blue);color:white;border-color:var(--blue)}
.btn{padding:9px 20px;border-radius:50px;border:none;font-size:13px;font-weight:600;
     cursor:pointer;transition:opacity .15s}
.btn:hover{opacity:.85}
.btn-blue{background:var(--blue);color:white}
.btn-red{background:var(--red);color:white}
.btn-green{background:var(--green);color:white}
.btn-gray{background:#f1f5f9;color:var(--text);border:1px solid var(--bdr)}
.btn-purple{background:var(--purple);color:white}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin-bottom:1rem}
.stat{background:#f8fafc;border-radius:10px;padding:12px;border:1px solid var(--bdr)}
.stat-v{font-size:22px;font-weight:700}
.stat-l{font-size:11px;color:var(--muted);margin-top:2px}
.bar-wrap{height:6px;background:#e2e8f0;border-radius:3px;margin-bottom:.875rem;overflow:hidden}
.bar{height:6px;border-radius:3px;background:var(--blue);width:0%;transition:width .2s}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}
.b-found{background:#DCFCE7;color:#166534}
.b-http{background:#DBEAFE;color:#1e40af}
.b-err{background:#FEE2E2;color:#991B1B}
.results-tbl{width:100%;font-size:12px;border-collapse:collapse}
.results-tbl th{background:#f8fafc;padding:9px 10px;text-align:left;font-size:11px;
  font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;border-bottom:1px solid var(--bdr)}
.results-tbl td{padding:8px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top;font-family:var(--mono)}
.results-tbl tr:hover td{background:#f8fafc}
.log-box{background:#0f172a;border-radius:10px;padding:1rem;font-family:var(--mono);
  font-size:11px;max-height:180px;overflow-y:auto;line-height:1.9;color:#64748b}
.ok{color:#4ade80}.warn{color:#fbbf24}.err{color:#f87171}.info{color:#60a5fa}
.watermark{border-top:1px solid var(--bdr);padding-top:1rem;margin-top:1rem;
  display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.wm-name{font-size:13px;font-weight:700}
.wm-role{font-size:11px;color:var(--muted)}
.wm-links a{font-size:13px;color:var(--blue);text-decoration:none;margin-left:10px;font-weight:500}
.tag{display:inline-block;background:#f1f5f9;border-radius:4px;padding:1px 6px;
     font-size:11px;margin:1px;font-family:var(--mono);color:var(--text)}
</style>
</head>
<body>
<div class="container">
  <h1>🌐 Subdomain Finder</h1>
  <p class="subtitle">Educational DNS enumeration tool — discover subdomains of a target domain</p>

  <div class="disc" role="alert">
    <h2>⚠️ Legal disclaimer — read before use</h2>
    <p>Use <strong>only</strong> on domains you own or have <strong>explicit written permission</strong> to test. Unauthorised subdomain enumeration may violate <strong>CFAA</strong> (US) · <strong>Computer Misuse Act 1990</strong> (UK) · <strong>IT Act 2000</strong> (India). <strong>Karanam Shrivasta</strong> assumes zero liability for misuse. By using this tool you accept these terms.</p>
  </div>

  <div class="card">
    <div class="card-title">Target configuration</div>
    <div class="form-row">
      <label>Domain</label>
      <input id="domain" placeholder="example.com" style="width:240px">
      <label>Threads</label>
      <input type="number" id="workers" value="50" min="1" max="200" style="width:70px">
      <label>Timeout(s)</label>
      <input type="number" id="timeout" value="2" step="0.5" min="0.5" max="10" style="width:70px">
    </div>

    <div class="card-title">Wordlist mode</div>
    <div class="tabs" id="wl-tabs">
      <div class="tab active" data-m="builtin">Built-in (~200 words)</div>
      <div class="tab" data-m="custom">Custom wordlist</div>
    </div>
    <div id="custom-wl" style="display:none;margin-bottom:.875rem">
      <textarea id="custom-words" rows="5" style="width:100%;font-size:12px"
        placeholder="One subdomain prefix per line&#10;www&#10;api&#10;mail&#10;dev&#10;staging"></textarea>
    </div>

    <div class="card-title">HTTP probing</div>
    <div class="form-row">
      <label style="display:flex;align-items:center;gap:6px;cursor:pointer">
        <input type="checkbox" id="http-probe" checked style="width:16px;height:16px;accent-color:var(--blue)">
        Probe HTTP/HTTPS status + server banner + page title
      </label>
    </div>

    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button class="btn btn-blue" id="start-btn">▶ Start scan</button>
      <button class="btn btn-red" id="stop-btn" style="display:none">⏸ Stop</button>
      <button class="btn btn-gray" id="clear-btn">✕ Clear</button>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Progress</div>
    <div class="stats">
      <div class="stat"><div class="stat-v" id="st-checked">0</div><div class="stat-l">checked</div></div>
      <div class="stat"><div class="stat-v" id="st-found" style="color:var(--green)">0</div><div class="stat-l">found</div></div>
      <div class="stat"><div class="stat-v" id="st-total">0</div><div class="stat-l">total</div></div>
      <div class="stat"><div class="stat-v" id="st-pct">0%</div><div class="stat-l">complete</div></div>
      <div class="stat"><div class="stat-v" id="st-time">0s</div><div class="stat-l">elapsed</div></div>
    </div>
    <div class="bar-wrap"><div class="bar" id="prog-bar"></div></div>
    <div id="scan-status" style="font-size:12px;color:var(--muted);margin-bottom:.5rem">Ready</div>
  </div>

  <div class="card">
    <div class="card-title">Results</div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:.875rem">
      <input id="filter" placeholder="Filter results..." style="flex:1;min-width:180px">
      <button class="btn btn-gray" onclick="exportCSV()" style="font-size:12px;padding:7px 14px">⬇ CSV</button>
      <button class="btn btn-gray" onclick="exportJSON()" style="font-size:12px;padding:7px 14px">⬇ JSON</button>
      <button class="btn btn-gray" onclick="copyAll()" style="font-size:12px;padding:7px 14px">⎘ Copy hostnames</button>
    </div>
    <div style="overflow-x:auto">
      <table class="results-tbl">
        <thead>
          <tr>
            <th>#</th><th>Subdomain</th><th>IP addresses</th><th>CNAME</th>
            <th>HTTP</th><th>Server</th><th>Title</th>
          </tr>
        </thead>
        <tbody id="results-body"></tbody>
      </table>
    </div>
    <div id="no-results" style="text-align:center;padding:2rem;color:var(--muted);font-size:14px">
      No results yet — start a scan above.
    </div>
  </div>

  <div class="card">
    <div class="card-title">Activity log</div>
    <div class="log-box" id="log"></div>
  </div>

  <div class="watermark">
    <div>
      <div class="wm-name">Made by Karanam Shrivasta</div>
      <div class="wm-role">Network Security Educator · Ethical Hacking Researcher · Open Source Developer</div>
    </div>
    <div class="wm-links">
      <a href="https://www.linkedin.com/in/karanam-shrivasta/" target="_blank" rel="noopener">LinkedIn</a>
      <a href="https://github.com/mrshrivasta" target="_blank" rel="noopener">GitHub</a>
    </div>
  </div>
</div>

<script>
let scan={es:null,results:[],checked:0,total:0,timer:null,startTime:null};
let wlMode='builtin';

document.querySelectorAll('#wl-tabs .tab').forEach(t=>t.addEventListener('click',function(){
  document.querySelectorAll('#wl-tabs .tab').forEach(x=>x.classList.remove('active'));
  this.classList.add('active'); wlMode=this.dataset.m;
  document.getElementById('custom-wl').style.display=wlMode==='custom'?'block':'none';
}));

function ts(){return new Date().toLocaleTimeString();}
function addLog(msg,type='info'){
  const el=document.getElementById('log');
  el.innerHTML+=`<span class="${type}">[${ts()}]</span> ${msg}\n`;
  el.scrollTop=el.scrollHeight;
}

function updateStats(){
  const found=scan.results.length;
  document.getElementById('st-checked').textContent=scan.checked;
  document.getElementById('st-found').textContent=found;
  document.getElementById('st-total').textContent=scan.total;
  document.getElementById('st-pct').textContent=scan.total?Math.round(scan.checked/scan.total*100)+'%':'0%';
  document.getElementById('prog-bar').style.width=scan.total?(scan.checked/scan.total*100)+'%':'0%';
}

function renderRow(r, idx){
  const ips=(r.ips||[]).join(', ')||'—';
  const cname=r.cname||'—';
  const http=r.http_status?`<span class="badge b-http">${r.http_status}</span>`:'—';
  const server=r.server?`<span class="tag">${r.server.substring(0,30)}</span>`:'—';
  const title=r.title?`<span style="font-size:11px;color:var(--muted)">${r.title.substring(0,60)}</span>`:'—';
  const tbody=document.getElementById('results-body');
  const tr=document.createElement('tr');
  tr.id='row-'+idx;
  tr.innerHTML=`
    <td style="color:var(--muted);font-size:11px">${idx}</td>
    <td><span class="badge b-found" style="font-family:var(--mono)">${r.hostname}</span></td>
    <td style="font-size:11px">${ips}</td>
    <td style="font-size:11px;color:var(--muted)">${cname}</td>
    <td>${http}</td>
    <td>${server}</td>
    <td>${title}</td>`;
  tbody.appendChild(tr);
  document.getElementById('no-results').style.display='none';
}

function startScan(){
  const domain=document.getElementById('domain').value.trim();
  if(!domain){alert('Enter a domain name.');return;}
  scan={es:null,results:[],checked:0,total:0,timer:null,startTime:Date.now()};
  document.getElementById('results-body').innerHTML='';
  document.getElementById('no-results').style.display='block';
  document.getElementById('start-btn').style.display='none';
  document.getElementById('stop-btn').style.display='inline-block';
  document.getElementById('scan-status').textContent='Scanning '+domain+'...';
  addLog('Scan started: '+domain,'info');

  const workers=document.getElementById('workers').value;
  const timeout=document.getElementById('timeout').value;
  const http=document.getElementById('http-probe').checked?'1':'0';
  let words='';
  if(wlMode==='custom'){
    words=encodeURIComponent(document.getElementById('custom-words').value.trim());
  }

  scan.timer=setInterval(()=>{
    document.getElementById('st-time').textContent=Math.round((Date.now()-scan.startTime)/1000)+'s';
  },1000);

  const url=`/api/scan?domain=${encodeURIComponent(domain)}&workers=${workers}&timeout=${timeout}&http=${http}&words=${words}`;
  scan.es=new EventSource(url);

  scan.es.addEventListener('progress',ev=>{
    const d=JSON.parse(ev.data);
    scan.total=d.total; scan.checked=d.checked;
    updateStats();
  });

  scan.es.addEventListener('found',ev=>{
    const r=JSON.parse(ev.data);
    scan.results.push(r);
    renderRow(r, scan.results.length);
    addLog('FOUND: '+r.hostname+' → '+(r.ips[0]||r.cname||'?')+(r.http_status?' [HTTP '+r.http_status+']':''),'ok');
    updateStats();
  });

  scan.es.addEventListener('done',ev=>{
    const d=JSON.parse(ev.data);
    finishScan(d.found, d.total);
  });

  scan.es.onerror=()=>{
    finishScan(scan.results.length, scan.total);
  };
}

function finishScan(found, total){
  if(scan.es) scan.es.close();
  if(scan.timer) clearInterval(scan.timer);
  document.getElementById('start-btn').style.display='inline-block';
  document.getElementById('stop-btn').style.display='none';
  document.getElementById('scan-status').textContent=`Done — ${found} subdomains found out of ${total} checked`;
  addLog(`Scan complete. ${found}/${total} subdomains found.`,'ok');
  updateStats();
}

function stopScan(){
  if(scan.es) scan.es.close();
  if(scan.timer) clearInterval(scan.timer);
  document.getElementById('start-btn').style.display='inline-block';
  document.getElementById('stop-btn').style.display='none';
  document.getElementById('scan-status').textContent='Stopped by user.';
  addLog('Scan stopped.','warn');
}

function clearAll(){
  stopScan();
  scan={es:null,results:[],checked:0,total:0,timer:null,startTime:null};
  document.getElementById('results-body').innerHTML='';
  document.getElementById('no-results').style.display='block';
  document.getElementById('scan-status').textContent='Ready';
  document.getElementById('st-time').textContent='0s';
  addLog('Cleared.','info');
  updateStats();
}

document.getElementById('filter').addEventListener('input',function(){
  const q=this.value.toLowerCase();
  document.querySelectorAll('#results-body tr').forEach(tr=>{
    tr.style.display=tr.textContent.toLowerCase().includes(q)?'':'none';
  });
});

function dl(content,filename,type){
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([content],{type}));
  a.download=filename; a.click();
}

function exportCSV(){
  const rows=['hostname,ips,cname,http_status,server,title'];
  scan.results.forEach(r=>{
    rows.push([r.hostname,(r.ips||[]).join(';'),r.cname||'',
               r.http_status||'',r.server||'',r.title||''].join(','));
  });
  dl(rows.join('\n'),'subdomains.csv','text/csv');
  addLog('CSV exported','ok');
}

function exportJSON(){
  dl(JSON.stringify(scan.results,null,2),'subdomains.json','application/json');
  addLog('JSON exported','ok');
}

function copyAll(){
  navigator.clipboard.writeText(scan.results.map(r=>r.hostname).join('\n'));
  addLog('Hostnames copied to clipboard','ok');
}

document.getElementById('start-btn').addEventListener('click',startScan);
document.getElementById('stop-btn').addEventListener('click',stopScan);
document.getElementById('clear-btn').addEventListener('click',clearAll);

addLog('Subdomain finder ready','ok');
addLog('Made by Karanam Shrivasta | github.com/mrshrivasta','info');
</script>
</body>
</html>
"""


def web_mode():
    try:
        from flask import Flask, request, jsonify, Response, stream_with_context
    except ImportError:
        print("Flask not installed. Run: pip install flask"); sys.exit(1)

    # Suppress SSL warnings for HTTP probing
    if REQUESTS:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    app = Flask(__name__)

    @app.route("/")
    def index():
        return HTML

    @app.route("/api/scan")
    def api_scan():
        domain  = request.args.get("domain", "example.com").strip().lower()
        workers = int(request.args.get("workers", 50))
        timeout = float(request.args.get("timeout", 2.0))
        http    = request.args.get("http", "1") == "1"
        words_raw = request.args.get("words", "").strip()

        if words_raw:
            wordlist = [w.strip() for w in words_raw.splitlines() if w.strip()]
        else:
            wordlist = BUILTIN_WORDLIST

        # Disable HTTP probing if requests not installed
        if not REQUESTS:
            http = False

        def generate():
            import json as _j
            targets = [f"{sub}.{domain}" for sub in wordlist]
            total   = len(targets)
            checked = 0
            found   = 0
            stop_ev = threading.Event()

            def scan_one(hostname):
                nonlocal checked, found
                r = resolve_host(hostname, timeout)
                checked += 1
                return r

            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
                futs = {ex.submit(scan_one, h): h for h in targets}
                for fut in concurrent.futures.as_completed(futs):
                    try:
                        res = fut.result()
                        # Send progress every host
                        yield f"event: progress\ndata: {_j.dumps({'checked':checked,'total':total})}\n\n"
                        if res:
                            found += 1
                            yield f"event: found\ndata: {_j.dumps(res)}\n\n"
                    except Exception:
                        checked += 1
                        yield f"event: progress\ndata: {_j.dumps({'checked':checked,'total':total})}\n\n"

            yield f"event: done\ndata: {_j.dumps({'found':found,'total':total})}\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    print("\n" + "="*58)
    print("  🌐 Subdomain Finder — Educational Tool")
    print("  Made by Karanam Shrivasta")
    print("  LinkedIn: linkedin.com/in/karanam-shrivasta")
    print("  GitHub  : github.com/mrshrivasta")
    print("  Running at http://localhost:5000")
    print("="*58 + "\n")
    app.run(debug=False, port=5000, threaded=True)


if __name__ == "__main__":
    cli_mode()

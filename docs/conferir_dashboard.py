import json,re,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory='/home/claude/site');H.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',8770),H);threading.Thread(target=srv.serve_forever,daemon=True).start()
gab=json.load(open('p5/data/gabarito_recortes.json'))
F={"R01 total geral":{},"R02 país China":{'pais':'China'},"R03 país Índia":{'pais':'Índia'},"R04 material Rolamentos":{'material':'Rolamentos'},"R05 material Sensores":{'material':'Sensores'},"R06 China + Rolamentos":{'pais':'China','material':'Rolamentos'},"R07 ano 2025":{'ano':'2025'},"R08 ano 2026":{'ano':'2026'},"R09 1º trimestre 2026":{'ano':'2026','tri':'1'},"R10 Alemanha + Sensores":{'pais':'Alemanha','material':'Sensores'}}
rows=[];ok=0
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1440,'height':960});pg.route('**/docs.google.com/**',lambda r:r.abort())
    for n,f in F.items():
        pg.goto('http://127.0.0.1:8770/index.html');pg.wait_for_selector('#app .metric')
        for k,v in f.items():
            pg.evaluate("([id,v])=>{const s=document.getElementById(id);s.value=v;s.dispatchEvent(new Event('change',{bubbles:true}))}",[k,v])
        pg.wait_for_timeout(300)
        t=pg.inner_text('#app .metric');tot=re.search(r'R\$\s?([\d.]+,\d{2})',t).group(1)
        c=int(re.search(r'(\d+) importações encontradas',pg.inner_text('.filters')).group(1))
        e=gab[n];ev=f"{int(e['custo_total_brl'].split('.')[0]):,}".replace(',','.')+','+e['custo_total_brl'].split('.')[1]
        d=round(float(tot.replace('.','').replace(',','.'))-float(e['custo_total_brl']),2)
        good=(tot==ev and c==e['qtd']);ok+=good
        rows.append((n,e['qtd'],ev,c,tot,d,'OK' if good else 'FALHA'))
        print(n,e['qtd'],ev,c,tot,d,'OK' if good else 'FALHA')
    b.close()
print(ok,'/10')
json.dump(rows,open('conf_result.json','w'),ensure_ascii=False)

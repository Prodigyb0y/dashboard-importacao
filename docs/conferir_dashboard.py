import json,re,sys,threading,http.server,socketserver,functools
from playwright.sync_api import sync_playwright
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory='.');H.log_message=lambda *a:None
srv=socketserver.TCPServer(('127.0.0.1',8803),H);threading.Thread(target=srv.serve_forever,daemon=True).start()
gab=json.load(open('data/gabarito_recortes.json'))
F={"R01 total geral":{},"R02 país China":{'pais':'China'},"R03 país Índia":{'pais':'Índia'},"R04 material Rolamentos":{'material':'Rolamentos'},"R05 material Sensores":{'material':'Sensores'},"R06 China + Rolamentos":{'pais':'China','material':'Rolamentos'},"R07 ano 2024":{'ano':'2024'},"R08 ano 2025":{'ano':'2025'},"R09 ano 2026":{'ano':'2026'},"R10 1º trimestre 2026":{'ano':'2026','tri':'1'},"R11 segmento Automotivo":{'segmento':'Automotivo'},"R12 área Manutenção":{'area':'Manutenção'},"R13 Alemanha + Sensores":{'pais':'Alemanha','material':'Sensores'},"R14 segmento Energia + área Projetos + 2025":{'segmento':'Energia','area':'Projetos','ano':'2025'}}
def br(v):
    i,f=v.split('.');return f"{int(i):,}".replace(',','.')+','+f
def num(s): return float(re.sub(r'[^\d,]','',s).replace(',','.'))
out=[];ok=0
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1440,'height':960});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.route('**/docs.google.com/**',lambda r:r.abort())
    for n,f in F.items():
        pg.goto('http://127.0.0.1:8803/index.html');pg.wait_for_selector('.kpi .val')
        for k,v in f.items():
            if k in('ano','tri'): pg.click(f'button[data-seg="{k}"][data-v="{v}"]')
            else: pg.select_option(f'#f-{k}',v)
        pg.wait_for_timeout(200)
        vals=pg.eval_on_selector_all('.kpi .val','e=>e.map(x=>x.innerText)')
        ctxs=pg.eval_on_selector_all('.kpi .ctx,.kpi .share','e=>e.map(x=>x.innerText)')
        tot=re.search(r'R\$\s?([\d.]+,\d{2})',vals[0]).group(1);cnt=int(vals[1].replace('.',''))
        e=gab[n]
        atr=num(vals[4]);cob=num(vals[5]);crit=int(vals[6])
        pa=[c for c in ctxs if 'atrasados' in c][0];pa=num(pa.split('%')[0])
        okrow=(tot==br(e['custo_total_brl']) and cnt==e['qtd'] and atr==float(e['atraso_medio_dias']) and cob==float(e['cobertura_media_dias']) and crit==e['status_critico'] and abs(pa-100*e['pedidos_com_atraso']/e['qtd'])<0.06)
        d=round(num(tot)-float(e['custo_total_brl']),2);ok+=okrow
        out.append([n,e['qtd'],br(e['custo_total_brl']),cnt,tot,d,e['atraso_medio_dias'],f"{atr}",e['cobertura_media_dias'],f"{cob}",e['status_critico'],crit,e['pedidos_com_atraso'],f"{pa}%",'OK' if okrow else 'FALHA'])
        print(out[-1])
    print(ok,'/',len(F),'erros JS:',errs)
    json.dump(out,open('docs/conferencia_resultado.json','w'),ensure_ascii=False)
    b.close()

"""Referência independente (não usa nada do dashboard). Grava data/gabarito_recortes.json."""
import csv, json
from decimal import Decimal, ROUND_HALF_UP
with open("data/importacoes.csv", encoding="utf-8") as f:
    dados = list(csv.DictReader(f))
Q2, Q1 = Decimal("0.01"), Decimal("0.1")
def resumo(filtro):
    L = [r for r in dados if filtro(r)]
    custo = sum(Decimal(r["custo_total_brl"]) for r in L)
    atraso = (Decimal(sum(int(r["atraso_dias"]) for r in L)) / len(L)) if L else Decimal(0)
    cob = (Decimal(sum(int(r["cobertura_dias"]) for r in L)) / len(L)) if L else Decimal(0)
    return {"qtd": len(L), "custo_total_brl": str(custo.quantize(Q2, ROUND_HALF_UP)),
            "atraso_medio_dias": str(atraso.quantize(Q1, ROUND_HALF_UP)),
            "cobertura_media_dias": str(cob.quantize(Q1, ROUND_HALF_UP)),
            "pedidos_com_atraso": sum(int(r["atraso_dias"]) > 0 for r in L),
            "status_critico": sum(r["status_mrp"] == "Crítico" for r in L)}
tri = lambda r, ano, ms: r["data"][:4] == ano and r["data"][5:7] in ms
RECORTES = {
    "R01 total geral": lambda r: True,
    "R02 país China": lambda r: r["pais"] == "China",
    "R03 país Índia": lambda r: r["pais"] == "Índia",
    "R04 material Rolamentos": lambda r: r["material"] == "Rolamentos",
    "R05 material Sensores": lambda r: r["material"] == "Sensores",
    "R06 China + Rolamentos": lambda r: r["pais"] == "China" and r["material"] == "Rolamentos",
    "R07 ano 2024": lambda r: r["data"].startswith("2024"),
    "R08 ano 2025": lambda r: r["data"].startswith("2025"),
    "R09 ano 2026": lambda r: r["data"].startswith("2026"),
    "R10 1º trimestre 2026": lambda r: tri(r, "2026", ("01", "02", "03")),
    "R11 segmento Automotivo": lambda r: r["segmento"] == "Automotivo",
    "R12 área Manutenção": lambda r: r["area"] == "Manutenção",
    "R13 Alemanha + Sensores": lambda r: r["pais"] == "Alemanha" and r["material"] == "Sensores",
    "R14 segmento Energia + área Projetos + 2025": lambda r: r["segmento"] == "Energia" and r["area"] == "Projetos" and r["data"].startswith("2025"),
}
res = {n: resumo(f) for n, f in RECORTES.items()}
with open("data/gabarito_recortes.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
for n, v in res.items(): print(n, v)

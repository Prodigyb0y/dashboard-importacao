import csv, json
from decimal import Decimal, ROUND_HALF_UP
with open("data/importacoes.csv", encoding="utf-8") as f:
    dados = list(csv.DictReader(f))
def soma(filtro):
    linhas = [r for r in dados if filtro(r)]
    total = sum(Decimal(r["custo_total_brl"]) for r in linhas)
    return {"qtd": len(linhas), "custo_total_brl": str(total.quantize(Decimal("0.01"), ROUND_HALF_UP))}
RECORTES = {
    "R01 total geral": lambda r: True,
    "R02 país China": lambda r: r["pais"] == "China",
    "R03 país Índia": lambda r: r["pais"] == "Índia",
    "R04 material Rolamentos": lambda r: r["material"] == "Rolamentos",
    "R05 material Sensores": lambda r: r["material"] == "Sensores",
    "R06 China + Rolamentos": lambda r: r["pais"] == "China" and r["material"] == "Rolamentos",
    "R07 ano 2025": lambda r: r["data"].startswith("2025"),
    "R08 ano 2026": lambda r: r["data"].startswith("2026"),
    "R09 1º trimestre 2026": lambda r: r["data"][:7] in ("2026-01", "2026-02", "2026-03"),
    "R10 Alemanha + Sensores": lambda r: r["pais"] == "Alemanha" and r["material"] == "Sensores",
}
resultado = {nome: soma(f) for nome, f in RECORTES.items()}
with open("data/gabarito_recortes.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)

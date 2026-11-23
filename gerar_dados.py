import csv, random, datetime as dt
random.seed(20260101)
PAISES = ["China", "Índia", "Alemanha", "EUA", "Vietnã"]
MATERIAIS = ["Rolamentos", "Parafusos", "Sensores", "Borrachas", "Chapas de aço"]
FORNECEDORES = {p: [f"Fornecedor {p[:3].upper()} {i:02d} Ltda (fictício)" for i in range(1, 4)] for p in PAISES}
ALIQUOTAS = {"China": (14, 5, 9), "Índia": (12, 4, 9), "Alemanha": (10, 3, 9), "EUA": (10, 3, 9), "Vietnã": (13, 5, 9)}
def cambio_mes(ano, mes):
    base = 5.0 + (ano - 2025) * 0.2 + (mes - 1) * 0.01
    return round(base + random.uniform(-0.05, 0.05), 4)
inicio = dt.date(2025, 1, 1)
linhas = []
for i in range(1, 501):
    dias = random.randint(0, 655)
    data = inicio + dt.timedelta(days=dias)
    pais = random.choice(PAISES)
    forn = random.choice(FORNECEDORES[pais])
    mat = random.choice(MATERIAIS)
    fob = round(random.uniform(2_000, 60_000), 2)
    frete = round(fob * random.uniform(0.03, 0.09), 2)
    seguro = round(fob * random.uniform(0.005, 0.015), 2)
    cambio = cambio_mes(data.year, data.month)
    ii, ipi, pis = ALIQUOTAS[pais]
    base_calc = fob + frete + seguro
    encargos = round(base_calc * (ii + ipi + pis) / 100, 2)
    custo_brl = round((base_calc * cambio) + encargos * cambio, 2)
    linhas.append({"id": f"IMP-{i:04d}", "data": data.isoformat(), "pais": pais, "fornecedor": forn,
        "material": mat, "fob_usd": fob, "frete_usd": frete, "seguro_usd": seguro,
        "cambio_brl_usd": cambio, "aliq_ii_pct": ii, "aliq_ipi_pct": ipi, "aliq_pis_cofins_pct": pis,
        "encargos_usd": encargos, "custo_total_brl": custo_brl})
with open("data/importacoes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
    w.writeheader(); w.writerows(linhas)
print("linhas:", len(linhas))

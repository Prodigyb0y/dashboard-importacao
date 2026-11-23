"""Gera data/importacoes.csv (v2). Dados 100% fictícios; semente fixa."""
import csv, random, datetime as dt
random.seed(20261123)
PAISES = ["China", "Índia", "Alemanha", "EUA", "Vietnã"]
# material: (sku, unidade, preço unitário base em USD)
MATERIAIS = {"Rolamentos": ("MAT-ROL", "un", 85.0), "Parafusos": ("MAT-PAR", "un", 2.4),
             "Sensores": ("MAT-SEN", "un", 140.0), "Borrachas": ("MAT-BOR", "kg", 9.5),
             "Chapas de aço": ("MAT-CHA", "kg", 1.8)}
SEGMENTOS = ["Automotivo", "Industrial", "Energia", "Eletroeletrônico", "Agroindústria"]
AREAS = ["Manutenção", "Produção", "Engenharia", "Qualidade", "Projetos"]
FORNECEDORES = {p: [f"Fornecedor {p[:3].upper()} {i:02d} Ltda (fictício)" for i in range(1, 4)] for p in PAISES}
ALIQUOTAS = {"China": (14, 5, 9), "Índia": (12, 4, 9), "Alemanha": (10, 3, 9), "EUA": (10, 3, 9), "Vietnã": (13, 5, 9)}
LEAD = {"China": 45, "Índia": 40, "Alemanha": 30, "EUA": 25, "Vietnã": 42}  # dias, prazo planejado
def cambio_mes(ano, mes):
    return round(5.0 + (ano - 2025) * 0.2 + (mes - 1) * 0.01 + random.uniform(-0.05, 0.05), 4)
inicio = dt.date(2024, 1, 1)
linhas = []
for i in range(1, 1501):
    data = inicio + dt.timedelta(days=random.randint(0, 1020))   # até 17/10/2026
    pais = random.choice(PAISES); forn = random.choice(FORNECEDORES[pais])
    mat = random.choice(list(MATERIAIS)); sku, un, preco = MATERIAIS[mat]
    seg = random.choice(SEGMENTOS); area = random.choice(AREAS)
    fob = round(random.uniform(2_000, 60_000), 2)
    frete = round(fob * random.uniform(0.03, 0.09), 2)
    seguro = round(fob * random.uniform(0.005, 0.015), 2)
    cambio = cambio_mes(data.year, data.month)
    ii, ipi, pis = ALIQUOTAS[pais]
    base = fob + frete + seguro
    encargos = round(base * (ii + ipi + pis) / 100, 2)
    custo = round(base * cambio + encargos * cambio, 2)
    qtd = max(1, round(fob / preco))
    lead_plan = LEAD[pais]
    atraso = max(0, round(random.gauss(3, 7)))                    # dias de atraso na chegada
    consumo = max(1, round(qtd * random.uniform(0.3, 0.9)))        # consumo mensal (un ou kg)
    cobertura = random.randint(5, 90)                              # dias de cobertura na data do pedido
    estoque = round(consumo * cobertura / 30)
    ponto_pedido = round(consumo * (lead_plan + atraso) / 30 * 1.2)
    status = "Crítico" if cobertura < lead_plan else ("Atenção" if cobertura < lead_plan * 1.5 else "Adequado")
    linhas.append({"id": f"IMP-{i:04d}", "data": data.isoformat(), "pais": pais, "fornecedor": forn,
        "material": mat, "sku": sku, "segmento": seg, "area": area, "unidade": un, "quantidade": qtd,
        "fob_usd": fob, "frete_usd": frete, "seguro_usd": seguro, "cambio_brl_usd": cambio,
        "aliq_ii_pct": ii, "aliq_ipi_pct": ipi, "aliq_pis_cofins_pct": pis, "encargos_usd": encargos,
        "custo_total_brl": custo, "lead_time_planejado_dias": lead_plan, "atraso_dias": atraso,
        "consumo_mensal": consumo, "estoque_atual": estoque, "cobertura_dias": cobertura,
        "ponto_pedido": ponto_pedido, "status_mrp": status})
with open("docs/data/importacoes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0].keys())); w.writeheader(); w.writerows(linhas)
print("linhas:", len(linhas))

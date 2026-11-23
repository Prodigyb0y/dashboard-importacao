# Conferência dos recortes

Método: dashboard servido localmente (Chrome headless, Playwright) com a cópia congelada `data/importacoes.csv` (sha256 `d3dcbbe5a3baa4469b608eb3973b1a8c4944ae3449d99d111e9928f2cdfe040d`, 1.500 linhas). Para cada recorte, os filtros foram aplicados na tela e os valores dos cartões da Visão geral foram lidos. Valores esperados: `data/gabarito_recortes.json`, gerado por `referencia.py` (script independente, Decimal, sem usar código do dashboard). A fonte Google Sheets foi bloqueada de propósito para fixar a cópia do repositório. Script: `docs/conferir_dashboard.py`.

| Recorte | Linhas esp. | Custo esperado (R$) | Linhas exib. | Custo exibido (R$) | Dif. (R$) | Atraso médio esp./exib. (d) | Cobertura média esp./exib. (d) | Críticos esp./exib. | % atrasados (esp. calc.) | Resultado |
|---|---|---|---|---|---|---|---|---|---|---|
| R01 total geral | 1500 | 307.292.989,94 | 1500 | 307.292.989,94 | 0.00 | 4.9 / 4.9 | 48.4 / 48.4 | 518 / 518 | 64.6% (64.6%) | OK |
| R02 país China | 341 | 75.041.961,00 | 341 | 75.041.961,00 | 0.00 | 5.0 / 5.0 | 48.6 / 48.6 | 145 / 145 | 64.2% (64.2%) | OK |
| R03 país Índia | 295 | 62.345.085,62 | 295 | 62.345.085,62 | 0.00 | 4.7 / 4.7 | 49.3 / 49.3 | 110 / 110 | 62.7% (62.7%) | OK |
| R04 material Rolamentos | 302 | 60.621.633,28 | 302 | 60.621.633,28 | 0.00 | 4.9 / 4.9 | 49.0 / 49.0 | 102 / 102 | 64.9% (64.9%) | OK |
| R05 material Sensores | 277 | 58.152.488,94 | 277 | 58.152.488,94 | 0.00 | 4.9 / 4.9 | 50.1 / 50.1 | 87 / 87 | 67.5% (67.5%) | OK |
| R06 China + Rolamentos | 59 | 12.457.987,75 | 59 | 12.457.987,75 | 0.00 | 5.0 / 5.0 | 47.8 / 47.8 | 27 / 27 | 64.4% (64.4%) | OK |
| R07 ano 2024 | 543 | 106.187.412,70 | 543 | 106.187.412,70 | 0.00 | 4.7 / 4.7 | 48.8 / 48.8 | 182 / 182 | 66.7% (66.7%) | OK |
| R08 ano 2025 | 529 | 108.412.591,91 | 529 | 108.412.591,91 | 0.00 | 5.1 / 5.1 | 48.7 / 48.7 | 182 / 182 | 62.4% (62.4%) | OK |
| R09 ano 2026 | 428 | 92.692.985,33 | 428 | 92.692.985,33 | 0.00 | 4.8 / 4.8 | 47.5 / 47.5 | 154 / 154 | 64.7% (64.7%) | OK |
| R10 1º trimestre 2026 | 153 | 32.070.703,75 | 153 | 32.070.703,75 | 0.00 | 5.2 / 5.2 | 47.4 / 47.4 | 51 / 51 | 68.6% (68.6%) | OK |
| R11 segmento Automotivo | 279 | 57.224.417,50 | 279 | 57.224.417,50 | 0.00 | 5.0 / 5.0 | 47.0 / 47.0 | 107 / 107 | 68.1% (68.1%) | OK |
| R12 área Manutenção | 324 | 65.489.355,33 | 324 | 65.489.355,33 | 0.00 | 4.9 / 4.9 | 48.7 / 48.7 | 108 / 108 | 65.7% (65.7%) | OK |
| R13 Alemanha + Sensores | 57 | 11.262.627,44 | 57 | 11.262.627,44 | 0.00 | 5.4 / 5.4 | 51.7 / 51.7 | 12 / 12 | 73.7% (73.7%) | OK |
| R14 segmento Energia + área Projetos + 2025 | 22 | 4.268.018,60 | 22 | 4.268.018,60 | 0.00 | 4.7 / 4.7 | 56.2 / 56.2 | 5 / 5 | 68.2% (68.2%) | OK |

Resultado: 14 de 14 recortes sem diferença (custo, contagem, atraso médio, cobertura média, críticos e % de pedidos atrasados).

Observações:
- O critério original (10 recortes sobre 500 linhas) foi substituído por 14 recortes sobre 1.500 linhas, por decisão do autor, ao incluir segmento, área, MRP e o ano de 2024.
- Ainda não conferido: carregamento direto do Google Sheets (a planilha precisa receber o novo CSV) e a página publicada no GitHub Pages.

Planilha (fonte primária): [dashboard-importacao-base v2](https://docs.google.com/spreadsheets/d/1G8Uidlj_B9qH8sGUY4FsBWGn6F_U6-7iR92cn-Zc-DY/edit), importada do mesmo CSV. A exportação CSV da planilha, lida de outra origem (CORS ok), tem 1.500 linhas, o mesmo cabeçalho e soma de `custo_total_brl` de R$ 307.292.989,94, igual ao gabarito R01. O sha256 do arquivo exportado difere do CSV do repositório porque o Sheets reformata números (por exemplo, `49144.2` em vez de `49144.20`); o conteúdo numérico é o mesmo. Ainda não testado a partir de `github.io`.

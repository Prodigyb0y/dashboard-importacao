# Conferência dos 10 recortes

Método: dashboard servido localmente (Chrome headless, Playwright) com a cópia congelada `data/importacoes.csv` (sha256 `7cfd869b09993ed8c0fd652faa28f630bd4f9b520dac6f4cb288f285e1c86b2b`). Para cada recorte, o filtro foi aplicado e o total (R$) e a contagem exibidos foram lidos da tela. Valores esperados: `data/gabarito_recortes.json`, gerado por `referencia.py` (script independente, Decimal). Fonte dos dados na conferência: cópia do repositório (Google Sheets bloqueado de propósito para fixar a fonte).

| Recorte | Linhas esperadas | Esperado (R$) | Linhas exibidas | Exibido (R$) | Diferença (R$) | Resultado |
|---|---|---|---|---|---|---|
| R01 total geral | 500 | 108.917.549,62 | 500 | 108.917.549,62 | 0.00 | OK |
| R02 país China | 105 | 24.634.181,75 | 105 | 24.634.181,75 | 0.00 | OK |
| R03 país Índia | 105 | 22.578.655,52 | 105 | 22.578.655,52 | 0.00 | OK |
| R04 material Rolamentos | 95 | 21.936.286,11 | 95 | 21.936.286,11 | 0.00 | OK |
| R05 material Sensores | 96 | 21.167.381,12 | 96 | 21.167.381,12 | 0.00 | OK |
| R06 China + Rolamentos | 16 | 3.589.669,10 | 16 | 3.589.669,10 | 0.00 | OK |
| R07 ano 2025 | 277 | 59.662.578,09 | 277 | 59.662.578,09 | 0.00 | OK |
| R08 ano 2026 | 223 | 49.254.971,53 | 223 | 49.254.971,53 | 0.00 | OK |
| R09 1º trimestre 2026 | 58 | 12.073.660,83 | 58 | 12.073.660,83 | 0.00 | OK |
| R10 Alemanha + Sensores | 21 | 4.773.155,32 | 21 | 4.773.155,32 | 0.00 | OK |

Resultado: 10 de 10 recortes com diferença zero.

Limitação: a conferência contra a planilha do Google Sheets (fonte primária) e no GitHub Pages ainda não foi feita.

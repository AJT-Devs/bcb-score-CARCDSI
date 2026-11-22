# Artigo SBC

Fonte: `main.tex`; referências verificadas: `references.bib`; template original preservado em `template/`. As referências de BCB, CatBoost e Chronos-2 foram verificadas nas fontes primárias em 22/11/2026.

Na raiz, com `PYTHONPATH=src`, exporte uma execução concluída:

```powershell
.\.venv\Scripts\python.exe -m visualization.export_paper runs/2025-comparison
Push-Location paper
tectonic -k --keep-logs main.tex
Pop-Location
```

Alternativa pdfLaTeX/BibTeX em `paper/`: `pdflatex main.tex`, `bibtex main`, `pdflatex main.tex` duas vezes. Tectonic executa os passes automaticamente. O pacote T1 assegura a fonte Times do estilo também sob XeTeX; não modifica o `.sty`.

`generated/results.tex`, `metrics.csv` e `test_mae.png` vêm do código, sem digitação de métricas. Manifestos e auditorias pequenos documentam a execução; previsões por perfil, modelos e CSVs brutos não são copiados ao artigo.

Autores informados pelo usuário: João Alves Passos e Túlio Kenji Yoshimura. Afiliação e e-mails não informados. O limite de páginas do evento não foi fornecido; a formatação SBC não define esse limite. Antes de submissão é necessário confirmar esses dados. Fine-tuning e avaliação por publicações históricas não foram realizados. O documento diferencia piloto Chronos amostrado da cobertura integral dos outros métodos.

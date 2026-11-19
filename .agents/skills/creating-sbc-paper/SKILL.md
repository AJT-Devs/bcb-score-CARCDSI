---
name: creating-sbc-paper
description: Use when creating, editing, or formatting this project's paper in LaTeX using the SBC template, including sbc-template.sty v2017.
---

# Paper do projeto no formato SBC

Use o template local em `paper/template/` como fonte de verdade: leia `main.tex` para as instruções e exemplos, `sbc-template.sty` para a formatação efetiva (atualizado em dezembro de 2017) e `sbc.bst` para a bibliografia. Preserve esses arquivos de referência; crie ou edite o artigo fora de `paper/template/`, salvo pedido explícito em contrário. Adapte um artigo existente antes de criar outro.

- Use `\documentclass[12pt]{article}` e `\usepackage{sbc-template}`; disponibilize o `.sty` e o `.bst` locais ao compilador sem modificar seu conteúdo. Siga o preâmbulo e os comandos de autoria, afiliação e e-mail de `main.tex`. Deixe o pacote definir margens A4, fonte, espaçamento, seções, legendas e ausência de numeração de páginas, evitando substituições que contrariem o estilo.
- Para artigo em português, inclua `abstract` em inglês e `resumo` em português; para artigo em inglês, inclua apenas `abstract`. Cada resumo deve ter até 10 linhas e ficar na primeira página. Use título, autores e afiliações reais; respeite eventual anonimização exigida pelo evento.
- Use legendas de figuras abaixo das imagens e de tabelas acima das tabelas; numere e referencie os elementos no texto. Siga os exemplos do template para imagens, citações e bibliografia com `\bibliographystyle{sbc}`. Use referências verificáveis, sem inventar dados bibliográficos.
- O limite de páginas é definido pelo evento, não pelo template. Aplique regras adicionais do evento quando conhecidas e sinalize conflitos com o modelo ou requisitos que não estejam disponíveis.
- Fundamente métodos, resultados e conclusões nos dados e artefatos efetivos do projeto. Preserve as limitações, filtros e decisões metodológicas; não invente métricas, previsões, experimentos ou referências.

Compile o artigo com o motor LaTeX e BibTeX apropriados quando disponíveis, repetindo as passagens necessárias para resolver referências. Confira o PDF, especialmente primeira página, resumos, legendas, margens, referências e limite de páginas. Informe erros, avisos relevantes ou a impossibilidade de compilar e inspecionar o PDF; não afirme conformidade visual sem essa inspeção.

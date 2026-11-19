# Registro 007 - Renomear skill SBC

## Prompt integral do usuário

mude o nome para apenas sbc-paper

## Ações e decisão

A skill local `creating-sbc-paper` foi renomeada para `sbc-paper`, incluindo sua pasta e o campo `name` do frontmatter. O conteúdo e o comportamento permanecem iguais; o novo nome passa a ser usado para descoberta e invocação. O registro anterior foi preservado como histórico.

## Arquivos criados, movidos ou alterados

- `.agents/skills/creating-sbc-paper/SKILL.md` movido para `.agents/skills/sbc-paper/SKILL.md` e atualizado.
- `artifacts/007-renomear-skill-sbc-paper.md` criado.

## Validações e limitações

- Verificados o nome da pasta e o frontmatter, a preservação do conteúdo e a existência dos arquivos do template referenciados.
- Verificados o estado do Git e espaços em branco com `git diff --check`; não foram incluídos dados ou credenciais.
- O validador oficial continua indisponível: o Python da `.venv` está ausente e o Python disponível não possui PyYAML.

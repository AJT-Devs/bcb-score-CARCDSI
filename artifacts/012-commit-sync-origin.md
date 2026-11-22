# Commit e sincronização com origin — 22/11/2026

## Prompt integral do usuário

faz commit e sync com a origin , cria a mensagem de features

## Ações e escopo

Autorização explícita para criar commit e enviar à origin. Branch atual: `main`; remoto: `https://github.com/AJT-Devs/bcb-score-CARCDSI.git`. `git fetch origin` concluído; antes do commit, `HEAD...origin/main` apresentou `0 0`, sem divergência a integrar.

Preparadas as alterações da tarefa anterior: ingestão e validação SCR, atributos e cortes temporais, baselines, CatBoost, Chronos-2, pipelines, testes, documentação, artigo SBC e evidências agregadas. Os arquivos estão detalhados em `011-preparacao-experimentos-artigo.md`. Este registro é o único arquivo adicional desta tarefa. Não há nova decisão arquitetural nem mudança no comportamento do projeto nesta operação de Git.

Mensagem de feature escolhida:

```text
feat: implementa previsão temporal com CatBoost e Chronos-2

- prepara e valida o painel mensal SCR com atributos sem vazamento
- adiciona baselines, treinamento, inferência, métricas e cobertura
- registra experimentos reais, documentação e artigo no formato SBC
- inclui testes de calendário, dados inválidos e integração dos pipelines
```

## Validações realizadas antes do commit

- `git diff --check`: aprovado, somente avisos de conversão LF/CRLF.
- `.venv/Scripts/python.exe -m unittest discover -s tests -q`, com `PYTHONPATH=src`: 16 testes aprovados.
- `.venv/Scripts/python.exe -m pip check`: sem dependências quebradas.
- Conferência de arquivos novos e tamanhos: apenas código, documentos, PDF, figura e evidências resumidas; nenhum arquivo grande de dados.
- `git check-ignore`: confirmou exclusão de dados brutos, `.venv`, checkpoint e previsões individuais em `runs/`.

## Operação de sincronização

Criar o commit com a mensagem acima e executar `git push origin main`, sem force push. Conferir hash remoto, diferenças de commits e estado limpo após o envio. A confirmação final da operação é apresentada ao usuário após o retorno do Git; este registro integra o próprio commit e não antecipa um resultado de push.

Nenhum dado bruto, ambiente virtual, segredo ou peso de modelo deve integrar o commit. Alterações e logs anteriores foram preservados.

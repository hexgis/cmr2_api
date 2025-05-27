# 🚀 Merge Request: [SC-819] - Criar API de busca de palavra em um JSONField

## 📌 Descrição
<!-- Descreva de forma objetiva o que foi feito neste MR. -->
Encontrar uma forma performática de buscar uma palavra dentro do campo Properties de todas as VectorGeometries vinculadas ao Vector “Spectra”. Ele deve retornar os resultados agrupados por fileName.

## 🎯 Objetivo
<!-- Explique o propósito principal dessa mudança. -->
- [x] Criar nova API para [descrição]
- [ ] Corrigir bug relacionado
- [ ] Melhorar performance

## 🔗 Tarefa no Jira
[[SC-819] - Criar API de busca de palavra em um JSONField](https://xskylab.atlassian.net/browse/SC-819)

## 🛠️ Implementação
<!-- Explique as mudanças técnicas feitas no código. -->
- A melhor forma de busca encontrada foi o Full-Text Search (FTS) do PostgreSQL é um mecanismo avançado de busca textual que permite encontrar palavras e frases dentro de textos armazenados no banco de dados. Ele é muito mais eficiente do que buscas comuns com LIKE '%palavra%', pois usa estruturas otimizadas para indexação e ranking de relevância.
- Foi desenvolvido uma rota na API para buscar e listar de forma paginada os documentos inseridos na aplicação.
- Foi desenvolvido uma API de consulta e filtro de documento por ID.

## 📸 Prints / 🎥 Vídeos
<!-- Adicione imagens ou vídeos para ilustrar o funcionamento da feature/correção. -->
![image](/uploads/87996cb427cadadf0e01181f34bc911a/image.png)
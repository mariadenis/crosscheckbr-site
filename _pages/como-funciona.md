---
layout: page
permalink: /como-funciona/
title: Como funciona
description: As etapas da análise, da mensagem até a resposta.
nav: true
nav_order: 1
---

Cada consulta passa pelas mesmas etapas. Todas ficam registradas na resposta, com a situação de cada uma: concluída, parcial, pulada ou com falha. Quando uma etapa falha, a análise continua e a falha aparece como limitação.

## As etapas

| Etapa | O que acontece |
| --- | --- |
| 1. Recebimento | A mensagem é classificada como texto, título ou link. Links só são lidos quando pertencem a um portal do catálogo. |
| 2. Afirmações | O texto é dividido em afirmações factuais que podem ser verificadas. |
| 3. Base de checagem | Cada afirmação é procurada no índice das agências de checagem. |
| 4. Descoberta | Uma busca de notícias encontra o que foi publicado recentemente sobre o assunto. O conteúdo das fontes mais próximas é lido. |
| 5. Julgamento | Cada notícia encontrada é avaliada: ela sustenta a afirmação, refuta, ou trata de outro assunto? |
| 6. Corroboração | O sistema conta quantos veículos independentes tratam do assunto. Republicações e veículos do mesmo grupo contam uma vez. |
| 7. Modelo e padrões | O modelo próprio estima a probabilidade de desinformação, em textos com 80 palavras ou mais. Os padrões textuais são identificados. |
| 8. Avaliação | Os sinais são combinados por regras e pesos fixos, e a resposta é redigida por modelos de texto neutros. |

## Por que a resposta nunca é "fato" ou "fake"

Uma resposta binária esconde a incerteza e pede que a pessoa confie no sistema. O Crosscheck BR faz o contrário: mostra o que encontrou, diz o que não conseguiu verificar e devolve a decisão para quem lê. Toda resposta termina com três perguntas para a pessoa conferir por conta própria:

1. A data do fato é a mesma da publicação, ou o conteúdo é antigo?
2. Quem assina o conteúdo original?
3. A informação aparece em mais de um veículo independente?

## O que cada sinal pesa

As checagens de agências são o sinal mais forte. Quando uma agência já verificou exatamente aquela afirmação, essa é a melhor evidência disponível. A corroboração entre veículos vem em seguida. O modelo próprio e os padrões textuais são indícios auxiliares, com peso menor.

## Limitações atuais

- O modelo próprio só opina em textos com 80 palavras ou mais. Em textos curtos ele erra por causa do formato.
- Sem um modelo de linguagem configurado, a relação entre a notícia e as fontes é medida por palavras em comum, o que pode trazer fontes sem relação.
- Portais com acesso pago ou proteção contra robôs limitam a leitura do conteúdo.

Os detalhes e a situação de cada requisito estão na página de [requisitos]({{ '/requisitos/' | relative_url }}).

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
| 1. Recebimento | A mensagem é classificada como texto, título ou link. O link só é lido quando pertence a um portal do catálogo; senão, o robô pede que você cole o texto. Relato de segunda mão, opinião, sátira e afirmação vaga são sinalizados. |
| 2. Afirmações | O texto é dividido em afirmações que podem ser verificadas, sem a moldura de encaminhamento ("me mandaram que…") e mantendo o autor de uma fala ("Fulano disse que…"). |
| 3. Base de checagens | Cada afirmação é procurada nas checagens já publicadas pelas agências: a base própria e, quando configurada, a Google Fact Check Tools. |
| 4. Busca na web | Só quando a base não tem uma checagem aplicável: uma busca encontra o que os veículos e as agências publicaram. Sem resultado útil, a busca é reformulada uma vez. |
| 5. Leitura | O conteúdo das páginas encontradas é lido. Páginas iniciais, listagens, redes sociais e PDFs não são lidos. |
| 6. Julgamento | Cada página lida é avaliada frente à afirmação: confirma, contesta, só relata ou trata de outro assunto. O julgamento só vale com um trecho citado que exista na página. |
| 7. Comparação | Republicações e veículos do mesmo grupo contam uma vez. Selos e datas divergentes entre as fontes são apontados. |
| 8. Data | Se o texto diz "hoje", "ontem" ou "agora", fontes de outro período perdem peso e recebem o aviso "anterior ao período do texto". |
| 9. Estimativa | Uma regra fixa e documentada combina as fontes e os selos e chega à propensão. A conclusão é escrita por modelos de texto neutros, não por inteligência artificial. |

## Por que a resposta nunca é "fato" ou "fake"

Uma resposta binária esconde a incerteza e pede que a pessoa confie no sistema. O Checa AI faz o contrário: mostra o que encontrou, diz o que não conseguiu verificar e devolve a decisão para quem lê. Toda resposta termina com três perguntas para a pessoa conferir por conta própria:

1. A data do fato é a mesma da publicação, ou o conteúdo é antigo?
2. Quem assina o conteúdo original?
3. A informação aparece em mais de um veículo independente?

## O que conta na estimativa

- **Checagem de agência sobre a mesma afirmação** é a evidência mais forte. Quando uma agência de checagem contesta a afirmação, isso pesa como um selo.
- **Notícia lida por inteiro** que confirma ou contesta a afirmação conta um voto por grupo de fontes independentes.
- **Só a manchete não vota**: uma página que não pôde ser lida aparece na lista como "só manchete", sem influenciar a estimativa.
- **Rede social ou site pouco acessado, sozinho,** não leva a estimativa a "alta" nem a "baixa".
- **Sem nenhuma fonte que confirme ou conteste**, a resposta é "não foi possível estimar".

O modelo próprio e os padrões textuais aparecem como sinais de estilo e não entram na conta.

## Limitações atuais

- Sem o modelo de linguagem, as fontes não são julgadas e a resposta é "não foi possível estimar".
- Afirmações que nenhuma agência checou e que a imprensa só relata (por exemplo, "café cura câncer") tendem a terminar em "não foi possível estimar".
- Portais com acesso pago limitam a leitura do conteúdo.

Os detalhes e o status de cada requisito estão na página de [requisitos]({{ '/requisitos/' | relative_url }}).
